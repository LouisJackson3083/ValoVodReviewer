from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *
import sys
import os
import asyncio

def on_progress(stream, chunk, bytes_remaining):
    filesize = stream.filesize
    current = ((filesize - bytes_remaining)/filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()

async def download_vod(url: str="https://www.youtube.com/watch?v=99k-EAMBuM8", verbose: bool=False) -> str:
    """
    Given a url, we download a video to ./vods/
    returns:
        video path
        video resolution
    """
    chunk_size = 2048
    yt = YouTube(url)

    # find the highest quality mp4 vod
    itag = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()[0].itag
    vod = yt.streams.get_by_itag(itag)

    yt.register_on_progress_callback(on_progress)
    if (verbose):
        print(f"Fetching \"{vod.title}\"..")
        print(f"Fetching successful\n")
        print(f"Information: \n"
            f"File size: {round(vod.filesize * 0.000001, 2)} MegaBytes\n"
            f"Highest Resolution: {vod.resolution}\n"
            f"Author: {yt.author}")
        print("Views: {:,}\n".format(yt.views))

    print(f"Downloading \"{vod.title}\"..")
    vod.download(output_path='./vods/')
    return './vods/'+str(vod.title), int(vod.resolution[:-1])

async def crop_vod_to_minimap(vod_path: str, vod_resolution: int, vod_start: str, vod_end: str):
    vod_height = vod_resolution
    vod_width = vod_resolution*1.77777777778

    ftr = [3600,60,1]
    vod_start_seconds = sum([a*b for a,b in zip(ftr, map(int,vod_start.split(':')))])
    vod_end_seconds = sum([a*b for a,b in zip(ftr, map(int,vod_end.split(':')))])

    clip = VideoFileClip(vod_path+'.mp4')
    clip = clip.subclip(vod_start_seconds, vod_end_seconds)
    clip = clip.crop(x1=0, y1=0, x2=vod_width/4.5, y2=vod_height/2.5)
    clip.write_videofile(vod_path+'_EDITED.mp4')
    clip.close()


async def main() -> None:
    vod_path, vod_resolution = await download_vod(
        url="https://youtu.be/XUREmJccWNw?si=Wk_9ON0zvW1z87BR", 
        verbose=True
    )

    await crop_vod_to_minimap(
        vod_path=vod_path, 
        vod_resolution=vod_resolution, 
        vod_start='00:39:24',
        vod_end='00:40:00',
    )

    os.remove(vod_path+'.mp4')

if __name__ == '__main__':
    asyncio.run(main())