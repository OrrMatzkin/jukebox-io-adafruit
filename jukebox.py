import sys
from typing import List
from urllib import request
import vlc
import json
import time
from Adafruit_IO import MQTTClient, Client, Feed, RequestError


ADAFRUIT_IO_KEY = "<YOUR ADAFRUIT IO KEY>"
ADAFRUIT_IO_USERNAME = "<YOUR ADAFRUIT IO USERNAME>"

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

        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()  
        self.media_player.toggle_fullscreen()

    def play_video(self, song_name: str) -> bool:
        """Playes the given song.

        Args:
            song (List[str]): song data. 

        Returns:
            bool: True if jukebox is playing the song successfully, else False.    
        """
        self.current_song = self.find_best_match(song_name)
        if self.current_song is None:
            print("song not found!")
            return False
        else:    
            print(f"playing {self.current_song['name']}")
            self.media_player.set_media(self.vlc_instance.media_new(self.current_song['path'])) 
            self.media_player.play()
            return True

    def stop_video(self) -> None:
        """Stops the current music video, (if there is non playing does nothing).
        """
        print("stoping music")
        self.current_song = None
        self.media_player.stop()


    def find_best_match(self, reqest: str) -> List[str]:
        """Finds the best match of all song.

        Args:
            reqest (str)): song reqest. 

        Returns:
            List[str]: returns the best scored matched song, if none found returns None;    
        """
        best_score = 0
        best_match = None
        reqest_list = [s.lower() for s in reqest.split()]
        for song in self.songs_by_name.values():
            num_of_mathces = sum(x == y for x, y in zip(reqest_list, song["mathches"]))
            score = num_of_mathces / len(song["mathches"])
            if score > best_score:
                best_score = score
                best_match = song
        return best_match

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
    
    jukebox = Jukebox("songs_data.json")

    jukebox.play_video("YOu got")
    time.sleep(5)
    jukebox.stop_video()

    

    # io_test()
 
