import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

#choose which director where the user wants to download videos
def choose_directory():
    download_directory.set(filedialog.askdirectory())

#download check if user wants a mp3 or mp4
def download():
    video_urls = url_entry.get("1.0", tk.END).splitlines()
    for video_url in video_urls:
        yt = YouTube(video_url.strip())
        if file_type.get() == "mp3":
            stream = yt.streams.filter(only_audio=True).first()
            out_file = stream.download(output_path=download_directory.get())
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        elif file_type.get() == "mp4":
            stream = yt.streams.first()
            out_file = stream.download(output_path=download_directory.get())
            status_label.config(text="Converting to MP4...")
            clip = VideoFileClip(out_file)
            clip.write_videofile(os.path.splitext(out_file)[0] + ".mp4")
            clip.close()
            os.remove(out_file)
        status_label.config(text="Download complete!")
        

root = tk.Tk()
root.title("YouTube Downloader")

# Create GUI elements
url_label = tk.Label(root, text="Video URLs (one per line):")
url_entry = tk.Text(root, height=5, width=50)
file_type_label = tk.Label(root, text="File type:")
file_type = ttk.Combobox(root, values=["mp3", "mp4"])
file_type.current(0)
directory_label = tk.Label(root, text="Download directory:")
download_directory = tk.StringVar()
download_directory.set(os.getcwd())
directory_entry = tk.Entry(root, textvariable=download_directory, width=50)
directory_button = tk.Button(root, text="Choose directory", command=choose_directory)
download_button = tk.Button(root, text="Download", command=download)
status_label = tk.Label(root, text="")

# Add GUI elements to the window
url_label.pack(pady=10)
url_entry.pack(pady=5)
file_type_label.pack(pady=5)
file_type.pack(pady=5)
directory_label.pack(pady=5)
directory_entry.pack(pady=5)
directory_button.pack(pady=5)
download_button.pack(pady=5)
status_label.pack(pady=10)

root.mainloop()
