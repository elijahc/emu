:py:mod:`emu.pipeline.timestamps`
=================================

.. py:module:: emu.pipeline.timestamps


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   emu.pipeline.timestamps.ChannelTimestamp




.. py:class:: ChannelTimestamp(*args, **kwargs)

   Bases: :py:obj:`emu.pipeline.process.sEEGTask`

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



