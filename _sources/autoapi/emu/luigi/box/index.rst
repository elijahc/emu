:py:mod:`emu.luigi.box`
=======================

.. py:module:: emu.luigi.box


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   emu.luigi.box.BoxClient
   emu.luigi.box.ReadableBoxFile
   emu.luigi.box.AtomicWritableBoxFile
   emu.luigi.box.BoxTarget



Functions
~~~~~~~~~

.. autoapisummary::

   emu.luigi.box.accept_trailing_slash_in_existing_dirpaths
   emu.luigi.box.accept_trailing_slash
   emu.luigi.box.obj_to_path
   emu.luigi.box.path_to_root
   emu.luigi.box.file_id_to_path
   emu.luigi.box.folder_id_to_path
   emu.luigi.box.path_to_obj
   emu.luigi.box.path_to_fid



Attributes
~~~~~~~~~~

.. autoapisummary::

   emu.luigi.box.DEFAULT_CONFIG_FP
   emu.luigi.box.logger


.. py:data:: DEFAULT_CONFIG_FP
   

   

.. py:data:: logger
   

   

.. py:function:: accept_trailing_slash_in_existing_dirpaths(func)


.. py:function:: accept_trailing_slash(func)


.. py:class:: BoxClient(path_to_config=DEFAULT_CONFIG_FP, user_agent='Luigi')

   Bases: :py:obj:`luigi.target.FileSystem`

   Box client for authentication, designed to be used by the :py:class:`BoxTarget` class.

   .. py:method:: file(self, fid)


   .. py:method:: folder(self, fid)


   .. py:method:: file_id_to_path(self, fid)


   .. py:method:: path_to_fid(self, path)


   .. py:method:: exists(self, path)

      Return ``True`` if file or directory at ``path`` exist, ``False`` otherwise

      :param str path: a path within the FileSystem to check for existence.


   .. py:method:: isdir(self, path)

      Return ``True`` if the location at ``path`` is a directory. If not, return ``False``.

      :param str path: a path within the FileSystem to check as a directory.

      *Note*: This method is optional, not all FileSystem subclasses implements it.


   .. py:method:: mkdir(self, path, parents=True, raise_if_exists=False)

      Create directory at location ``path``

      Creates the directory at ``path`` and implicitly create parent
      directories if they do not already exist.

      :param str path: a path within the FileSystem to create as a directory.
      :param bool parents: Create parent directories when necessary. When
                           parents=False and the parent directory doesn't
                           exist, raise luigi.target.MissingParentDirectory
      :param bool raise_if_exists: raise luigi.target.FileAlreadyExists if
                                   the folder already exists.


   .. py:method:: remove(self, path, recursive=True, skip_trash=True)

      Remove file or directory at location ``path``

      :param str path: a path within the FileSystem to remove.
      :param bool recursive: if the path is a directory, recursively remove the directory and all
                             of its descendants. Defaults to ``True``.


   .. py:method:: download_as_bytes(self, fid)


   .. py:method:: upload(self, folder_path, local_path)


   .. py:method:: _exists_and_is_dir(self, path)

      Auxiliary method, used by the 'accept_trailing_slash' and 'accept_trailing_slash_in_existing_dirpaths' decorators
      :param path: a Dropbox path that does NOT ends with a '/' (even if it is a directory)



.. py:class:: ReadableBoxFile(file_id, client)

   Bases: :py:obj:`object`

   Represents a file inside the Box cloud which will be read

   .. py:method:: read(self)


   .. py:method:: download_to_tmp(self)


   .. py:method:: __enter__(self)


   .. py:method:: __exit__(self, exc_type, exc, traceback)


   .. py:method:: __del__(self)


   .. py:method:: close(self)


   .. py:method:: readable(self)


   .. py:method:: writable(self)


   .. py:method:: seekable(self)



.. py:class:: AtomicWritableBoxFile(path, client)

   Bases: :py:obj:`luigi.target.AtomicLocalFile`

   Represents a file that will be created inside the Box cloud

   :param str path: Destination path inside Box cloud
   :param BoxClient client: a BoxClient object (initialized with a valid token, for the desired account)

   .. py:method:: move_to_final_destination(self)

      After editing the file locally, this function uploads it to the Dropbox cloud



.. py:function:: obj_to_path(obj)


.. py:function:: path_to_root(obj)


.. py:function:: file_id_to_path(file_id, client=None)


.. py:function:: folder_id_to_path(folder_id, client=None)


.. py:function:: path_to_obj(client, path)


.. py:function:: path_to_fid(path, client)


.. py:class:: BoxTarget(path=None, file_id=None, auth_config=DEFAULT_CONFIG_FP, format=None, user_agent='Luigi')

   Bases: :py:obj:`luigi.target.FileSystemTarget`

   Base class for FileSystem Targets like :class:`~luigi.local_target.LocalTarget` and :class:`~luigi.contrib.hdfs.HdfsTarget`.

   A FileSystemTarget has an associated :py:class:`FileSystem` to which certain operations can be
   delegated. By default, :py:meth:`exists` and :py:meth:`remove` are delegated to the
   :py:class:`FileSystem`, which is determined by the :py:attr:`fs` property.

   Methods of FileSystemTarget raise :py:class:`FileSystemException` if there is a problem
   completing the operation.

   Usage:
       .. code-block:: python

           target = FileSystemTarget('~/some_file.txt')
           target = FileSystemTarget(pathlib.Path('~') / 'some_file.txt')
           target.exists()  # False

   .. py:method:: fs(self)
      :property:

      The :py:class:`FileSystem` associated with this FileSystemTarget.


   .. py:method:: temporary_path(self)

      A context manager that enables a reasonably short, general and
      magic-less way to solve the :ref:`AtomicWrites`.

       * On *entering*, it will create the parent directories so the
         temporary_path is writeable right away.
         This step uses :py:meth:`FileSystem.mkdir`.
       * On *exiting*, it will move the temporary file if there was no exception thrown.
         This step uses :py:meth:`FileSystem.rename_dont_move`

      The file system operations will be carried out by calling them on :py:attr:`fs`.

      The typical use case looks like this:

      .. code:: python

          class MyTask(luigi.Task):
              def output(self):
                  return MyFileSystemTarget(...)

              def run(self):
                  with self.output().temporary_path() as self.temp_output_path:
                      run_some_external_command(output_path=self.temp_output_path)


   .. py:method:: temporary_file(self)


   .. py:method:: open(self, mode)

      Open the FileSystem target.

      This method returns a file-like object which can either be read from or written to depending
      on the specified mode.

      :param str mode: the mode `r` opens the FileSystemTarget in read-only mode, whereas `w` will
                       open the FileSystemTarget in write mode. Subclasses can implement
                       additional options. Using `b` is not supported; initialize with
                       `format=Nop` instead.



