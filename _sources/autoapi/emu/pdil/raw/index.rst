:py:mod:`emu.pdil.raw`
======================

.. py:module:: emu.pdil.raw


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   emu.pdil.raw.Electrophysiology
   emu.pdil.raw.Participant



Functions
~~~~~~~~~

.. autoapisummary::

   emu.pdil.raw.points_to_choice
   emu.pdil.raw.taskoutput_meta
   emu.pdil.raw.timestamps
   emu.pdil.raw.extract_trial_timing
   emu.pdil.raw.get_data_manifest



Attributes
~~~~~~~~~~

.. autoapisummary::

   emu.pdil.raw.PAYOFF_DICT


.. py:data:: PAYOFF_DICT
   

   

.. py:function:: points_to_choice(pts)


.. py:function:: taskoutput_meta(filename, rgx_string='blockNum_(\\d+)_(\\w+)TT_(\\w+)_taskoutput.mat')


.. py:function:: timestamps(filename, var_key='taskoutput')


.. py:function:: extract_trial_timing(filename, struct_as_record=False)


.. py:class:: Electrophysiology(patient_id, box_files, raw_path=None)

   Bases: :py:obj:`object`

   .. py:method:: gen_nlx_chunks(self)


   .. py:method:: load_all_nev(self)


   .. py:method:: events(self, index=None)


   .. py:method:: ttl(self)


   .. py:method:: to_nwb(self, ncs_paths, nev_fp=None)



.. py:class:: Participant(patient_id, raw_files, seeg_raw_path=None, sex=None, species='human')

   Bases: :py:obj:`object`

   .. py:method:: cache_behavior(self, verbose=False)

      :Yields: *luigi.Task* -- Yields a BehaviorRaw task for downloading a single behavior file


   .. py:method:: cache_nev(self, study='pdil', verbose=False)

      :Yields: *luigi.Task* -- Yields a NLXRaw task for downloading a single nev file from box


   .. py:method:: cache_ncs(self, study='pdil', verbose=False)

      :Yields: *luigi.Task* -- Yields a NLXRaw task for downloading a single ncs file from box


   .. py:method:: load_game_data(self, local_scheduler=False)


   .. py:method:: load_pdil_events(self, local_scheduler=False)


   .. py:method:: create_nwb(self, nev_fp, ncs_fps, blocks, desc='')


   .. py:method:: add_behavior(self, nev_fp, blocks, practice_incl=None)



.. py:function:: get_data_manifest(study='pdil')


