from asyncio import FastChildWatcher
import sys
from typing import List
from urllib import request
import vlc
import json
import time
from Adafruit_IO import MQTTClient, Client, Feed, RequestError


ADAFRUIT_IO_KEY = "<YOUR ADAFRUIT IO KEY>"
ADAFRUIT_IO_USERNAME = "<YOUR ADAFRUIT IO USERNAME>"
AIO_FEED_ID = 'playing-song'

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
        



    def play_video(self, song_reqest: str) -> bool:
        """Playes the given song.

        Args:
            song (List[str]): song data. 

        Returns:
            bool: True if jukebox is playing the song successfully, else False.    
        """
        song = self.find_best_match(song_reqest)
        if song is None:
            print("song not found!")
            return False
        elif song is not self.current_song:    
            self.current_song = song
            print(f"playing {self.current_song['name']}")
            self.media_player.set_media(self.vlc_instance.media_new(self.current_song['path'])) 
            self.media_player.play()
            self.is_playing = True
            return True
        else:
            print(f"{self.current_song['name']} is already playing")
            return True


    def stop_video(self) -> None:
        """Stops the current music video, (if there is non playing does nothing).
        """
        print("stoping music")
        self.current_song = None
        self.media_player.stop()
        self.is_playing = False

    def find_best_match(self, reqest: str) -> List[str]:
        """Finds the best match of all song.

        Args:
            reqest (str)): song reqest. 

        Returns:
            List[str]: returns the best scored matched song, if none found returns None;    
        """
        best_score = 0
        best_match = None
        reqest_list = {s.lower() for s in reqest.split()}
        for song in self.songs_by_name.values():
            num_of_mathces = len(reqest_list.intersection(song["matches"]))
            score = num_of_mathces / len(song["matches"])
            print(reqest_list)
            print(song["matches"])
            if score > best_score:
                best_score = score
                best_match = song
        return best_match

    def run(self) -> None:
        old_reqest = None
        while(True):
            feed_data = self.aio.receive(self.feed.key)
            song_reqest = feed_data.value
            if song_reqest == "Null" and self.is_playing:
                self.stop_video()    
            elif song_reqest != old_reqest:
                self.play_video(song_reqest)
                old_reqest = song_reqest
                
            
                
                


def io_test():

    # Create an instance of the REST client.
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    FEED_ID = 'playing-song'
    video_player = aio.feeds(FEED_ID)

    # try: # if we have a 'video_player' feed
    #     video_player = aio.feeds(FEED_ID)
    # except RequestError: # create a digital feed
    #     print("No feed found!")
    
    
    while True:
        data = aio.receive(video_player.key)
        print(data.value)
           
        # if data.value == 'ON':
        #     print('received <- ON')
        # elif data.value == 'OFF':
        #     print('received <- OFF')
   
    
if __name__ == "__main__":

    # TODO: remove key and user name getters for final commit
    ADAFRUIT_IO_KEY = sys.argv[1]
    ADAFRUIT_IO_USERNAME = sys.argv[2]    
    AIO_FEED_ID = sys.argv[3]
    
    jukebox = Jukebox("songs_data.json")

    jukebox.run()

    # jukebox.play_video("the police")
    # time.sleep(5)
    # jukebox.stop_video()

    

    # io_test()
 
