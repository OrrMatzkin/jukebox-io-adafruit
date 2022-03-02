from asyncio import FastChildWatcher
import sys
from typing import List
from urllib import request
import vlc
import json
import time
from Adafruit_IO import MQTTClient, Client, Feed, RequestError
import subprocess


ADAFRUIT_IO_KEY = "<YOUR ADAFRUIT IO KEY>"
ADAFRUIT_IO_USERNAME = "<YOUR ADAFRUIT IO USERNAME>"
AIO_FEED_ID = "playing-song"
JUKEBOX_BANNER = """     
       ██╗██╗   ██╗██╗  ██╗███████╗██████╗  ██████╗ ██╗  ██╗       
       ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝       
       ██║██║   ██║█████╔╝ █████╗  ██████╔╝██║   ██║ ╚███╔╝          
  ██   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗██║   ██║ ██╔██╗       |~~~~~~~~~~|
  ╚█████╔╝╚██████╔╝██║  ██╗███████╗██████╔╝╚██████╔╝██╔╝ ██╗      |~~~~~~~~~~|
   ╚═Orr Matzkin═╝ ╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝      |          |
                                                              /~~\|      /~~\|
                                                              \__/       \__/ 
                                                                          """

JUKEBOX_OPENING = """A modern partially automated music-playing device activted by Google Assistant.
To active the jukebox just say to your google assiatnt: "Jukebox, play XXXX".
To stop the music say: "Jukebox, stop music".
For browsing the available songs say: "Jukebox, display songs"."""
                                                     

class Jukebox:

    current_song = None

    def __init__(self, songs_data: str) -> None:
        """Loads the json songs data file and creates a vlc and media player instances.
        
        Args: 
            songs_data (str): The json file songs data.
        """
        with open(songs_data, 'r') as f:
            songs = json.load(f)
        self.songs_by_name = dict([(s['name'], s) for s in songs])   

        self.vlc_instance = vlc.Instance('--quiet')
        self.media_player = self.vlc_instance.media_player_new()  
        self.media_player.toggle_fullscreen()

        self.aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
        self.feed = self.aio.feeds(AIO_FEED_ID)

        self.is_playing = False
        self.msg_displayed = ""

        print(JUKEBOX_BANNER)
        print("a")
        
    def play_video(self, song_request: str) -> None:
        """Playes the given song.

        Args:
            song (List[str]): song data. 

        Returns:
            bool: True if jukebox is playing the song successfully, else False.    
        """
        song = self.find_best_match(song_request)
        if song is None:
             self.display_msg("Song not found! Plase request another song...")    
        elif song is not self.current_song:    
            self.current_song = song
            self.display_msg(f"playing {self.current_song['name']}")    
            self.media_player.set_media(self.vlc_instance.media_new(self.current_song['path'])) 
            self.media_player.play()
            self.is_playing = True
        else:
            print(f"{self.current_song['name']} is already playing")
        
    def stop_video(self) -> None:
        """Stops the current music video, (if there is non playing does nothing).
        """
        self.display_msg("Music stoped, please make a new reqest...")    
        self.current_song = None
        self.media_player.stop()
        self.is_playing = False

    def find_best_match(self, request: str) -> List[str]:
        """Finds the best match of all song.

        Args:
            request (str)): song request. 

        Returns:
            List[str]: returns the best scored matched song, if none found returns None;    
        """
        best_score = 0
        best_match = None
        request_list = {s.lower() for s in request.split()}
        for song in self.songs_by_name.values():
            num_of_mathces = len(request_list.intersection(song["matches"]))
            score = num_of_mathces / len(song["matches"])
            if score > best_score:
                best_score = score
                best_match = song
        return best_match

    def display_msg(self, msg: str) -> None:
        if  msg != self.msg_displayed:
            print("\033[A{}\033[A".format(' '*len(self.msg_displayed)))
            print(msg)
            self.msg_displayed = msg
        

    def run(self) -> None:
        """Main loop, starts the jukebox."""
        old_request = None
        displayed_songs = False
        while(True):
            feed_data = self.aio.receive(self.feed.key)
            song_request = feed_data.value
            if song_request == "Null":
                if self.is_playing:
                    self.stop_video()  
                else:
                    self.display("Waiting for a song request...")    
            elif song_request != old_request:
                self.play_video(song_request)
                old_request = song_request


    def __del__(self):
        self.media_player.release()
                
            
            
if __name__ == "__main__":

    # TODO: remove key and user name getters for final commit
    ADAFRUIT_IO_KEY = sys.argv[1]
    ADAFRUIT_IO_USERNAME = sys.argv[2]    
    AIO_FEED_ID = sys.argv[3]
    jukebox = Jukebox("songs_data.json")
    jukebox.run()


   
