import os
import glob
import requests
import pandas as pd
import numpy as np
from tqdm import tqdm as tqdm
import click

trickshots = [
    {
        'fname':'Beckham.mp4',
        'link':'https://v637g.app.goo.gl/PJuGYBvqsUApSmT86',
        'type':'fake',
    },{
        'fname':'Beckham.mp4',
        'link':'https://v637g.app.goo.gl/iPDhigC56j2YJwWR9',
        'type':'fake',
    },{
        'fname':'Beckham.mp4',
        'link':'https://v637g.app.goo.gl/6WmxWJSv1HPm3HCc7',
        'type':'fake',
    },{
        'fname':'Messi.mp4',
        'link':'https://v637g.app.goo.gl/wn5sEwRZCTKNtZiV8',
        'type':'fake',
    },{
        'fname':'pogba.mp4',
        'link':'https://v637g.app.goo.gl/tSXFHMYXuFWuFoDYA',
        'type':'fake',
    },{
        'fname':'DudePerfect_basketball.mp4',
        'link':'https://v637g.app.goo.gl/DanAUzSt5YVyookT8',
        'type':'fake',
    },{
        'fname':'Soccer_Trick_Shots_2_DudePerfect.mp4',
        'link':'https://v637g.app.goo.gl/ootJj8h4MBFkvEKs9',
        'type':'real',
    },{
        'fname':'Soccer_Trick_Shots_2_DudePerfect.mp4',
        'link':'https://v637g.app.goo.gl/iE2yrrk8EqL7dKPm6',
        'type':'real',
    },{
        'fname':'Drew_Brees_Edition_DP.mp4',
        'link':'https://v637g.app.goo.gl/oWrnVwfM1AmGwy2Q8',
        'type':'real',
    },{
        'fname':'Drew_Brees_Edition_DP.mp4',
        'link':'https://v637g.app.goo.gl/Vsr9R6EbEGkveR6T6',
        'type':'real',
    },{
        'fname':'World_Record_Edition_2_DudePerfect.mp4',
        'link':'https://v637g.app.goo.gl/UYWr93JfYcp7cz7C7',
        'type':'real',
    },{
        'fname':'World_Record_Edition_2_DudePerfect.mp4',
        'link':'https://v637g.app.goo.gl/s97rDmq9DkqriJ6DA',
        'type':'real',
    }
]

records = [
    {
        'fname':'Hader_ctrlshiftface.mp4',
        'link':'https://v637g.app.goo.gl/k4FqdJLbvhW7Yuow5',
        'type':'fake',

    },{
        'fname': 'Zucker.mp4',
#        'fid':615444233671,
#        'start':24,
#        'end':34,
        'link': 'https://v637g.app.goo.gl/2RzCLPbLWgtbgeXW6',
        'type': 'fake',
    },{
        'fname':'Obama_Peele.mp4',
        'link':'https://v637g.app.goo.gl/JQaLA1GD8ZhtmxAa9',
#        'fid':615445081594,
#        'start':8,
#        'end':15,
        'type':'fake',
    },{
        'fname':'Deepfake_Roundtable.mp4',
        'link':'https://youtu.be/l_6Tumd8EQI?t=896',
        'type':'fake',

    },{
        'fname':'Carson_note_360p.mp4',
        'link':'https://youtu.be/NtAE9Txmm4M?t=739',
        'type':'real',
    },{
        'fname':'Hader_ctrlshiftface.mp4',
        'link':'https://v637g.app.goo.gl/PH23hrjsJANfc1Ak6',
        'type':'real',

    },{
        'fname':'State_of_the_Union_2016.mp4',
        'link':'https://www.youtube.com/embed/OduMHTsRYFM?start=51&end=61&version=3',
        'type':'real',

    }
]

resolution_presets = {
        '1080p': {'b:v':'4500k','minrate':'4500k', 'maxrate':'9000k', 'bufsize':'9000k', 'vf': '\"scale=-1:1080, hue=s=0\"'},    
        '720p': {'b:v':'2500k','minrate':'1500k', 'maxrate':'4000k', 'bufsize':'5000k', 'vf': '\"scale=-1:720, hue=s=0\"'},    
        # '480p': {'b:v':'1000k','minrate':'500k'},    
        '360p': {'b:v':'750k','minrate':'400k', 'maxrate':'1000k', 'bufsize':'1500k', 'vf': '\"scale=-1:360, hue=s=0\"'},    
}

get_url_params = lambda url: {s.split('=')[0]:s.split('=')[1] for s in requests.get(url).url.split('?')[1].split('&') }

