import typer
import click_spinner
from tabulate import tabulate
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.object.collaboration import CollaborationRole
from tqdm.auto import tqdm
from .utils import get_file_type
from .auth import jwt

folder_app = typer.Typer()

@folder_app.command()
def list(id: int = typer.Argument(...)):
    print(tabulate(list(get_file_manifest(jwt().folder(id)))))

@folder_app.command()
def add_collaborator(id: int = typer.Argument(...),
                     role: CollaborationRole = CollaborationRole.EDITOR,
                     collaborator: str = typer.Argument(...,help='collaborator to add. May be a User, Group, or email address (unicode string)'),
                     notify: bool = False,
                     can_view_path: bool = False,
                    ):
    fold = jwt().folder(id)
    fold.get().add_collaborator(collaborator, role, notify=notify, can_view_path=can_view_path)
    typer.echo(list(fold.get().get_collaborations()))
    
def get_file_manifest(folder, prog_bar=False, **kwargs):
    folder = folder.get()

    # if parent is not None:
    #     parent = os.path.join(parent,folder.name)
    # else:
    #     parent = os.path.join('.')

    total_count = folder.item_collection['total_count']
    folder_name = folder.name
    
    for f in tqdm(folder.get_items(**kwargs),total=total_count,desc=folder_name):
        if isinstance(f,Folder):
            get_file_manifest(f)
            
        elif isinstance(f, File):
            ftype = get_file_type(f.name)
            rec = {
                    'filename':f.name,
                    'id':f.id,
                    # 'path':os.path.join(parent,f.name),
                    'type': ftype,
                    'folder': folder_name,
                }
            yield rec
        