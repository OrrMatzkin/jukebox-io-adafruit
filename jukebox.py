import sys
from typing import List
import vlc
import json
from Adafruit_IO import Client
import threading



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
   A modern partially automated music-playing device          \__/       \__/ 
   activted by Google Assistant.                                           

"""

JUKEBOX_OPENING = """Google Assistant Commands:
- To play a song say: "Jukebox, play XXXX".
- To stop the music say: "Jukebox, stop music".
- To display all available songs say: "Jukebox, display songs".
(To exit enter: 'q').\n"""
                                                     

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
        self.aio.send_data(self.feed.key, "Null")

        self.is_playing = False
        self.displayed_songs = False
        self.msg_displayed = ""

        print(JUKEBOX_BANNER)
        print(JUKEBOX_OPENING + '\n')
        
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
            self.display_msg(f"playing {self.current_song['name']} by {self.current_song['artist']}")    
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
            if self.displayed_songs:
                self.delete_msg(len(self.songs_by_name)+3)
            else:
                self.delete_msg(1)  
            self.displayed_songs = False       
            print(msg)
            self.msg_displayed = msg

    def delete_msg(self, num_of_line: int) -> None:
        for _ in range(num_of_line):
            print("\033[A{}\033[A".format(' '*80))  

    def display_available_songs(self) -> None:
        self.delete_msg(1)
        print("The availbe songs are:")
        counter = 1
        for song in self.songs_by_name.values():
            name, artist = song["name"], song["artist"]
            print(f"{counter}. {name} by {artist}") 
            counter += 1   
        print("\nWaiting for a song request...") 

    def run(self) -> None:
        """Main loop, starts the jukebox."""
        threading1 = threading.Thread(target=self.main_loop)
        threading1.daemon = True
        threading1.start()
        while(True):
            if input() == "q":
                sys.exit()
                

    def main_loop(self):
        """Main loop, starts the jukebox."""
        old_request = None
        while(True):
            feed_data = self.aio.receive(self.feed.key)
            song_request = feed_data.value
            if not self.displayed_songs and song_request == "@display_songs":
                if self.is_playing:
                        self.stop_video()  
                self.display_available_songs()
                self.displayed_songs = True
            elif song_request == "Null":
                if self.is_playing:
                    self.stop_video()  
                else:
                    self.display_msg("Waiting for a song request...")    
            elif song_request != "@display_songs" and song_request != old_request:
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


   
