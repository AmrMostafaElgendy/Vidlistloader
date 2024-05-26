import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from pytube import Playlist, YouTube
import threading
import os

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Downloader")
        self.root.geometry("600x600")

        # Apply the theme
        root.set_theme("radiance")

        self.main_frame = ttk.Frame(root, padding="10 10 10 10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # URL Input Section
        self.url_frame = ttk.LabelFrame(self.main_frame, text="Playlist URL", padding="10 10 10 10")
        self.url_frame.pack(fill=tk.X, pady=10)

        self.url_entry = ttk.Entry(self.url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.fetch_button = ttk.Button(self.url_frame, text="Fetch Videos", command=self.fetch_videos)
        self.fetch_button.pack(side=tk.RIGHT, padx=5)

        # Video Selection Section
        self.video_frame = ttk.LabelFrame(self.main_frame, text="Select Videos", padding="10 10 10 10")
        self.video_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.canvas = tk.Canvas(self.video_frame, borderwidth=0)
        self.video_list_frame = ttk.Frame(self.canvas)
        self.vsb = ttk.Scrollbar(self.video_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.video_list_frame, anchor="nw", tags="self.video_list_frame")

        self.video_list_frame.bind("<Configure>", self.on_frame_configure)

        # Quality and Path Selection Section
        self.options_frame = ttk.LabelFrame(self.main_frame, text="Options", padding="10 10 10 10")
        self.options_frame.pack(fill=tk.X, pady=10)

        self.quality_label = ttk.Label(self.options_frame, text="Select Quality:")
        self.quality_label.pack(side=tk.LEFT, padx=5)

        self.quality_options = ["144p", "240p", "360p", "480p", "720p", "1080p"]
        self.quality_var = tk.StringVar(value=self.quality_options[0])
        self.quality_menu = ttk.OptionMenu(self.options_frame, self.quality_var, *self.quality_options)
        self.quality_menu.pack(side=tk.LEFT, padx=5)

        self.path_label = ttk.Label(self.options_frame, text="Download Path:")
        self.path_label.pack(side=tk.LEFT, padx=5)

        self.path_entry = ttk.Entry(self.options_frame, width=30)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.browse_button = ttk.Button(self.options_frame, text="Browse", command=self.browse_path)
        self.browse_button.pack(side=tk.RIGHT, padx=5)

        # Download Section
        self.download_frame = ttk.Frame(self.main_frame, padding="10 10 10 10")
        self.download_frame.pack(fill=tk.X, pady=10)

        self.download_button = ttk.Button(self.download_frame, text="Download", command=self.start_download)
        self.download_button.pack(pady=10)

        self.current_video_label = ttk.Label(self.download_frame, text="Current Video: None")
        self.current_video_label.pack(pady=5)

        self.progress = ttk.Progressbar(self.download_frame, orient='horizontal', length=400, mode='determinate')
        self.progress.pack(pady=5)

    def fetch_videos(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a playlist URL.")
            return
        try:
            playlist = Playlist(url)
            self.videos = playlist.videos
            for widget in self.video_list_frame.winfo_children():
                widget.destroy()
            self.video_vars = []
            for video in self.videos:
                var = tk.BooleanVar()
                chk = ttk.Checkbutton(self.video_list_frame, text=video.title, variable=var)
                chk.pack(anchor='w', pady=2)
                self.video_vars.append(var)
            self.on_frame_configure(None)  # Adjust the scroll region
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch playlist: {e}")

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def start_download(self):
        selected_videos = [video for video, var in zip(self.videos, self.video_vars) if var.get()]
        quality = self.quality_var.get()
        path = self.path_entry.get()
        if not selected_videos:
            messagebox.showwarning("Warning", "No videos selected.")
            return
        if not path:
            messagebox.showwarning("Warning", "No download path selected.")
            return
        if not os.path.isdir(path):
            messagebox.showwarning("Warning", "The selected path is invalid.")
            return
        self.progress["value"] = 0
        self.progress["maximum"] = len(selected_videos)
        threading.Thread(target=self.download_videos, args=(selected_videos, quality, path)).start()

    def download_videos(self, videos, quality, path):
        try:
            for idx, video in enumerate(videos):
                self.update_status(f"Current Video: {video.title}")
                yt = video.streams.filter(progressive=True, res=quality, file_extension='mp4').first()
                if yt is None:
                    yt = self.get_closest_quality(video, quality)
                if yt:
                    yt.download(output_path=path)
                else:
                    messagebox.showerror("Error", f"Failed to find suitable stream for: {video.title}")
                self.update_progress(idx + 1)
            self.update_status("Download Complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")

    def get_closest_quality(self, video, quality):
        available_qualities = ["144p", "240p", "360p", "480p", "720p", "1080p"]
        current_idx = available_qualities.index(quality)
        for q in available_qualities[current_idx:]:
            yt = video.streams.filter(progressive=True, res=q, file_extension='mp4').first()
            if yt:
                return yt
        for q in reversed(available_qualities[:current_idx]):
            yt = video.streams.filter(progressive=True, res=q, file_extension='mp4').first()
            if yt:
                return yt
        return None

    def update_status(self, message):
        # This method is called from a different thread, so we need to use `after` to update the GUI.
        self.root.after(0, lambda: self.current_video_label.config(text=message))

    def update_progress(self, value):
        # This method is called from a different thread, so we need to use `after` to update the GUI.
        self.root.after(0, lambda: self.progress.config(value=value))

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = ThemedTk(theme="radiance")
    app = YouTubeDownloader(root)
    root.mainloop()
