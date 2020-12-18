import os
import datetime
import numpy as np
import pandas as pd
import sys
import warnings
from tqdm import tqdm as tqdm
from . import neuralynx_io as nlx
from .neuralynx_io import nev_as_records,load_nev

from pynwb import NWBFile, TimeSeries,NWBHDF5IO
from pynwb import TimeSeries, NWBFile,NWBHDF5IO
from pynwb.ecephys import ElectricalSeries,LFP
from pynwb.misc import AnnotationSeries

def iter_ncs_to_timeseries(ncs_fps,data_time_len,dtype=np.float16,downsample=4,electrode_locations=None):
    channel_ids = []
    np_fps = []
    rates = []
    
    # Write all numpy files, then iter again yielding timeseries
    for fp in tqdm(ncs_fps,desc='compressing channels'):
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
        rates.append(float(int(ncs['sampling_rate']/downsample)))
        np_fps.append(os.path.join(d,name+'.npy'))
        n_samples = int(data_time_len*ncs['sampling_rate'])
        np.save(os.path.join(d,name),ncs['data'][:n_samples:downsample].astype(dtype))
        
    for fp,ch,rate in zip(np_fps,channel_ids,rates):
        
        # Load compressed data
        data = np.load(fp)
        
        ts_kwargs = {
            'name':'channel_{}'.format(int(ch)),
            'rate':rate,
            'data':data.astype(np.float16),
            'conversion':1.0/10**6,
            'comments': ncs['header']['AcqEntName']
        }

        yield ch,ts_kwargs
        os.remove(fp)

def ncs_to_timeseries(ncs,data_time_len,downsample=4):
    rate = float(ncs['sampling_rate'])

    # Use AcqEntName instead of channel_number to infer channel
    ch = ncs['channel_number']
    # ch = int(ncs['header']['AcqEntName'][3:])
    n_samples = int(data_time_len*rate)
    if downsample:
        data = ncs['data'][:n_samples:downsample]
        rate = rate/downsample
    else:
        data = ncs['data']

    # ch_ts = TimeSeries(name='channel_{}'.format(ch),rate =rate, data=data.astype(np.float16),conversion=1.0/10**6,unit='V')
    ts_kwargs = {
        'name': 'channel_{}'.format(ch+1),
        'rate':rate,
        'data':data.astype(np.float16),
        'conversion':1.0/10**6,
        'comments': ncs['header']['AcqEntName']
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

def ncs_to_nwb(ncs_paths,
                desc='',
                nev_path=None,
                electrode_locations=None,
                lab='Thompson Lab',
                institution='University of Colorado Anschutz',
                trim_buffer=60*10,
                ):
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

    dev = nwbfile.create_device(name='Neuralynx')
    # ts = ncs_to_timeseries(ncs)

    if electrode_locations is not None:
        add_electrodes(nwbfile,electrode_locations,dev)

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
    else:
        data_time_len = len(ncs['data'])/int(ncs['sampling_rate'])

    ncs_paths.append(first_ncs)
    lfp = LFP(name='LFP')

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
                else:
                    print('Failed to load: ',ts.name)
            except IndexError:
                pass
        else:
            ts = TimeSeries(**ts_kwargs)
            if ts.name not in nwbfile.acquisition.keys():
                nwbfile.add_acquisition(ts)
            else:
                print('Failed to load: ',ts.name)

    nwbfile.create_processing_module(name='ecephys',
                                description='preprocessed extracellular electrophysiology')
    nwbfile.processing['ecephys'].add(lfp)
        
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