def add_start(df):
    starts = []
    for u in df.link.values:
        params = get_url_params(u)
        if 'start' in params.keys():
            starts.append(int(params['start']))
        elif 't' in params.keys():
            starts.append(int(params['t']))

    df['start'] = starts
    return df

def add_end(df):
    ends = []
    for u in df.link.values:
        e = np.nan
        params = get_url_params(u)
        if 'end' in params.keys():
            e = params['end']
        ends.append(e)

    df['end'] = ends
    return df

def process_video(in_file,out_file=None, suffix=None, verbose=True, audio_bitrate='128k', video_bitrate='750k', preset='slow', **kwargs):
    arg_defaults = {'b:v':video_bitrate,'b:a':audio_bitrate,'preset':preset}
    kwargs.update(arg_defaults)

    if 'r' in kwargs.keys():
        kwargs.update(resolution_presets[kwargs['r']])
        del kwargs['r']

    d,in_fn = os.path.split(in_file)
    if out_file is None:
        out_file = os.path.join(d,'processed',in_fn)
    else:
        out_fn=out_file

    if suffix is not None:
        fp,ext = out_fn.split('.')
        out_file = fp+'{}_{}.{}'.format(fp,suffix,ext)


    in_file = os.path.expanduser(in_file)
    out_file = os.path.expanduser(out_file)

    cmd = "ffmpeg -i {} ".format(in_file)
    args = ' '.join(["-{} {}".format(k, kwargs[k]) for k in kwargs.keys()])

    if not verbose:
        args+=' -loglevel panic'

    cmd = cmd+args+" {}".format(out_file)

    os.system(cmd)

def process(infile, resolution, start=0, end=None, video_set=None, video_directory=None, verbose=False):
    video_meta = {'trickshots':trickshots, 'deepfake':records}

    if infile is not None:
        if not os.path.exists(infile):
            raise ValueError('{} does not exist'.format(infile))
        else:
            print('Converting @ {}'.format(resolution))
            # df=pd.DataFrame.from_records(trickshots+records])

            # df = df.pipe(add_start).pipe(add_end)
            dirpath, fn = os.path.split(infile)
            outfile = os.path.join(dirpath, 'processed_'+str(fn))

            opts = {'out_file':outfile, 'r':resolution, 'verbose':verbose}
            if start > 0:
                opts.update({'ss':start})
            if end is not None:
                print('\t{} -> {}(0\'{}\" -> 0\'{}\")'.format(infile,outfile,start,end))
                opts['t']=int(end)-int(start)
            else:
                print('\t{} -> {}(0\'{}\" -> {})'.format(infile,outfile,start,'end'))


            process_video(infile, **opts)

    elif os.path.exists(video_directory) and video_set is not None:
        vdir = os.path.expanduser(video_directory)
        print('Converting {} videos in {} @ {}'.format(video_set, vdir, resolution))
        v_files = glob.glob(os.path.join(vdir,'*.mp4'))
        v = pd.DataFrame.from_records(video_meta[video_set]).pipe(add_start).pipe(add_end)
        for i,row in v.iterrows():
            fp = os.path.join(vdir,row.fname)
            out_name = str(i+1)+'_'+row.fname
            out_file = os.path.join(vdir, 'processed', out_name)
            infile = os.path.split(fp)[-1]

            if pd.notna(row.end):
                t = int(row.end)-int(row.start)
                print('\t{} -> {}(0\'{}\" -> 0\'{}\")'.format(infile,out_file,row.start,row.end))
                process_video(fp, out_file = out_file, ss=row.start, t=t, r=resolution, suffix=row.type, verbose=verbose)
            else:
                print('\t{} -> {}(0\'{}\" -> {})'.format(infile,out_file,row.start,'end'))
                process_video(fp, out_file = out_file, ss=row.start, r=resolution, suffix=row.type, verbose=verbose)


        



@click.command()
@click.option('-i', '--infile', type=str, help='Single file input. By default will write the output to the same dir as input file')
@click.option('-r', '--resolution', default='360p',
        type=click.Choice(list(resolution_presets.keys())), help='Resolution options for output video(s)')
@click.option('-ss', '--start', default=0, type=int, help='Clip output video starting at ss (seconds)')
@click.option('-e', '--end', type=int, help='Clip output video at end (seconds)')
@click.option('--video_set', type=click.Choice(['trickshots','deepfake']), help='Video set to convert')
@click.option('-d', '--video_directory', default='./', help='Path to folder containing raw video files')
@click.option('--verbose', is_flag=True, default=False)
def preprocess(*args, **kwargs):
    return process(*args, **kwargs)

if __name__ == '__main__':
    preprocess()
