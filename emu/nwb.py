import os
import datetime
import numpy as np
import pandas as pd
import warnings
from tqdm import tqdm as tqdm
from . import neuralynx_io as nlx
from .neuralynx_io import nev_as_records

from pynwb import NWBFile, TimeSeries,NWBHDF5IO
from pynwb import TimeSeries, NWBFile,NWBHDF5IO
from pynwb.ecephys import ElectricalSeries
from pynwb.misc import AnnotationSeries

def ncs_to_timeseries(ncs,downsample=4):
    rate = float(ncs['sampling_rate'])

    ch = ncs['channel_number']
    if downsample:
        data = ncs['data'][::downsample]
        rate = rate/downsample
    else:
        data = ncs['data']

    ch_ts = TimeSeries(name='channel_{}'.format(ch),rate =rate, data=data.astype(np.float32),conversion=1.0/10**6,unit='V')
    return ch_ts

def nlx_to_nwb(nev_fp,ncs_paths,desc=''):
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
    print(n_blocks,' blocks')

    # ev['TimeStamp'] = ev.index.values/10**6 - start_time.timestamp()
    ev_ts = np.array([t.timestamp() for t in ev.time]) - start_time.timestamp()
#     start_stop = ev[ev.EventString.isin(['Starting Recording','Stopping Recording'])]
    
    events = AnnotationSeries(name='ttl', data=ev.label.values[:n_blocks*17], timestamps=ev_ts[:n_blocks*17])
    nwbfile.add_acquisition(events)
    
    for p in tqdm(ncs_paths):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                nwbfile.add_acquisition(ncs_to_timeseries(nlx.load_ncs(p)))
            except ValueError:
                print('Failed to load: ',os.path.split(p)[-1])
        
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
