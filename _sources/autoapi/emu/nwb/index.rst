:py:mod:`emu.nwb`
=================

.. py:module:: emu.nwb


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   emu.nwb.get_channel_id
   emu.nwb.iter_ncs_to_timeseries
   emu.nwb.ncs_to_timeseries
   emu.nwb.add_electrodes
   emu.nwb.nev_to_behavior_annotation
   emu.nwb.initialize_nwb
   emu.nwb.add_ttl
   emu.nwb.ncs_to_grp_eseries
   emu.nwb.ncs_to_nwb_raw
   emu.nwb.ncs_to_nwb
   emu.nwb.nlx_to_nwb
   emu.nwb.label_blockstart



.. py:function:: get_channel_id(fp)


.. py:function:: iter_ncs_to_timeseries(ncs_fps, data_time_len=None, dtype=np.float16, fs=4000, electrode_locations=None)


.. py:function:: ncs_to_timeseries(ncs, data_time_len=None, fs=1000, dtype=np.float16)


.. py:function:: add_electrodes(nwb, trodes, device, group_col='wire_num')


.. py:function:: nev_to_behavior_annotation(nev_fp, practice_incl=False)


.. py:function:: initialize_nwb(ncs_paths, desc='', lab='Thompson Lab', institution='University of Colorado Anschutz')


.. py:function:: add_ttl(nwbfile, nev_fp)


.. py:function:: ncs_to_grp_eseries(grp, electrode_locations, nwbfile, data_time_len=None, dtype=np.float32, fs=None)


.. py:function:: ncs_to_nwb_raw(ncs_paths, desc='', lab='Thompson Lab', institution='University of Colorado Anschutz', nev_fp=None, fs=None, electrode_locations=None)


.. py:function:: ncs_to_nwb(ncs_paths, desc='', nev_path=None, electrode_locations=None, lab='Thompson Lab', institution='University of Colorado Anschutz', trim_buffer=60 * 10)

   Create NWB file from neuralynx data file paths and electrode locations map


.. py:function:: nlx_to_nwb(nev_fp, ncs_paths, desc='', trim_buffer=60 * 10, practice_incl=False, electrode_locations=None)


.. py:function:: label_blockstart(df, threshold=300000, num_practice_trials=8, num_trials=15)


