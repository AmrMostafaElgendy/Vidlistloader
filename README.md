Certainly! Below is the `README.md` content with the missing section converted to code format as well.

```markdown
# YouTube Playlist Downloader

This tool allows you to download videos from YouTube playlists with ease. You can select specific videos, choose the desired quality, and set the download path. It provides a simple GUI interface using Tkinter and supports downloading videos in various resolutions.

## Features

- Fetch videos from a YouTube playlist.
- Select specific videos to download.
- Choose video quality (144p, 240p, 360p, 480p, 720p, 1080p).
- Set the download path for saving videos.
- Progress tracking for the download process.

## Requirements

- Python 3.x
- `tkinter` library
- `ttkthemes` library
- `pytube` library

## Installation

1. Make sure you have Python 3 installed on your machine.
2. Install the required libraries:
   ```bash
   pip install tk ttkthemes pytube
   ```

## Usage

1. Clone or download the script to your local machine.
2. Run the script:
   ```bash
   python youtube_playlist_downloader.py
   ```
3. Enter the YouTube playlist URL in the "Playlist URL" field.
4. Click on "Fetch Videos" to retrieve the list of videos in the playlist.
5. Select the videos you want to download from the list.
6. Choose the desired video quality from the "Select Quality" dropdown.
7. Set the download path by clicking on the "Browse" button and selecting the folder.
8. Click on the "Download" button to start downloading the selected videos.

## Code Overview

### Main Components

- **URL Input Section**: Allows users to input the YouTube playlist URL and fetch the list of videos.
- **Video Selection Section**: Displays the list of videos fetched from the playlist, allowing users to select which videos to download.
- **Quality and Path Selection Section**: Provides options to choose the video quality and set the download path.
- **Download Section**: Displays the current video being downloaded and a progress bar to track the download progress.

### Key Methods

- `fetch_videos()`: Fetches videos from the given YouTube playlist URL.
- `browse_path()`: Opens a dialog for the user to select the download path.
- `start_download()`: Initiates the download process for the selected videos.
- `download_videos(videos, quality, path)`: Handles the downloading of videos in a separate thread.
- `get_closest_quality(video, quality)`: Finds the closest available quality for a video if the desired quality is not available.
- `update_status(message)`: Updates the status message in the GUI.
- `update_progress(value)`: Updates the progress bar in the GUI.
- `on_frame_configure(event)`: Configures the scrolling region for the video list.

## Author

Amr Elgendy

```
