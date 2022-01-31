import os
import datetime
import numpy as np
import pandas as pd
import sys
import warnings
from tqdm import tqdm as tqdm
from . import neuralynx_io as nlx
from .neuralynx_io import nev_as_records,load_nev,load_ncs

from pynwb import NWBFile, TimeSeries,NWBHDF5IO
from pynwb import TimeSeries, NWBFile,NWBHDF5IO
from pynwb.ecephys import ElectricalSeries,LFP
from pynwb.misc import AnnotationSeries

def get_channel_id(fp):
    fn = fp.split('CSC')[1]
    if '_' in fn:
        return int(fn.split('_')[0])
    else:
        return int(fn.split('.ncs')[0])

def iter_ncs_to_timeseries(ncs_fps,data_time_len=None,dtype=np.float16,fs = 4000,electrode_locations=None):
    channel_ids = []
    np_fps = []
    rates = []
    
    # Write all numpy files, then iter again yielding timeseries
    for fp in tqdm(ncs_fps,desc='compressing channels to {} {}Hz'.format(dtype,fs)):
        d,f = os.path.split(fp)
        name = f.split('.ncs')[0]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                ncs = nlx.load_ncs(fp,load_time=False)
            except ValueError:
                print('Error loading {}'.format(os.path.split(fp)[-1]))
                print('skipping...')

        # Use AcqEntName instead of channel_number to infer channel
        # ch = int(ncs['header']['AcqEntName'][3:])
        ch = ncs['channel_number']
        channel_ids.append(ch)
        downsample = int(ncs['sampling_rate']/fs)
#         rates.append(float(int(ncs['sampling_rate']/downsample)))
        rates.append(float(fs))
        np_fps.append(os.path.join(d,name+'.npy'))
        if data_time_len is not None:
            n_samples = int(data_time_len*ncs['sampling_rate'])
            np.save(os.path.join(d,name),ncs['data'][:n_samples:downsample].astype(dtype))
        else:
            np.save(os.path.join(d,name),ncs['data'][::downsample].astype(dtype))
        
    for fp,ch,rate in zip(np_fps,channel_ids,rates):
        
        # Load compressed data
        data = np.load(fp)
        
        ts_kwargs = {
            #'name':'channel_{}'.format(int(ch)),
            'rate':rate,
            'data':data.astype(dtype),
            'starting_time':ncs['timestamp'][0]/1000/1000,
            'comments': '{} originally from file {}'.format(ncs['header']['AcqEntName'],ncs['file_path']),
        }

        yield ch,ts_kwargs
        os.remove(fp)
        
def ncs_to_timeseries(ncs,data_time_len=None,fs=1000,dtype=np.float16):
    rate = float(ncs['sampling_rate'])
    n_samples = None

    # Use AcqEntName instead of channel_number to infer channel
    ch = ncs['channel_number']
    # ch = int(ncs['header']['AcqEntName'][3:])
    if fs:
        downsample = int(rate/fs)
        rate = fs
    else:
        downsample=1
        
    if data_time_len:
        n_samples = int(data_time_len*rate)
        data = ncs['data'][:n_samples:downsample]
    else:
        data = ncs['data']

    # ch_ts = TimeSeries(name='channel_{}'.format(ch),rate =rate, data=data.astype(np.float16),conversion=1.0/10**6,unit='V')
    ts_kwargs = {
        'name': os.path.split(ncs['file_path'])[1],
        'rate':float(rate),
        'data':data.astype(dtype),
        'starting_time':ncs['timestamp'][0]/1000/1000,
        'comments': '{} originally from file {}'.format(ncs['header']['AcqEntName'],ncs['file_path']),
        'unit':'uV',
    }

    return TimeSeries(**ts_kwargs)

def add_electrodes(nwb,trodes,device,group_col='wire_num'):
    wire_loc = trodes[[group_col,'anat_lg']].drop_duplicates()

    # Create electrode groups
    e_groups = []
    for i,wire in wire_loc.iterrows():
        grp = nwb.create_electrode_group(
            name='wire_{}'.format(wire.wire_num),
            description='SEEG wire',
            location=wire.anat_lg,
            device=device)

        e_groups.append(grp)

    for i,df_grp in enumerate(trodes.groupby(group_col)):
        grp_name, sub_grp = df_grp
        e_grp = e_groups[i]
        for j,row in sub_grp.iterrows():
            nwb.add_electrode(id=row.chan_num,
                                  x=0.0,y=0.0,z=0.0,
                                  imp=float(-1),
                                  location=row.anat_sh, filtering='none',
                                  group=e_grp)

