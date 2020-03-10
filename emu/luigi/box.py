import luigi.format
import logging
import ntpath
import os
import random
import tempfile
import time
import sys
from contextlib import contextmanager
from ..auth import jwt, DEFAULT_CONFIG
from luigi.target import FileSystem, FileSystemTarget, AtomicLocalFile
from boxsdk import JWTAuth, Client

if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

# TODO: Rename all instances of DEFAULT_CONFIG_FP to DEFAULT_CONFIG
DEFAULT_CONFIG_FP = DEFAULT_CONFIG

logger = logging.getLogger('luigi-interface')

def accept_trailing_slash_in_existing_dirpaths(func):
    @wraps(func)
    def wrapped(self, path, *args, **kwargs):
        if path != '/' and path.endswith('/'):
            logger.warning("Dropbox paths should NOT have trailing slashes. This causes additional API calls")
            logger.warning("Consider modifying your calls to {}, so that they don't use paths than end with '/'".format(func.__name__))

            if self._exists_and_is_dir(path[:-1]):
                path = path[:-1]

        return func(self, path, *args, **kwargs)

    return wrapped

def accept_trailing_slash(func):
    @wraps(func)
    def wrapped(self, path, *args, **kwargs):
        if path != '/' and path.endswith('/'):
            path = path[:-1]
        return func(self, path, *args, **kwargs)

    return wrapped

class BoxClient(FileSystem):
    """
    Box client for authentication, designed to be used by the :py:class:`BoxTarget` class.
    """

    def __init__(self, path_to_config=DEFAULT_CONFIG_FP, user_agent="Luigi"):
        """
        :param str path_to_config: path to Box JWT config.json file
        """
        if not path_to_config:
            raise ValueError("The path_to_config parameter must contain a valid Box JWT config.json file")

        self.path_to_config = path_to_config

        try:
            config = JWTAuth.from_settings_file(path_to_config)
            self.client = Client(config)
            self.conn = self.client
        except Exception as e:
            raise Exception("Cannot connect to Box. Check your Internet connection and the token. \n" + repr(e))

        self.token = path_to_config

    def file(self,fid):
        return self.conn.file(fid)

    def folder(self,fid):
        return self.conn.folder(fid)
    
    def file_id_to_path(self,fid):
        return file_id_to_path(file_id=fid,client=self.conn)

    def path_to_fid(self,path):
        return path_to_fid(client=self.conn,path=path)

    def exists(self, path):
        try:
            f = path_to_obj(self.client,path)
            if f.type in ['file','folder']:
                return True
        except ValueError as e:
            return False
        # Implement this

    def isdir(self, path):
        if path == '/':
            return True
        try:
            f = path_to_obj(self.conn,path)
            if f.type == 'folder':
                return isinstance(md, dropbox.files.FolderMetadata)
            else:
                return False
        except ValueError as e:
            raise e

    def mkdir(self, path, parents=True, raise_if_exists=False):
        parent_path, new_dir = os.path.split(path)
        print(parent_path)
        parent_folder = path_to_obj(self.conn, parent_path)
        try:
            f = path_to_obj(self.conn,path)
            if f.type is 'file':
                raise luigi.target.NotADirectory()
            elif raise_if_exists:
                raise luigi.target.FileAlreadyExists()
        except ValueError as e:
            print('Make folder!')

    def remove(self, path, recursive=True, skip_trash=True):
        if not self.exists(path):
            return False
        self.conn.files_delete_v2(path)
        return True

    def download_as_bytes(self, fid):
        # content = self.conn.file(fid).content()
        # if isinstance(content,str):
        #     content = unicode(content, 'utf-8')
        return self.conn.file(fid).content()

    def upload(self, folder_id, file_path):
        folder = self.conn.folder(folder_id).get()
        if os.path.exists(file_path):
            new_file = folder.upload(file_path)

