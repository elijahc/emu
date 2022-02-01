:py:mod:`emu.pipeline.download`
===============================

.. py:module:: emu.pipeline.download


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   emu.pipeline.download.FileManifest
   emu.pipeline.download.CacheData
   emu.pipeline.download.CacheTaskOutput
   emu.pipeline.download.PatientsLocal
   emu.pipeline.download.Raw
   emu.pipeline.download.BehaviorRaw
   emu.pipeline.download.NLXRaw
   emu.pipeline.download.ExperimentManifest
   emu.pipeline.download.CollectionBuilder



Functions
~~~~~~~~~

.. autoapisummary::

   emu.pipeline.download.sha1
   emu.pipeline.download.check_or_create
   emu.pipeline.download.cache_fp



.. py:function:: sha1(filename)


.. py:function:: check_or_create(dir_path)


.. py:class:: FileManifest(*args, **kwargs)

   Bases: :py:obj:`luigi.Task`

   This is the base class of all Luigi Tasks, the base unit of work in Luigi.

   A Luigi Task describes a unit or work.

   The key methods of a Task, which must be implemented in a subclass are:

   * :py:meth:`run` - the computation done by this task.
   * :py:meth:`requires` - the list of Tasks that this Task depends on.
   * :py:meth:`output` - the output :py:class:`Target` that this Task creates.

   Each :py:class:`~luigi.Parameter` of the Task should be declared as members:

   .. code:: python

       class MyTask(luigi.Task):
           count = luigi.IntParameter()
           second_param = luigi.Parameter()

   In addition to any declared properties and methods, there are a few
   non-declared properties, which are created by the :py:class:`Register`
   metaclass:


   .. py:attribute:: patient_id
      

      

   .. py:attribute:: data_root
      

      

   .. py:method:: requires(self)

      The Tasks that this Task depends on.

      A Task will only run if all of the Tasks that it requires are completed.
      If your Task does not require any other Tasks, then you don't need to
      override this method. Otherwise, a subclass can override this method
      to return a single Task, a list of Task instances, or a dict whose
      values are Task instances.

      See :ref:`Task.requires`


   .. py:method:: run(self)

      The task run method, to be overridden in a subclass.

      See :ref:`Task.run`


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



.. py:class:: CacheData(*args, **kwargs)

   Bases: :py:obj:`luigi.Task`

   This is the base class of all Luigi Tasks, the base unit of work in Luigi.

   A Luigi Task describes a unit or work.

   The key methods of a Task, which must be implemented in a subclass are:

   * :py:meth:`run` - the computation done by this task.
   * :py:meth:`requires` - the list of Tasks that this Task depends on.
   * :py:meth:`output` - the output :py:class:`Target` that this Task creates.

   Each :py:class:`~luigi.Parameter` of the Task should be declared as members:

   .. code:: python

       class MyTask(luigi.Task):
           count = luigi.IntParameter()
           second_param = luigi.Parameter()

   In addition to any declared properties and methods, there are a few
   non-declared properties, which are created by the :py:class:`Register`
   metaclass:


   .. py:attribute:: patient_id
      

      

   .. py:attribute:: data_root
      

      

   .. py:method:: requires(self)

      The Tasks that this Task depends on.

      A Task will only run if all of the Tasks that it requires are completed.
      If your Task does not require any other Tasks, then you don't need to
      override this method. Otherwise, a subclass can override this method
      to return a single Task, a list of Task instances, or a dict whose
      values are Task instances.

      See :ref:`Task.requires`



.. py:class:: CacheTaskOutput(*args, **kwargs)

   Bases: :py:obj:`CacheData`

   This is the base class of all Luigi Tasks, the base unit of work in Luigi.

   A Luigi Task describes a unit or work.

   The key methods of a Task, which must be implemented in a subclass are:

   * :py:meth:`run` - the computation done by this task.
   * :py:meth:`requires` - the list of Tasks that this Task depends on.
   * :py:meth:`output` - the output :py:class:`Target` that this Task creates.

   Each :py:class:`~luigi.Parameter` of the Task should be declared as members:

   .. code:: python

       class MyTask(luigi.Task):
           count = luigi.IntParameter()
           second_param = luigi.Parameter()

   In addition to any declared properties and methods, there are a few
   non-declared properties, which are created by the :py:class:`Register`
   metaclass:


   .. py:method:: run(self)

      The task run method, to be overridden in a subclass.

      See :ref:`Task.run`


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



.. py:class:: PatientsLocal(*args, **kwargs)

   Bases: :py:obj:`luigi.Task`

   This is the base class of all Luigi Tasks, the base unit of work in Luigi.

   A Luigi Task describes a unit or work.

   The key methods of a Task, which must be implemented in a subclass are:

   * :py:meth:`run` - the computation done by this task.
   * :py:meth:`requires` - the list of Tasks that this Task depends on.
   * :py:meth:`output` - the output :py:class:`Target` that this Task creates.

   Each :py:class:`~luigi.Parameter` of the Task should be declared as members:

   .. code:: python

       class MyTask(luigi.Task):
           count = luigi.IntParameter()
           second_param = luigi.Parameter()

   In addition to any declared properties and methods, there are a few
   non-declared properties, which are created by the :py:class:`Register`
   metaclass:


   .. py:attribute:: file_id
      

      

   .. py:attribute:: data_root
      

      

   .. py:method:: run(self)

      The task run method, to be overridden in a subclass.

      See :ref:`Task.run`


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



