import os
from pytube import Playlist, YouTube
from pytube.exceptions import *

# function to download playlist videos
def download_playlist_videos(playlist_url, quality, destination):
    playlist = Playlist(playlist_url)
    # get all video urls in the playlist
    urls = playlist.video_urls
    print(f'Downloading {len(urls)} videos...')
    # loop over the urls and download each video
    for url in urls:
        try:
            download_video(url, quality, destination)
        except VideoUnavailable:
            print(f'Skipping video - {url}: video is unavailable')
        except PytubeError as e:
            print(f'Error occurred while downloading video - {url}: {str(e)}')
    print('Playlist downloaded successfully!')

# function to download a single video
def download_video(video_url, quality, destination):
    yt = YouTube(video_url)
    video = yt.streams.filter(res=quality).first()
    try:
        video.download(output_path=destination)
        print(f'Downloaded: {video.title}')
    except PytubeError as e:
        print(f'Error occurred while downloading {video.title}: {str(e)}')

# get user input for playlist url, quality, and destination folder
while True:
    playlist_url = input('Enter the playlist URL: ')
    if 'youtube.com/playlist' in playlist_url:
        break
    print('Invalid playlist URL. Please enter a valid YouTube playlist URL.')

while True:
    quality = input('Enter the quality (e.g. 720p, 480p): ')
    if quality in ['720p', '480p', '360p', '240p', '144p']:
        break
    print('Invalid quality. Please enter a valid quality (e.g. 720p, 480p).')

while True:
    destination = input('Enter the destination folder: ')
    if os.path.isdir(destination):
        break
    print('Invalid destination folder. Please enter a valid folder path.')

# call the function to download playlist videos
try:
    download_playlist_videos(playlist_url, quality, destination)
except PytubeError as e:
    print(f'Error occurred while downloading playlist: {str(e)}')
except Exception as e:
    print(f'Unknown error occurred: {str(e)}')
