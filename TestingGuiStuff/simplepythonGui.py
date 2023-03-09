import tkinter as tk
from pytube import YouTube

def download():
    video_url = url_entry.get()
    yt = YouTube(video_url)
    stream = yt.streams.first()
    stream.download()
    status_label.config(text="Download complete!")

root = tk.Tk()
root.title("YouTube Video Downloader")

# Create GUI elements
url_label = tk.Label(root, text="Video URL:")
url_entry = tk.Entry(root, width=50)
download_button = tk.Button(root, text="Download", command=download)
status_label = tk.Label(root, text="")

# Add GUI elements to the window
url_label.pack(pady=10)
url_entry.pack(pady=5)
download_button.pack(pady=5)
status_label.pack(pady=10)

root.mainloop()
