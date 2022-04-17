<!-- PROJECT LOGO (light) -->
![GitHub-Mark-Light](https://github.com/OrrMatzkin/jukebox-io-adafruit/blob/main/readme_assets/jukebox-title-trans-white.png?raw=true#gh-light-mode-only)
![GitHub-Mark-Dark](https://github.com/OrrMatzkin/jukebox-io-adafruit/blob/main/readme_assets/jukebox-title-trans-black.png?raw=true#gh-dark-mode-only)
 <br />
<!-- <div align="center">
  <a href="https://github.com/OrrMatzkin/jukebox-io-adafruit">
    <img src="https://github.com/OrrMatzkin/jukebox-io-adafruit/blob/main/readme_assets/jukebox-title-trans-white.png?raw=true#gh-light-mode-only" alt="Logo" >
  </a> -->

<!-- PROJECT LOGO (dark) -->
<!-- <div align="center"> -->
  <!-- <a href="https://github.com/OrrMatzkin/jukebox-io-adafruit">
    <img src="https://github.com/OrrMatzkin/jukebox-io-adafruit/blob/main/readme_assets/jukebox-title-trans-black.png?raw=true#gh-dark-mode-only" alt="Logo" >
  </a> -->

  <p align="center">
    A modern partially automated music-playing program
    activted by Google Assistant </p>
<!-- </div> -->

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/navendu-pottekkat/awesome-readme?include_prereleases)
![GitHub last commit](https://img.shields.io/github/last-commit/orrmatzkin/jukebox-io-adafruit?color=orange)
![GitHub issues](https://img.shields.io/github/issues/orrMatzkin/jukebox-io-adafruit?color=yellow)
![GitHub pull requests](https://img.shields.io/github/issues-pr/orrmatzkin/jukebox-io-adafruit?color=yellow)
![GitHub repo size](https://img.shields.io/github/repo-size/orrmatzkin/jukebox-io-adafruit)
![GitHub](https://img.shields.io/github/license/orrMatzkin/jukebox-io-adafruit)

<a href="https://github.com/github_username/repo_name">View Demo</a> ·
    <a href="https://github.com/OrrMatzkin/jukebox-io-adafruit/issues">Report Bug</a> ·
    <a href="https://github.com/OrrMatzkin/jukebox-io-adafruit/issues">Request Feature</a>
</div>

## About the project


jukebox is a CLI program for playing music videos using Google assistant command from any compatible device such Android phone, Google Home, etc.

I originally design and wrote this program for playing songs on my grandfather old analog CRT TV with a Raspberry pi, controlling it only with my Google Home Mini.

You can see the full article about this project on ..[fill missing]! 

## Demo




## Requirements

jukebox requires the followin to run:

- Python 3.7.3+
  - python-vlc 3.0.12118+
  - adafruit-io 2.5.0+
- VLC media player 3.0.12+
- Adafruit IO Account 
- IFTT Account
- Google Assistance (Any access)


## Getting Started

Disclaimer: There is quite a lot of things that jukebox needs for running, and there is more then one way to configure it. This is how I choose to connect everything together. 

You might find more detiles about how to make it all work in this article -> [fill missign]


### Prerequisites

#### Adafruit 

1. Create a free account at [Adafruit IO](https://accounts.adafruit.com/users/sign_in).
2. Create a new feed:
    - Turn Feed History off.
    - Remember it's name.
3. Generate an Adafruit IO Key   

#### IFTTT

1. Create a free account at [IFTTT](https://ifttt.com).
2. Create at least 3 applets trigged by Google Assistant, which sends data to Adafruit:
    - For starting playing a music video.
    - For stopping a music video.
    - For displaying the jukebox available songs

Again, to see an exaple check this article -> [fill missign].


### Installation

1. Clone the repo
   ```bash
   git clone https://github.com/OrrMatzkin/jukebox-io-adafruit.git
   ```
2. Install the required packages
   ```bash
   pip3 install python-vlc
   pip3 install pip install adafruit-io
   ```
3. Enter your Adafruit details in `adafruit_config.json`
   ```json
    "ADAFRUIT_IO_KEY": "<YOUR ADAFRUIT IO KEY>",
    "ADAFRUIT_IO_USERNAME": "<YOUR ADAFRUIT IO USERNAME>",
    "AIO_FEED_ID": "<YOUR ADAFRUIT IO FEED NAME>" 
   ```
4. Make sure your device (Raspberry pi) is connected to a monitor and a set of speakers.

<p align="right">(<a href="#top">back to top</a>)</p>

### Run Locally

Go to the project directory

```bash
 cd jukebox-io-adafruit
```

Start the the program

```bash
 python3 jukebox.py
```

## Features

- [x] Play/stop local video songs
- [x] Show available songs
- [ ] Increase/decrease volume
- [ ] Play/stop youtube video songs (pafy integratiion)
- [ ] Create and play a playlist of songs
  - [ ] By artist name
  - [ ] By a preloaded playlist 
- [ ] Remove the need for a json data file
- [ ] A Better score mechanism for songs
- [ ] A "hard" integrated assistant control


See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).


