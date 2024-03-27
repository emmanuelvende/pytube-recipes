import functools
import pathlib
import subprocess

import pytube

FFMPEG = "path/to/ffmpeg.exe"

def convert_tracks_to_mp3s(tracks):
    for track in tracks:
        convert_to_mp3(track)

def convert_to_mp3(fp):
    outfp = fp.with_suffix(".mp3")
    command = f'{FFMPEG} -i "{fp}" -ar 44100 "{outfp}"'
    subprocess.run(command, shell=True)


def download_best_audio_stream(yt):
    def _compare_audio_bitrate(x, y):
        return int(x.abr[:-4]) - int(y.abr[:-4])

    print(f"Downloading best audio for {yt}...")
    return sorted(
        yt.streams.filter(only_audio=True),
        key=functools.cmp_to_key(_compare_audio_bitrate),
    )[-1].download()


def download_best_audio_tracks(urls):
    filepaths = []
    for url in urls:
        yt = pytube.YouTube(url)
        filepaths.append(pathlib.Path(download_best_audio_stream(yt)))
    return filepaths


with open("videos.txt", "r") as f:
    urls = f.read().split("\n")

tracks = download_best_audio_tracks(urls)
convert_tracks_to_mp3s(tracks)
