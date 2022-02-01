:py:mod:`emu.pipeline.remote`
=============================

.. py:module:: emu.pipeline.remote


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   emu.pipeline.remote.RemoteFile
   emu.pipeline.remote.RemoteCSV
   emu.pipeline.remote.RemoteNLX
   emu.pipeline.remote.RemotePatientManifest
   emu.pipeline.remote.RemoteStudyManifest




Attributes
~~~~~~~~~~

.. autoapisummary::

   emu.pipeline.remote.Patients


.. py:class:: RemoteFile(*args, **kwargs)

   Bases: :py:obj:`luigi.ExternalTask`

   :param file_id:
   :type file_id: int
   :param file_path:
   :type file_path: str

   .. py:attribute:: file_id
      

      

   .. py:attribute:: file_path
      

      

   .. py:method:: output(self)

      The output that this Task produces.

      The output of the Task determines if the Task needs to be run--the task
      is considered finished iff the outputs all exist. Subclasses should
      override this method to return a single :py:class:`Target` or a list of
      :py:class:`Target` instances.

      Implementation note
        If running multiple workers, the output must be a resource that is accessible
        by all workers, such as a DFS or database. Otherwise, workers might compute
        the same output since they don't see the work done by other workers.

      See :ref:`Task.output`



.. py:class:: RemoteCSV(*args, **kwargs)

   Bases: :py:obj:`RemoteFile`

   :param file_id:
   :type file_id: int
   :param file_path:
   :type file_path: str

   .. py:attribute:: file_id
      

      

   .. py:attribute:: file_path
      

      

   .. py:method:: load(self, parse_func=pd.read_csv, force=False)

      :param parse_func: Default is pd.read_csv
      :type parse_func: func
      :param force: Force a reload from the server, Default is False
      :type force: bool


   .. py:method:: append(self, row)


   .. py:method:: commit(self)



.. py:class:: RemoteNLX(*args, **kwargs)

   Bases: :py:obj:`RemoteFile`

   :param file_id:
   :type file_id: int
   :param file_path:
   :type file_path: str

   .. py:attribute:: file_id
      

      

   .. py:method:: raw_header(self)


   .. py:method:: header(self)



.. py:class:: RemotePatientManifest(*args, **kwargs)

   Bases: :py:obj:`RemoteCSV`

   :param file_id:
   :type file_id: int
   :param file_path:
   :type file_path: str

   .. py:method:: output(self)

      The output that this Task produces.

      The output of the Task determines if the Task needs to be run--the task
      is considered finished iff the outputs all exist. Subclasses should
      override this method to return a single :py:class:`Target` or a list of
      :py:class:`Target` instances.

      Implementation note
        If running multiple workers, the output must be a resource that is accessible
        by all workers, such as a DFS or database. Otherwise, workers might compute
        the same output since they don't see the work done by other workers.

      See :ref:`Task.output`


   .. py:method:: register_folder(self, firstname, lastname, study, data_type, folder_id=None, path=None, patient_order=0)


   .. py:method:: generate_id(self, firstname, lastname)


   .. py:method:: register_study_root(self, firstname, lastname, study, folder_id=None, path=None, order=0)



.. py:class:: RemoteStudyManifest(*args, **kwargs)

   Bases: :py:obj:`RemoteCSV`

   :param file_id:
   :type file_id: int
   :param file_path:
   :type file_path: str

   .. py:attribute:: study
      

      

   .. py:method:: requires(self)

      The Tasks that this Task depends on.

      A Task will only run if all of the Tasks that it requires are completed.
      If your Task does not require any other Tasks, then you don't need to
      override this method. Otherwise, a subclass can override this method
      to return a single Task, a list of Task instances, or a dict whose
      values are Task instances.

      See :ref:`Task.requires`


   .. py:method:: create(self)


   .. py:method:: output(self)

      The output that this Task produces.

      The output of the Task determines if the Task needs to be run--the task
      is considered finished iff the outputs all exist. Subclasses should
      override this method to return a single :py:class:`Target` or a list of
      :py:class:`Target` instances.

      Implementation note
        If running multiple workers, the output must be a resource that is accessible
        by all workers, such as a DFS or database. Otherwise, workers might compute
        the same output since they don't see the work done by other workers.

      See :ref:`Task.output`



.. py:data:: Patients
   

   

