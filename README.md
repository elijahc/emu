# EMU

## Installation
From command line clone the repository and/or navigate to its directory

```bash
$ git clone https://github.com/elijahc/emu

$ cd emu
```

Install the python requirements and packages
```bash
$ pip install -r requirements.txt
```

Install the optional jwt plugin
```bash
$ pip install boxsdk[jwt]
```

If you want systemwide access to the emu command line interface install the library using pip
```bash

$ pip install -e .

```

> The video preprocessing tools depend on ffmpeg, so make sure you have ffmpeg installed


> `sudo apt-get install ffmpeg`

## Access

In order to use the Box API you'll need a credentials file (Contact Elijah)

By default when you initialize the jwt client it will look for this file at ~/.emu/config.json but you can give it another path if you want to store the credentials somewhere else

## Usage

### emu Box SDK

#### Accessing Box Data

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

### Command Line Interface (CLI)

Several of the commonly used python functions have also been wrapped in a CLI for convenient access on the command line

You can access command line tools by either running the emu.py script...

```bash
$ python3 emu.py --help
Usage: emu.py [OPTIONS] COMMAND [ARGS]...

  Simple CLI for accessing emu data

Options:
  --help  Show this message and exit.

Commands:
  download
  info
  preprocess
```

...or, if the emu package was installed system-wide (see Installation), the `emu` cli tool is added to your `PATH`

```bash

$ pip install -e .

$ emu --help
Usage: emu [OPTIONS] COMMAND [ARGS]...

  Simple CLI for accessing emu data

Options:
  --help  Show this message and exit.

Commands:
  download
  info
  preprocess

```

#### Video Preprocessing

The preprocessing subcommand in the emu cli allows you to rescale resolution of video files and greyscale them.

```bash

$ emu preprocess --help
Usage: emu preprocess [OPTIONS]

Options:
  -i, --infile TEXT               Single file input. By default will write the
                                  output to the same dir as input file
  -r, --resolution [1080p|720p|360p]
                                  Resolution options for output video(s)
  -ss, --start INTEGER            Clip output video starting at ss (seconds)
  -e, --end INTEGER               Clip output video at end (seconds)
  --video_set [trickshots|deepfake]
                                  Video set to convert
  -d, --video_directory TEXT      Path to folder containing raw video files
  --verbose
  --help                          Show this message and exit.

```

Preprocess a single video to 360p starting at 8 seconds and ending at 15

```bash

$ emu preprocess -i ./Beckham.mp4 -r 360p -ss 8 -e 15
Converting @ 360p
	./Beckham.mp4 -> ./processed_Beckham.mp4(0'8" -> 0'15")

```

To rescale all trickshot videos to 360p, use the `--video_set` and `-d` options to specify source directory and which set of videos

```bash

$ emu preprocess -r 360p --video_set=trickshots -d ~/deepfake/videos/trickshots

Converting trickshots videos in /home/elijahc/deepfake/videos/trickshots @ 360p
	Beckham.mp4 -> /home/elijahc/deepfake/videos/trickshots/processed/1_Beckham.mp4(0'34" -> 0'39")
	Beckham.mp4 -> /home/elijahc/deepfake/videos/trickshots/processed/2_Beckham.mp4(0'40" -> 0'47")
	Beckham.mp4 -> /home/elijahc/deepfake/videos/trickshots/processed/3_Beckham.mp4(0'48" -> 0'57")
	Messi.mp4 -> /home/elijahc/deepfake/videos/trickshots/processed/4_Messi.mp4(0'12" -> 0'16")
	pogba.mp4 -> /home/elijahc/deepfake/videos/trickshots/processed/5_pogba.mp4(0'0" -> 0'10")
	DudePerfect_basketball.mp4 -> /home/elijahc/deepfake/videos/trickshots/processed/6_DudePerfect_basketball.mp4(0'21" -> 0'26")
	Soccer_Trick_Shots_2_DudePerfect.mp4 -> /home/elijahc/deepfake/videos/trickshots/processed/7_Soccer_Trick_Shots_2_DudePerfect.mp4(0'27" -> 0'30")
	Soccer_Trick_Shots_2_DudePerfect.mp4 -> /home/elijahc/deepfake/videos/trickshots/processed/8_Soccer_Trick_Shots_2_DudePerfect.mp4(0'73" -> 0'76")

```
