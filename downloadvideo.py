from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import sys
import os.path

# # Download vod
# url = 'https://www.youtube.com/watch?v=q4LQdAVusr0&list=PLMJ9cfx_WDdybdHDw28uCEFnxQvprJ59W&t=1180s'
# vod = YouTube(url).streams.get_highest_resolution()
# path_to_vod = './vods/'+str(vod.title)
# if (os.path.isfile(path_to_vod)):
#     print("Vod already exists!")
#     exit

# vod.download(output_path=f'./vods')

# vod_start = 1180
# vod_end = 1300
# ffmpeg_extract_subclip(path_to_vod, vod_start, vod_end, path_to_vod)

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    print(percentage_of_completion)

def download_video(url: str="https://www.youtube.com/watch?v=99k-EAMBuM8", verbose: bool=False):
    chunk_size = 1024
    yt = YouTube(url)
    vod = yt.streams.get_highest_resolution()
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

download_video(url="https://www.youtube.com/watch?v=99k-EAMBuM8")