def nev_to_behavior_annotation(nev_fp,practice_incl=False):
    nev = load_nev(nev_fp)
    ev = pd.DataFrame.from_records(nev_as_records(nev),index='TimeStamp')

    ev['EventString'] = [str(v,'utf-8') for v in ev.EventString.values]
    ev['time'] = pd.to_datetime(ev.index.values,unit='us',utc=True)
    ev = ev[ev.ttl==1]

    label_blockstart(ev)
    n_blocks = int(len(ev[ev.label=='block_start'])/2)
    n_ttls = int(n_blocks*17)
    if practice_incl:
        n_ttls-=5

    ev_ts = np.array([t.timestamp() for t in ev.time])

    events = AnnotationSeries(name='ttl', data=ev.label.values[:n_ttls], timestamps=ev_ts[:n_ttls])

    return events

def initialize_nwb(ncs_paths,
                   desc='',
                   lab='Thompson Lab',
                   institution='University of Colorado Anschutz',):
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        first_ncs = ncs_paths.pop(0)
        ncs = nlx.load_ncs(first_ncs,load_time=False)
    
    uuid = ncs['header']['SessionUUID']
    start_time = pd.to_datetime(ncs['timestamp'][0],unit='us',utc=True).to_pydatetime()
    # start_time = ncs['header']['TimeCreated_dt']
    start_time_sec = start_time.timestamp()
    nwbfile = NWBFile(session_description=desc,
                    identifier=uuid,
                    session_id=uuid,
                    lab=lab,
                    institution=institution,
                    session_start_time=start_time
                    )
    ncs_paths.append(first_ncs)
    
    return nwbfile

def add_ttl(nwbfile,nev_fp):
    with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nev = load_nev(nev_fp)
            if len(nev['events']) > 0:
                ev = pd.DataFrame.from_records(nev_as_records(nev),index='TimeStamp')

    ev['EventString'] = [str(v,'utf-8') for v in ev.EventString.values]
    ev['time'] = pd.to_datetime(ev.index.values,unit='us',utc=True)
    ev = ev[ev.ttl==1]

    ev_ts = np.array([t.timestamp() for t in ev.time])

    events = AnnotationSeries(name='ttl', data=ev.ttl.values, timestamps=ev_ts)
    nwbfile.add_acquisition(events)
    return nwbfile

def ncs_to_grp_eseries(grp,electrode_locations,nwbfile,data_time_len=None,dtype=np.float32,fs=None):
    grp_ts_kwargs = []
    channels = []

    for ch,ts_kwargs in iter_ncs_to_timeseries(grp.ncs_path.values,data_time_len=data_time_len,dtype=dtype,fs=fs):
#             row = electrode_locations.where(electrode_locations.chan_num==ch+1).dropna().iloc[0]
        channels.append(ch)

        grp_ts_kwargs.append(ts_kwargs)
        
    if len(grp_ts_kwargs) > 0:
        dats = [t['data'] for t in grp_ts_kwargs]
    
    shapes = np.unique([len(t['data']) for t in grp_ts_kwargs])
    if len(shapes) == 1:
        dats = np.stack(dats)
        ts_kwargs['data'] = dats
    
    electrode_table_region = nwbfile.create_electrode_table_region(channels,'Channel')
    ts_kwargs['electrodes'] = electrode_table_region
    ts_kwargs['name'] = grp.anat_sh.unique()[0]
    ts = ElectricalSeries(**ts_kwargs)
    return ts
                
