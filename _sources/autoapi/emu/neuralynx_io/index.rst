:py:mod:`emu.neuralynx_io`
==========================

.. py:module:: emu.neuralynx_io


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   emu.neuralynx_io.read_header
   emu.neuralynx_io.parse_header
   emu.neuralynx_io.read_records
   emu.neuralynx_io.estimate_record_count
   emu.neuralynx_io.parse_neuralynx_time_string
   emu.neuralynx_io.check_ncs_records
   emu.neuralynx_io.load_ncs
   emu.neuralynx_io.load_nev
   emu.neuralynx_io.nev_as_records



Attributes
~~~~~~~~~~

.. autoapisummary::

   emu.neuralynx_io.HEADER_LENGTH
   emu.neuralynx_io.NCS_SAMPLES_PER_RECORD
   emu.neuralynx_io.NCS_RECORD
   emu.neuralynx_io.NEV_RECORD
   emu.neuralynx_io.VOLT_SCALING
   emu.neuralynx_io.MILLIVOLT_SCALING
   emu.neuralynx_io.MICROVOLT_SCALING


.. py:data:: HEADER_LENGTH
   

   

.. py:data:: NCS_SAMPLES_PER_RECORD
   :annotation: = 512

   

.. py:data:: NCS_RECORD
   

   

.. py:data:: NEV_RECORD
   

   

.. py:data:: VOLT_SCALING
   :annotation: = [1, 'V']

   

.. py:data:: MILLIVOLT_SCALING
   :annotation: = [1000, 'mV']

   

.. py:data:: MICROVOLT_SCALING
   :annotation: = [1000000, 'µV']

   

.. py:function:: read_header(fid)


.. py:function:: parse_header(raw_hdr)


.. py:function:: read_records(fid, record_dtype, record_skip=0, count=None)


.. py:function:: estimate_record_count(file_path, record_dtype)


.. py:function:: parse_neuralynx_time_string(time_string)


.. py:function:: check_ncs_records(records)


.. py:function:: load_ncs(file_path, load_time=True, rescale_data=True, signal_scaling=MICROVOLT_SCALING)


.. py:function:: load_nev(file_path)


.. py:function:: nev_as_records(n)


