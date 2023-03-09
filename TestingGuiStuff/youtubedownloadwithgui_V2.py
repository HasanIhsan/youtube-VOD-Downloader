import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube, Playlist
from moviepy.video.io.VideoFileClip import VideoFileClip
import os


#note: downloading playlist/videos doensn't work yet
def choose_directory():
    download_directory.set(filedialog.askdirectory())

def choose_playlist_directory():
    playlist_directory.set(filedialog.askdirectory())

def choose_file():
    file_path = filedialog.askopenfilename()
    with open(file_path, "r") as f:
        urls = f.readlines()
        url_entry.delete("1.0", tk.END)
        url_entry.insert(tk.END, "\n".join(urls))

def download():
    video_urls = url_entry.get("1.0", tk.END).splitlines()
    if playlist_var.get():  # Download a playlist
        playlist = Playlist(video_urls[0].strip())
        if not os.path.exists(playlist_directory.get()):
            os.makedirs(playlist_directory.get())
        for i, video in enumerate(playlist.videos):
            video_title = video.title
            if len(video_title) > 50:
                video_title = video_title[:50] + "..."
            if file_type.get() == "mp3":
                stream = video.streams.filter(only_audio=True).first()
                out_file = os.path.join(playlist_directory.get(), "{}.mp3".format(video_title))
                stream.download(output_path=playlist_directory.get(), filename=video_title)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
            elif file_type.get() == "mp4":
                stream = video.streams.first()
                out_file = os.path.join(playlist_directory.get(), "{}.mp4".format(video_title))
                status_label.config(text="Downloading {} ({}/{})...".format(playlist.title, i+1, len(playlist)))
                stream.download(output_path=playlist_directory.get(), filename=video_title)
                clip = VideoFileClip(out_file)
                clip.write_videofile(os.path.splitext(out_file)[0] + ".mp4", audio_codec='aac')
                clip.close()
                os.remove(out_file)
            show_progress(i+1, len(playlist))
        status_label.config(text="Download complete!")
        progress_label.config(text="")
        progress_bar['value'] = 0
        popup = tk.Toplevel(root)
        popup.geometry("300x100")
        popup.title("Download completed!")
        popup_label = tk.Label(popup, text="Download complete!")
        popup_label.pack(pady=20)
        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack()
    else:  # Download a single video
        for i, url in enumerate(video_urls):
            try:
                yt = YouTube(url, on_progress_callback=show_progress)
                video_title = yt.title
                if len(video_title) > 50:
                    video_title = video_title[:50] + "..."
                if file_type.get() == "mp3":
                    stream = yt.streams.filter(only_audio=True).first()
                    out_file = os.path.join(download_directory.get(), "{}.mp3".format(video_title))
                    stream.download(output_path=download_directory.get(), filename=video_title)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                elif file_type.get() == "mp4":
                    stream = yt.streams.first()
                    out_file = os.path.join(download_directory.get(), "{}.mp4".format(video_title))
                    status_label.config(text="Downloading {} ({}/{})...".format(video_title, i+1, len(video_urls)))
                    stream.download(output_path=download_directory.get(), filename=video_title)
                    clip = VideoFileClip(out_file)
                    clip.write_videofile(os.path.join(download_directory.get(), "{}.mp4".format(video_title)))
                    clip.close()
                    os.remove(out_file)
            except Exception as e:
                print(e)
                status_label.config(text="Error: {}".format(str(e)))
        status_label.config(text="Download complete!")
        progress_label.config(text="")
        progress_bar['value'] = 0
        popup = tk.Toplevel(root)
        popup.geometry("300x100")
        popup.title("Download completed!")
        popup_label = tk.Label(popup, text="Download complete!")
        popup_label.pack(pady=20)
        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack()






def show_progress(stream, chunk, bytes_remaining):
    size = stream.filesize
    downloaded = size - bytes_remaining
    percent = (downloaded / size) * 100
    progress_bar['value'] = percent
    progress_label.config(text="{:00.0f}% downloaded".format(percent))

root = tk.Tk()
root.title("YouTube Downloader")


download_directory = tk.StringVar()
download_directory.set(os.getcwd())
playlist_directory = tk.StringVar()


main_frame = ttk.Frame(root, padding="30 15")
main_frame.grid(column=0, row=0, sticky="nswe")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


download_label = ttk.Label(main_frame, text="Choose download directory:")
download_label.grid(column=0, row=2, sticky="w", pady=5)
download_button = ttk.Button(main_frame, text="Choose directory", command=choose_directory)
download_button.grid(column=1, row=2, sticky="w")

file_type = tk.StringVar()
file_type.set("mp4")

url_label = ttk.Label(main_frame, text="Enter video URL(s):")
url_label.grid(column=0, row=0, sticky="w", pady=5)

url_entry = tk.Text(main_frame, height=10, width=50)
url_entry.grid(column=1, row=0, padx=5, pady=5)

file_type_label = ttk.Label(main_frame, text="Choose file type:")
file_type_label.grid(column=0, row=1, sticky="w", pady=5)

mp4_radiobutton = ttk.Radiobutton(main_frame, text="mp4", variable=file_type, value="mp4")
mp4_radiobutton.grid(column=1, row=1, sticky="w")

mp3_radiobutton = ttk.Radiobutton(main_frame, text="mp3", variable=file_type, value="mp3")
mp3_radiobutton.grid(column=2, row=1, sticky="w")

playlist_var = tk.BooleanVar()
playlist_checkbox = ttk.Checkbutton(main_frame, text="Download playlist", variable=playlist_var)
playlist_checkbox.grid(column=0, row=3, sticky="w", pady=5)

playlist_directory_label = ttk.Label(main_frame, text="Choose playlist directory:")
playlist_directory_label.grid(column=0, row=4, sticky="w", pady=5)
playlist_directory_button = ttk.Button(main_frame, text="Choose directory", command=choose_playlist_directory)
playlist_directory_button.grid(column=1, row=4, sticky="w")

download_button = ttk.Button(main_frame, text="Download", command=download)
download_button.grid(column=1, row=5, pady=10)

status_label = ttk.Label(main_frame, text="")
status_label.grid(column=0, row=6, columnspan=2, pady=5)

progress_label = ttk.Label(main_frame, text="")
progress_label.grid(column=0, row=7, columnspan=2, pady=5)

progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(column=0, row=8, columnspan=2, pady=5)

root.mainloop()

