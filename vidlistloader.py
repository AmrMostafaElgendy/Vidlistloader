import os
from pytube import Playlist, YouTube
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog



# function to download playlist videos
def download_playlist_videos(playlist_url, quality, destination, progress_bar, progress_text):
    playlist = Playlist(playlist_url)
    # get all video urls in the playlist
    urls = playlist.video_urls
    print(f'Downloading {len(urls)} videos...')
    # loop over the urls and download each video
    for i, url in enumerate(urls):
        progress_text.set(f'Downloading video {i+1} of {len(urls)}')
        download_video(url, quality, destination)
        progress_bar['value'] = (i+1)/len(urls)*100
        root.update_idletasks()
    progress_text.set('Playlist downloaded successfully!')
    progress_bar['value'] = 100

# function to download a single video
def download_video(video_url, quality, destination):
    yt = YouTube(video_url)
    video = yt.streams.filter(res=quality).first()
    video.download(output_path=destination)
    print(f'Downloaded: {video.title}')

# function to select the destination folder using a file dialog
def browse_destination_folder():
    folder_path = filedialog.askdirectory()
    destination_folder.set(folder_path)

# create main window
root = Tk()
root.title('Vidlistloader')
root.geometry('400x300')

# create input fields and labels
playlist_url = StringVar()
quality = StringVar()
destination_folder = StringVar()

playlist_label = Label(root, text='Playlist URL:')
playlist_entry = Entry(root, textvariable=playlist_url)

quality_label = Label(root, text='Quality:')
quality_entry = Entry(root, textvariable=quality)

destination_label = Label(root, text='Destination:')
destination_entry = Entry(root, textvariable=destination_folder)
destination_button = Button(root, text='Browse', command=browse_destination_folder)

Copyright_label = Label(root, text='© 2023 -Amr Elgendy, All right reserved')

# create progress bar and text
progress_bar = Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
progress_text = StringVar()
progress_label = Label(root, textvariable=progress_text)

# create download button
download_button = Button(root, text='Download', command=lambda: download_playlist_videos(playlist_url.get(), quality.get(), destination_folder.get(), progress_bar, progress_text))

# place widgets in the window
playlist_label.pack()
playlist_entry.pack()


quality_label.pack()
quality_entry.pack()

destination_label.pack()
destination_entry.pack()
destination_button.pack()


download_button.pack()

progress_bar.pack()
progress_label.pack()

Copyright_label.pack()


root.mainloop()
