:py:mod:`emu.utils`
===================

.. py:module:: emu.utils


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   emu.utils.Experiment



Functions
~~~~~~~~~

.. autoapisummary::

   emu.utils.create_or_reuse_client
   emu.utils.get_file_type
   emu.utils.load_patients
   emu.utils.get_file_manifest
   emu.utils.md5_16
   emu.utils.generate_id
   emu.utils.is_url



Attributes
~~~~~~~~~~

.. autoapisummary::

   emu.utils.DEFAULT_MANIFEST_FID
   emu.utils.RELEVANT_FILES
   emu.utils._parse_ch
   emu.utils._get_ch
   emu.utils._get_block
   emu.utils.channel_fn_rgx


.. py:data:: DEFAULT_MANIFEST_FID
   :annotation: = 588757437066

   

.. py:data:: RELEVANT_FILES
   

   

.. py:data:: _parse_ch
   

   

.. py:data:: _get_ch
   

   

.. py:data:: _get_block
   

   

.. py:data:: channel_fn_rgx
   :annotation: = CSC(?P<channel>[0-9]+)(?P<block>_[0-9]{4})?\.ncs

   

.. py:function:: create_or_reuse_client(client)


.. py:function:: get_file_type(filename, relevant_files=RELEVANT_FILES)


.. py:function:: load_patients()


.. py:function:: get_file_manifest(folder, prog_bar=False, **kwargs)


.. py:function:: md5_16(*args)


.. py:function:: generate_id(firstname, lastname)


.. py:function:: is_url(url)


.. py:class:: Experiment(study, patient_id, client=None, pt_manifest_file_id=None)

   Bases: :py:obj:`object`

   .. py:method:: __repr__(self)

      Return repr(self).


   .. py:method:: files(self)


   .. py:method:: load_channels(self)



