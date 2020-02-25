# from .auth import Auth
from .process_videos import process, records, trickshots, resolution_presets
import click
import yaml

# with open(r'box_index.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
#     BOX_METADATA = yaml.load(file)

#     print(BOX_METADATA)

@click.group()
def main():
    """
    Simple CLI for accessing emu data
    """
    pass

@main.command()
@click.argument('fileid')
@click.option('--verbose', is_flag=True, default=False, help='Print debugging info')
def download(fileid,verbose):
    if verbose == True:
        click.echo("{}".format(fileid))

@main.command()
@click.option('-i', '--infile', type=str, help='Single file input. By default will write the output to the same dir as input file')
@click.option('-r', '--resolution', default='360p', type=click.Choice(list(resolution_presets.keys())), help='Resolution options for output video(s)')
@click.option('-ss', '--start', default=0, type=int, help='Clip output video starting at ss (seconds)')
@click.option('-e', '--end', type=int, help='Clip output video at end (seconds)')
@click.option('--video_set', type=click.Choice(['trickshots','deepfake']), help='Video set to convert')
@click.option('-d', '--video_directory', default='./', help='Path to folder containing raw video files')
@click.option('--verbose', is_flag=True, default=False)
def preprocess(*args, **kwargs):
    process(*args, **kwargs)

@main.command()
@click.option('--patient_id')
@click.option('--verbose', is_flag=True, default=False, help='Print debugging info')
def info(patient_id,verbose):
    client = Auth().jwt()

    print('patient_id: ',patient_id)

    folder_id = None
    for p in BOX_METADATA['patients']:
        if str(patient_id) == str(p['id']):
            folder_id = p['box_folder_id']

    if folder_id is not None:
        items = client.folder(folder_id).get_items()
        for item in items:
            print('{0} {1} is named "{2}"'.format(item.type.capitalize(), item.id, item.name))

if __name__ == "__main__":
    main()
    # FILEID = 562127657379

    # download(FILEID)
