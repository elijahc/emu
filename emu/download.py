import requests
from auth import Auth

def dl_file(client, file_id, filename='dl_file.ns'):
    file_info = client.file(file_id).get()
    print(file_info)

    file_content = client.file(file_id).content()

    print('writing file...')
    open(filename, 'wb').write(file_content)
    return file_info

if __name__ == "__main__":

    FILEID = 562127657379

    client = Auth().jwt()

    file_info = dl_file(client, FILEID)
    print(file_info)
    # import ipdb; ipdb.set_trace()
