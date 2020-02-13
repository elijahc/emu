# EMU

## Installation
From command line clone the repository and/or navigate to its directory

```bash
$ git clone https://github.com/elijahc/emu

$ cd emu
```

Install the python requirements
```bash
$ pip install -r requirements.txt
```

Install the optional jwt plugin
```bash
$ pip install boxsdk[jwt]
```

## Access

In order to use the Box API you'll need a credentials file (Contact Elijah)

By default when you initialize the jwt client it will look for this file at ~/.emu/config.json but you can give it another path if you want to store the credentials somewhere else

## Usage

### Video Preprocessing

The preprocessing subcommand in the emu cli allows you to rescale resolution of video files and greyscale them.
Make sure you have ffmpeg installed

```bash
$ sudo apt-get install ffmpeg
```

```bash
elijahc@hopper:~/emu$ python3 emu.py preprocess --help
Usage: emu.py preprocess [OPTIONS]

Options:
  -r, --resolution [1080p|720p|360p]
                                  Resolution options for output videos
  -s, --video_set [trickshots|deepfake]
                                  Video set to convert
  -d, --video_directory TEXT      Path to folder containing raw video files
  --verbose
  --help                          Show this message and exit.

```

Rescale trickshot videos to 360p

```bash

$ python3 emu.py preprocess  -r 360p -s trickshots -d ~/deepfake/videos/trickshots

```

### Accessing Box Data

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
