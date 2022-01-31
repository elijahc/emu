:py:mod:`emu.pipeline.process`
==============================

.. py:module:: emu.pipeline.process


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   emu.pipeline.process.PDilTask
   emu.pipeline.process.sEEGTask
   emu.pipeline.process.Downsample
   emu.pipeline.process.NWB



Functions
~~~~~~~~~

.. autoapisummary::

   emu.pipeline.process.gen_ncs



.. py:function:: gen_ncs(fp_list, ignore_warnings=True)


.. py:class:: PDilTask(*args, **kwargs)

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
      

      

   .. py:method:: patient_data(self)



.. py:class:: sEEGTask(*args, **kwargs)

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
      

      

   .. py:method:: ch_files(self, ch_ids)


   .. py:method:: sEEG_root(self)



.. py:class:: Downsample(*args, **kwargs)

   Bases: :py:obj:`sEEGTask`

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


   .. py:attribute:: channel_id
      

      

   .. py:attribute:: decimate
      

      

   .. py:method:: save_path(self)


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



.. py:class:: NWB(*args, **kwargs)

   Bases: :py:obj:`sEEGTask`

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


   .. py:attribute:: decimate
      

      

   .. py:method:: save_path(self)


   .. py:method:: requires(self)

      The Tasks that this Task depends on.

      A Task will only run if all of the Tasks that it requires are completed.
      If your Task does not require any other Tasks, then you don't need to
      override this method. Otherwise, a subclass can override this method
      to return a single Task, a list of Task instances, or a dict whose
      values are Task instances.

      See :ref:`Task.requires`


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


   .. py:method:: make_timeseries(self, ts_file, dat_file, ch)


   .. py:method:: run(self)

      The task run method, to be overridden in a subclass.

      See :ref:`Task.run`



