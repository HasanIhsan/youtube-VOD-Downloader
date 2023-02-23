from pytube import YouTube
from pytube import Playlist
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
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_by_itag(22)
    try:
       
        youtubeObject.download(os.getcwd()+'\Downloaded_Videos')
    except:
        print("An error has occurred")
    print("Download is completed successfully")



#Using readlines() read a file 
links = open(os.getcwd()+"\links.txt") 
AllLinks = links.readlines()

#Create a new folder called downloaded_videos
os.mkdir('Downloaded_Videos')   
count = 0
# Strips the newline character

for link in AllLinks:
    count += 1
    print("Link: {}: {}".format(count, link.strip()))
    DownloadVideo(link)

 
 