def ncs_to_nwb_raw(ncs_paths, desc='', lab='Thompson Lab',institution='University of Colorado Anschutz', nev_fp=None, fs=None, electrode_locations=None):
    nwbfile = initialize_nwb(ncs_paths, desc, lab, institution)
    if nev_fp is not None:
        nwbfile = add_ttl(nwbfile,nev_fp)
    
    if electrode_locations is not None:
        dev = nwbfile.create_device(name='Neuralynx')
        add_electrodes(nwbfile,electrode_locations,dev)
        fp_df = pd.DataFrame({'chan_num':[get_channel_id(p) for p in ncs_paths],'ncs_path':ncs_paths})
        electrode_locations = electrode_locations.merge(fp_df,on='chan_num')
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                for i,grp in electrode_locations.groupby('wire_num'):
                    eseries = ncs_to_grp_eseries(grp, electrode_locations, nwbfile, dtype=np.float16, fs=fs)
                    nwbfile.add_acquisition(eseries)
            except ValueError:
                print('Error loading {}'.format(os.path.split(fp)[-1]))
                print('skipping...')
    else:
        for nfp in tqdm(ncs_paths):
            nwbfile.add_acquisition(ncs_to_timeseries(load_ncs(nfp,load_time=False)))
        
    return nwbfile

def ncs_to_nwb(ncs_paths,
                desc='',
                nev_path=None,
                electrode_locations=None,
                lab='Thompson Lab',
                institution='University of Colorado Anschutz',
                trim_buffer=60*10,
                ):
    """Create NWB file from neuralynx data file paths and electrode locations map"""
    
    nwbfile = initialize_nwb(ncs_paths,desc,lab,institution)

    if nev_path is not None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            nev = load_nev(nev_path)
            if len(nev['events']) > 0:
                ev = pd.DataFrame.from_records(nev_as_records(nev),index='TimeStamp')

                ev['EventString'] = [str(v,'utf-8') for v in ev.EventString.values]
                ev['time'] = pd.to_datetime(ev.index.values,unit='us',utc=True)
                ev = ev[ev.ttl==1]
                ev_ts = np.array([t.timestamp() for t in ev.time]) - start_time.timestamp()
                data_time_len = ev_ts[-1]+trim_buffer
    
    if electrode_locations is not None:
        add_electrodes(nwbfile,electrode_locations,dev)
        fp_df = pd.DataFrame({'chan_num':[get_channel_id(p) for p in ncs_paths],'ncs_path':ncs_paths})
        electrode_locations = electrode_locations.merge(fp_df,on='chan_num')

    
    else:
        data_time_len = len(ncs['data'])/int(ncs['sampling_rate'])

    nwbfile.create_processing_module(name='ecephys',
                                description='preprocessed extracellular electrophysiology')
    
    if electrode_locations is not None:
        for i,grp in electrode_locations.groupby('wire_num'):
            channels = list(grp.chan_num.values)
            grp_ts_kwargs = []
            for ch,ts_kwargs in iter_ncs_to_timeseries(grp.ncs_path.values,data_time_len):
                try:
                    electrode_table_region = nwbfile.create_electrode_table_region(channels,'Channel')
                    row = electrode_locations.where(electrode_locations.chan_num==ch+1).dropna().iloc[0]
                    ts_kwargs['electrodes'] = electrode_table_region
                    grp_ts_kwargs.append(ts_kwargs)
                except IndexError:
                    pass
            if len(grp_ts_kwargs) > 0:
                dats = [t['data'] for t in grp_ts_kwargs]
                shapes = np.unique([len(d) for d in dats])
                if len(shapes) == 1:
                    dats = np.stack(dats)
                ts_kwargs['name'] = grp.anat_sh.unique()[0]
                ts_kwargs['data'] = dats

                ts = ElectricalSeries(**ts_kwargs)
                if ts_kwargs['name'] not in nwbfile.processing['ecephys'].fields.keys():
                    nwbfile.processing['ecephys'].add(ts)
                else:
                    print('Failed to load: ',ts.name)
    
    else:
        for ch,ts_kwargs in iter_ncs_to_timeseries(ncs_paths,data_time_len):
            try:
                electrode_table_region = nwbfile.create_electrode_table_region([ch],'Channel')
                row = electrode_locations.where(electrode_locations.chan_num==ch+1).dropna().iloc[0]
                ts_kwargs['electrodes'] = electrode_table_region
            except IndexError:
                pass
        if len(grp_ts_kwargs) > 0:
            dats = [t['data'] for t in grp_ts_kwargs]
            shapes = np.unique([len(d) for d in dats])
            if len(shapes) == 1:
                dats = np.stack(dats)
            ts_kwargs['name'] = grp.anat_sh.unique()[0]
            ts_kwargs['data'] = dats

            ts = TimeSeries(**ts_kwargs)
        if ts.name not in nwbfile.acquisition.keys():
            nwbfile.add_acquisition(ts)
        else:
            print('Failed to load: ',ts.name)
        
    return nwbfile