.. py:class:: Raw(*args, **kwargs)

   Bases: :py:obj:`luigi.Task`

   This is the base class of all Luigi Tasks, the base unit of work in Luigi.

   A Luigi Task describes a unit or work.

   The key methods of a Task, which must be implemented in a subclass are:

   * :py:meth:`run` - the computation done by this task.
   * :py:meth:`requires` - the list of Tasks that this Task depends on.
   * :py:meth:`output` - the output :py:class:`Target` that this Task creates.

   Each :py:class:`~luigi.Parameter` of the Task should be declared as members:

   .. code:: python

       class MyTask(luigi.Task):
           count = luigi.IntParameter()
           second_param = luigi.Parameter()

   In addition to any declared properties and methods, there are a few
   non-declared properties, which are created by the :py:class:`Register`
   metaclass:


   .. py:attribute:: __name__
      :annotation: = Raw

      

   .. py:attribute:: data_root
      

      

   .. py:attribute:: file_id
      

      

   .. py:attribute:: file_name
      

      

   .. py:attribute:: save_to
      

      

   .. py:attribute:: overwrite
      

      

   .. py:method:: __repr__(self)

      Build a task representation like `MyTask(param1=1.5, param2='5')`


   .. py:method:: out_dir(self)


   .. py:method:: is_intact(self)


   .. py:method:: get_client(self)


   .. py:method:: download(self)


   .. py:method:: run(self)

      The task run method, to be overridden in a subclass.

      See :ref:`Task.run`


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



.. py:function:: cache_fp(data_root, study, patient_id, data_type=None)


.. py:class:: BehaviorRaw(*args, **kwargs)

   Bases: :py:obj:`Raw`

   This is the base class of all Luigi Tasks, the base unit of work in Luigi.

   A Luigi Task describes a unit or work.

   The key methods of a Task, which must be implemented in a subclass are:

   * :py:meth:`run` - the computation done by this task.
   * :py:meth:`requires` - the list of Tasks that this Task depends on.
   * :py:meth:`output` - the output :py:class:`Target` that this Task creates.

   Each :py:class:`~luigi.Parameter` of the Task should be declared as members:

   .. code:: python

       class MyTask(luigi.Task):
           count = luigi.IntParameter()
           second_param = luigi.Parameter()

   In addition to any declared properties and methods, there are a few
   non-declared properties, which are created by the :py:class:`Register`
   metaclass:


   .. py:attribute:: __name__
      :annotation: = BehaviorRaw

      

   .. py:attribute:: study
      

      

   .. py:attribute:: patient_id
      

      

   .. py:method:: cache_fp(self, data_type)


   .. py:method:: out_dir(self)



.. py:class:: NLXRaw(*args, **kwargs)

   Bases: :py:obj:`Raw`

   This is the base class of all Luigi Tasks, the base unit of work in Luigi.

   A Luigi Task describes a unit or work.

   The key methods of a Task, which must be implemented in a subclass are:

   * :py:meth:`run` - the computation done by this task.
   * :py:meth:`requires` - the list of Tasks that this Task depends on.
   * :py:meth:`output` - the output :py:class:`Target` that this Task creates.

   Each :py:class:`~luigi.Parameter` of the Task should be declared as members:

   .. code:: python

       class MyTask(luigi.Task):
           count = luigi.IntParameter()
           second_param = luigi.Parameter()

   In addition to any declared properties and methods, there are a few
   non-declared properties, which are created by the :py:class:`Register`
   metaclass:


   .. py:attribute:: __name__
      :annotation: = NLXRaw

      

   .. py:attribute:: study
      

      

   .. py:attribute:: patient_id
      

      

   .. py:method:: cache_fp(self, data_type)


   .. py:method:: out_dir(self)



.. py:class:: ExperimentManifest(*args, **kwargs)

   Bases: :py:obj:`luigi.Task`

   This is the base class of all Luigi Tasks, the base unit of work in Luigi.

   A Luigi Task describes a unit or work.

   The key methods of a Task, which must be implemented in a subclass are:

   * :py:meth:`run` - the computation done by this task.
   * :py:meth:`requires` - the list of Tasks that this Task depends on.
   * :py:meth:`output` - the output :py:class:`Target` that this Task creates.

   Each :py:class:`~luigi.Parameter` of the Task should be declared as members:

   .. code:: python

       class MyTask(luigi.Task):
           count = luigi.IntParameter()
           second_param = luigi.Parameter()

   In addition to any declared properties and methods, there are a few
   non-declared properties, which are created by the :py:class:`Register`
   metaclass:


   .. py:attribute:: data_root
      

      

   .. py:attribute:: study
      

      

   .. py:attribute:: file_name
      

      

   .. py:method:: out_dir(self)


   .. py:method:: requires(self)

      The Tasks that this Task depends on.

      A Task will only run if all of the Tasks that it requires are completed.
      If your Task does not require any other Tasks, then you don't need to
      override this method. Otherwise, a subclass can override this method
      to return a single Task, a list of Task instances, or a dict whose
      values are Task instances.

      See :ref:`Task.requires`


   .. py:method:: create(self)


   .. py:method:: run(self)

      The task run method, to be overridden in a subclass.

      See :ref:`Task.run`


   .. py:method:: load(self, force=False)


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



.. py:class:: CollectionBuilder(study, data_root=None)

   Bases: :py:obj:`object`

   .. py:method:: from_dataframe(cls, df, study, data_root=None)
      :classmethod:


   .. py:method:: _create_seeg_path(self, patient_id, study=None)


   .. py:method:: gen_ncs(self)

      :Yields: *luigi.Task* -- Yields a NLXRaw task for downloading a single ncs file from box


   .. py:method:: nev(self)

      :Yields: *luigi.Task* -- Yields a NLXRaw task for downloading a single ncs file from box


   .. py:method:: clean(self, jobs, dry_run=False)



