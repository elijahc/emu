import os
import datetime
import numpy as np
import pandas as pd
import sys
import warnings
from tqdm import tqdm as tqdm
from . import neuralynx_io as nlx
from .neuralynx_io import nev_as_records

from pynwb import NWBFile, TimeSeries,NWBHDF5IO
from pynwb import TimeSeries, NWBFile,NWBHDF5IO
from pynwb.ecephys import ElectricalSeries
from pynwb.misc import AnnotationSeries

def iter_ncs_to_timeseries(ncs_fps,data_time_len,dtype=np.float16,downsample=4):
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
                ncs = nlx.load_ncs(fp)
            except ValueError:
                print('Error loading {}'.format(os.path.split(fp)[-1]))
                print('skipping...')
        channel_ids.append(ncs['channel_number'])
        rates.append(float(int(ncs['sampling_rate']/downsample)))
        np_fps.append(os.path.join(d,name+'.npy'))
        n_samples = int(data_time_len*ncs['sampling_rate'])
        np.save(os.path.join(d,name),ncs['data'][:n_samples:downsample].astype(dtype))
        
    for fp,ch,rate in zip(np_fps,channel_ids,rates):
        
        # Load compressed data
        data = np.load(fp)
        
        ch_ts = TimeSeries(name='channel_{}'.format(ch),
                           rate=rate,
                           data=data,conversion=1.0/10**6,unit='V')
        yield ch_ts
        os.remove(fp)

def ncs_to_timeseries(ncs,downsample=4):
    rate = float(ncs['sampling_rate'])

    ch = ncs['channel_number']
    if downsample:
        data = ncs['data'][::downsample]
        rate = rate/downsample
    else:
        data = ncs['data']

    ch_ts = TimeSeries(name='channel_{}'.format(ch),rate =rate, data=data.astype(np.float16),conversion=1.0/10**6,unit='V')
    return ch_ts

def nlx_to_nwb(nev_fp,ncs_paths,desc='', trim_buffer=60*10, practice_incl=False):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ncs = nlx.load_ncs(ncs_paths.pop(0))
        nev = nlx.load_nev(nev_fp)

    uuid = nev['header']['SessionUUID']
    start_time = pd.to_datetime(ncs['time'][0],unit='us',utc=True).to_pydatetime()
    start_time_sec = start_time.timestamp()
    nwbfile = NWBFile(session_description=desc,
                      identifier=uuid,
                      session_start_time=start_time
                     )
    # ts = ncs_to_timeseries(ncs)
    nwbfile.add_acquisition(ncs_to_timeseries(ncs))
    
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
    
    for ts in iter_ncs_to_timeseries(ncs_paths,data_time_len):
        if ts.name not in nwbfile.acquisition.keys():
            nwbfile.add_acquisition(ts)
        else:
            print('Failed to load: ',ts.name)

    # for p in tqdm(ncs_paths):
    #     with warnings.catch_warnings():
    #         warnings.simplefilter("ignore")
        
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