class ReadableBoxFile(object):
    def __init__(self, file_id, client):
        """
        Represents a file inside the Dropbox cloud which will be read

        :param str path: Dropbpx path of the file to be read (always starting with /)
        :param DropboxClient client: a DropboxClient object (initialized with a valid token)

        """
        self.fid = file_id

        self.client = client
        self.path = self.client.file_id_to_path(file_id)
        self.download_file_location = os.path.join(tempfile.mkdtemp(prefix=str(time.time())),
                                                   ntpath.basename(self.path))
        self.closed = False

    def read(self):
        # content = self.client.download_as_bytes(self.fid)
        # print(content)
        byte_content =  self.client.download_as_bytes(self.fid)

        return byte_content

    def download_to_tmp(self):
        with open(self.download_file_location, 'w') as tmpfile:
            self.client.file(self.fid).download_to(tmpfile)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()

    def __del__(self):
        self.close()
        if os.path.exists(self.download_file_location):
            os.remove(self.download_file_location)

    def close(self):
        self.closed = True

    def readable(self):
        return True

    def writable(self):
        return False

    def seekable(self):
        return False

class AtomicWritableBoxFile(AtomicLocalFile):
    def __init__(self, path, client):
        """
        Represents a file that will be created inside the Dropbox cloud

        :param str path: Destination path inside Dropbox
        :param DropboxClient client: a DropboxClient object (initialized with a valid token, for the desired account)
        """
        super(AtomicWritableBoxFile, self).__init__(path)
        self.path = path
        self.client = client

        dir_path,_ = os.path.split(self.path)
        self.folder = path_to_obj(self.client,dir_path)

    def move_to_final_destination(self):
        """
        After editing the file locally, this function uploads it to the Dropbox cloud
        """
        self.client.upload(self.folder.id, self.path)

def file_id_to_path(file_id, client=None):
    if client is None:
        client = jwt()
    parent_dirs = []
    f = client.file(file_id).get()
    parent_path = f.path_collection['entries']
    parent_path = [folder.get().name for folder in parent_path[1:]]
    parent_dirs.extend(parent_path)
    path = '/'+'/'.join(parent_dirs)+'/'
    return path + f.name

def path_to_obj(client, path):
    target = path.split('/')[-1]
    results = client.search().query(query=target, limit=100,order='relevance')
    results = [f for f in results if f.name == target]
    for f in results:
        full_path = file_id_to_path(client=client,file_id=f.id)
        print(full_path)
        if full_path == path:
            return f

    # should never reach this point if you find it
    raise ValueError('Path not found:\n Path: {}'.format(path))

def path_to_fid(path,client):
    f = path_to_obj(path=path,client=client)
    return int(f.id)

class BoxTarget(FileSystemTarget):
    def __init__(self, path=None, file_id=None, auth_config=DEFAULT_CONFIG_FP, format=None, user_agent="Luigi"):
        super(BoxTarget, self).__init__(path)

        if not auth_config or not os.path.exists(auth_config):
            raise ValueError("The auth_config parameter must contain a valid path to a JWT config.json file")

        if path is None and file_id is None:
            raise ValueError("Must provide either path or file_id")
        self.path = path
        self.auth_config = auth_config
        self.client = BoxClient(auth_config, user_agent=user_agent)
        self.format = format or luigi.format.get_default_format()

        if file_id is not None and isinstance(file_id,int):
            self.fid = file_id
        else:
            self.fid = self.client.path_to_fid(path=self.path)

    @property
    def fs(self):
        return self.client

    @contextmanager
    def temporary_path(self):
        tmp_dir = tempfile.mkdtemp()
        num = random.randrange(0, 1e10)
        temp_path = '{}{}luigi-tmp-{:010}{}'.format(
            tmp_dir, os.sep,
            num, ntpath.basename(self.path))

        yield temp_path
        # We won't reach here if there was an user exception.
        self.fs.upload(temp_path, self.path)

    def open(self, mode):
        if mode not in ('r', 'w'):
            raise ValueError("Unsupported open mode '%s'" % mode)
        if mode == 'r':
            rbf = ReadableBoxFile(file_id=self.fid,client=self.client)
            return StringIO(str(rbf.read(), 'utf-8'))
            # return self.format.pipe_reader(ReadableBoxFile(self.fid, self.client))
            # fp = rbf.download_to_tmp()
            # print('downloading to:\n {}'.format(rbf.download_file_location))
            # return open(rbf.download_file_location, 'r')
        else:
            return self.format.pipe_reader(AtomicWritableBoxFile(self.path, self.client))
