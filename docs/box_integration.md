# emu Box SDK

## Accessing Box Data

To access data on the Box server you'll need to initialize/auth their client using jwt
I created a few helper methods to streamline this

```python

from src.auth import jwt
client = jwt()

# or if you want your credentials stored somewhere else
client = jwt('/path/to/config.json')
```

You can use the client to directly access files uploaded to box via the file's *file_id*. From the browser you can get this straight from the url in the form of app.box.com/file/<file_id>.
For instance if I wanted to work with [this file](https://app.box.com/file/562127657379):

```python

file_id = 562127657379

# This will grab a short summary of the file and is useful for checking if it exists and you have access
file = client.file(file_id)

# This will pull down the files full metadata
file_info = client.file(file_id).get()

# You can download the file using download_to
with open('/path/to/dir', 'wb') as directory:
    client.file(file_id).download_to(directory)

```

The client has a similar syntax for folders as well

```python
folder_id = 123456

# This will grab a short summary of the file and is useful for checking if it exists and you have access
folder = client.folder(folder_id)

# This will pull down the files full metadata
folder_info = client.folder(folder_id).get()
```
