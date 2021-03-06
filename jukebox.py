import sys
import vlc
import json
import threading
from typing import List
from Adafruit_IO import Client

ADAFRUIT_IO_KEY = "<YOUR ADAFRUIT IO KEY>"
ADAFRUIT_IO_USERNAME = "<YOUR ADAFRUIT IO USERNAME>"
AIO_FEED_ID = "<YOUR FEED NAME>"

JUKEBOX_BANNER = """     
       ██╗██╗   ██╗██╗  ██╗███████╗██████╗  ██████╗ ██╗  ██╗       
       ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝       
       ██║██║   ██║█████╔╝ █████╗  ██████╔╝██║   ██║ ╚███╔╝          
  ██   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗██║   ██║ ██╔██╗       |~~~~~~~~~|
  ╚█████╔╝╚██████╔╝██║  ██╗███████╗██████╔╝╚██████╔╝██╔╝ ██╗      |~~~~~~~~~|
   ╚═Orr Matzkin═╝ ╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝      |         |
                                                              /~~\|     /~~\|
   A modern partially automated music-playing program         \__/      \__/ 
   activted by Google Assistant.\n\n"""
JUKEBOX_OPENING = """Google Assistant Commands:
- To play a song say: "Jukebox, play XXXX".
- To stop the music say: "Jukebox, stop music".
- To display all available songs say: "Jukebox, display songs".
(To exit enter: 'q').\n"""
                                                     
class Jukebox:

    def __init__(self, songs_data: str) -> None:
        """ Initializing a jukebox.
        Args: 
            songs_data (str): The json file songs data.
        """
        # loading json file
        with open(songs_data, 'r') as f:
            songs = json.load(f)
        self.songs_by_name = dict([(s['name'], s) for s in songs])   

        # creating the media player
        self.vlc_instance = vlc.Instance('--quiet')
        self.media_player = self.vlc_instance.media_player_new()  
        self.media_player.toggle_fullscreen()
        
        # setting defualt config for adafruit io   
        self.aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
        self.feed = self.aio.feeds(AIO_FEED_ID)
        self.aio.send_data(self.feed.key, "Null")

        # setting defualt class variables
        self.current_song = None
        self.is_playing = False
        self.is_available_songs_displayed = False
        self.current_msg = ""
        
        print(JUKEBOX_BANNER)
        print(JUKEBOX_OPENING + '\n')
        

    def play_video(self, song_request: str) -> None:
        """Tries to play the requested song.
        Args:
            song (str): song request.   
        """
        song = self.find_best_match(song_request)
        # match not found
        if song is None:
             self.display_msg("Song not found! Plase request another song...")   
        # song is alredy playing 
        elif song is self.current_song:
            self.display_msg(f"{self.current_song['name']} is already playing")   
        # play matched song    
        else:    
            self.current_song = song
            self.is_playing = True
            self.display_msg(f"playing {self.current_song['name']} by {self.current_song['artist']}")
            self.media_player.set_media(self.vlc_instance.media_new(self.current_song['path']))
            self.media_player.play()
           

    def stop_video(self) -> None:
        """Stops the current music video."""
        self.display_msg("Music stopped, please make a new reqest...")    
        self.current_song = None
        self.is_playing = False
        self.media_player.stop()


    def find_best_match(self, request: str) -> List[str]:
        """Finds the best match of all song.
        Each available song gets a score by number of matches with request / total matches.
        Args:
            request (str): song request. 
        Returns:
            List[str]: returns the best scored matched song, if none found returns None;    
        """
        # best_match = (None, 0)  # best_match = (song, score
        best_song = None
        best_score = 0
        request_list = {s.lower() for s in request.split()}
        for song in self.songs_by_name.values():
            num_of_mathces = len(request_list.intersection(song["matches"]))
            score = num_of_mathces / len(song["matches"])
            if score > best_score:
                best_song= song
                best_score = score
        return best_song


    def display_msg(self, msg: str) -> None:
        """Displayes the given message.
        Args:
            msg (str): the message.
        """
        if  msg != self.current_msg:
            if self.is_available_songs_displayed:
                self.delete_msg(len(self.songs_by_name)+3)
            else:
                self.delete_msg(1)  
            self.is_available_songs_displayed = False    
            self.current_msg = msg   
            print(self.current_msg)


    def delete_msg(self, num_of_line: int) -> None:
        """Deletes the last lines printed.
        Args:
            num_of_lines (int): number of lines to delete.
        """
        for _ in range(num_of_line):
            print("\033[A{}\033[A".format(' '*80))  


    def display_available_songs(self) -> None:
        """Display all the song the jukebox can play"""
        self.delete_msg(1)
        print("The available songs are:")
        for idx, song in enumerate(self.songs_by_name.values()):
            name, artist = song["name"], song["artist"]
            print(f"{idx+1}. {name} by {artist}") 
        print("\nWaiting for a song request...") 


    def run(self) -> None:
        """Starts the jukebox."""
        thread = threading.Thread(target=self.main_loop)
        thread.daemon = True
        thread.start()
        while(True):
            if input() == 'q':
                sys.exit()
                

    def main_loop(self):
        """Main loop.
        This method runs in the background ask checks changing in the adafruit io feed,
        triggred by a voice command. 
        """
        old_request = None
        while(True):
            feed_data = self.aio.receive(self.feed.key)
            song_request = feed_data.value
            # disply available songs
            if song_request == "@display_songs" and not self.is_available_songs_displayed:
                if self.is_playing:
                     self.stop_video()
                self.display_available_songs()
                self.is_available_songs_displayed = True
            # stop video song
            elif song_request == "Null":
                if self.is_playing: 
                    self.stop_video()  
                else:
                     self.display_msg("Waiting for a song request...")    
            # play video song    
            elif song_request != "@display_songs" and song_request != old_request:
                self.play_video(song_request)
                old_request = song_request


    def __del__(self):
        """Releases the media player instace when the jukebox is destoyed."""
        self.media_player.release()
                         
        
if __name__ == "__main__":

    # Configures your private Adafruit details
    with open("adafruit_config.json", 'r') as f:
            config = json.load(f)       
            ADAFRUIT_IO_KEY = config["ADAFRUIT_IO_KEY"]
            ADAFRUIT_IO_USERNAME = config["ADAFRUIT_IO_USERNAME"] 
            AIO_FEED_ID = config["AIO_FEED_ID"] 

    jukebox = Jukebox("songs_data.json")
    jukebox.run()


   