def nlx_to_nwb(nev_fp,ncs_paths,desc='', trim_buffer=60*10, practice_incl=False,electrode_locations=None):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ncs = nlx.load_ncs(ncs_paths.pop(0),load_time=False)
        nev = nlx.load_nev(nev_fp)

    uuid = nev['header']['SessionUUID']
    start_time = pd.to_datetime(ncs['timestamp'][0],unit='us',utc=True).to_pydatetime()
    start_time_sec = start_time.timestamp()
    nwbfile = NWBFile(session_description=desc,
                      identifier=uuid,
                      session_start_time=start_time
                     )

    dev = nwbfile.create_device(name='Neuralynx')
    # ts = ncs_to_timeseries(ncs)

    if electrode_locations is not None:
        add_electrodes(nwbfile,electrode_locations,dev)
    
    ev = pd.DataFrame.from_records(nev_as_records(nev),index='TimeStamp')

    ev['EventString'] = [str(v,'utf-8') for v in ev.EventString.values]
    ev['time'] = pd.to_datetime(ev.index.values,unit='us',utc=True)
    ev = ev[ev.ttl==1]
    label_blockstart(ev)
    n_blocks = int(len(ev[ev.label=='block_start'])/2)
    n_ttls = int(n_blocks*17)
    if practice_incl:
        n_ttls-=5

    # ev['TimeStamp'] = ev.index.values/10**6 - start_time.timestamp()
    ev_ts = np.array([t.timestamp() for t in ev.time]) - start_time.timestamp()
#     start_stop = ev[ev.EventString.isin(['Starting Recording','Stopping Recording'])]
    
    events = AnnotationSeries(name='ttl', data=ev.label.values[:n_ttls], timestamps=ev_ts[:n_ttls])
    data_time_len = events.timestamps[-1]+trim_buffer

    nwbfile.add_acquisition(events)
    
    lfp = LFP(name='LFP')
    nwbfile.add_acquisition(ncs_to_timeseries(ncs,data_time_len))

    for ch,ts_kwargs in iter_ncs_to_timeseries(ncs_paths,data_time_len):
        if electrode_locations is not None:
            # ts_kwargs['electrodes']=electrode_table_region
            try:
                electrode_table_region = nwbfile.create_electrode_table_region([ch],'Channel')
                row = electrode_locations.where(electrode_locations.chan_num==ch+1).dropna().iloc[0]
                ts_kwargs['name'] = 'wire_{}_electrode_{}'.format(int(row.wire_num),int(row.electrode))
                ts_kwargs['electrodes'] = electrode_table_region
                ts = ElectricalSeries(**ts_kwargs)
                if ts.name not in lfp.electrical_series.keys():
                    lfp.add_electrical_series(ts)
            except IndexError:
                pass
        else:
            ts = TimeSeries(**ts_kwargs)
            if ts.name not in nwbfile.acquisition.keys():
                nwbfile.add_acquisition(ts)

            else:
                print('Failed to load: ',ts.name)

        ecephys_module = ProcessingModule(name='ecephys',
                                  description='preprocessed extracellular electrophysiology')
        nwbfile.create_processing_module(name='ecephys',
                                    description='preprocessed extracellular electrophysiology')
        nwbfile.processing['ecephys'].add(lfp)
        
    return nwbfile

def label_blockstart(df,threshold=300000, num_practice_trials=8, num_trials=15):
    labels = ['block_start']
    for i in np.arange(len(df.index.values))[1:-1]:
#         triplet = df.index.values[i-1:i+1]
        diff_prev = int(np.abs(df.index.values[i]-df.index.values[i-1]))
        diff_next = int(np.abs(df.index.values[i]-df.index.values[i+1]))
#         print([diff_prev, diff_next])
        if  diff_prev <= threshold or diff_next <= threshold:
            labels.append('block_start')
#         elif i<len(df.index.values) and  <= threshold:
#             labels.append('block_start')
        else:
            labels.append('trial_start')
    labels.append('trial_start')
    df['label'] = labels
    return df
