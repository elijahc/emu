import click
import requests
from auth import Auth

@click.command()
@click.argument('file_id')
@click.option('--filename', default='dl_file.ns')
def dl_file(file_id, filename):
    client = Auth().jwt()
    file_info = client.file(file_id).get()
    print(file_info)

    try:
        file_content = client.file(file_id).content()

        print('writing file...')
        open(filename, 'wb').write(file_content)
    except:
        pass

    return file_info

if __name__ == "__main__":
    # FILEID = 562127657379
    dl_file()
