from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress #this module contains the built in progress bar.  
from pathlib import Path 
  
import os

 
 

 

#using pytube to download playlists (currently not implmented with my code)
# needs testing! 
def DownloadPlaylists(link):
    youtubeObject = Playlist(link)

    try:
        #printing video titles
        print(f'Downloading: {youtubeObject.title}') 

        os.mkdir('Downloaded_Video_Playlist')
        for video in youtubeObject.videos:
            video.streams.first().download(os.getcwd()+'\Downloaded_Video_Playlist')

    except:
        print("an error has Occured")
    print("Download is Completed successfully")


#using pytube to download videos from a link
def DownloadVideo(link):
    #create a youtube object for youtube
    #get the highest resolution video has (may take a long time to download for larger resolutions)
    youtubeObject = YouTube(link,on_progress_callback=on_progress)
    youtubeObject = youtubeObject.streams.get_by_itag(22)
    try: 
        print(youtubeObject.title)
        youtubeObject.download(os.getcwd()+'\Downloaded_Videos')
    except:
        print("An error has occurred")


def startDownload():
    #Using readlines() read a file 
    links = open(os.getcwd()+"\links.txt") 
    AllLinks = links.readlines()
     
    count = 0
    # Strips the newline character
     
    for link in AllLinks:
        count += 1 
        print("Link: {}: {}".format(count, link.strip()))
        DownloadVideo(link)



 

#Create a new folder called downloaded_videos 
#checking if folder exits
path = os.getcwd()+"\Downloaded_Videos"
isExist = os.path.exists(path)

if isExist:
    print("Download Folder Found:")
    print("Starting Download:\n\n")

    startDownload()
else:
    print("Download Folder Not Found Creating...\n")
    os.mkdir('Downloaded_Videos')   

    print("Download Folder Created:\n")
    print("Starting Download...:\n\n")
    startDownload()





 
 
 

 

 