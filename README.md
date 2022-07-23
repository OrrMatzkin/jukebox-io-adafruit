<!-- PROJECT LOGO (light) -->
![GitHub-Mark-Light](https://github.com/OrrMatzkin/jukebox-io-adafruit/blob/main/readme_assets/jukebox-title-trans-white.png?raw=true#gh-light-mode-only)

![GitHub-Mark-Dark](https://github.com/OrrMatzkin/jukebox-io-adafruit/blob/main/readme_assets/jukebox-title-trans-black.png?raw=true#gh-dark-mode-only)


<div align="center">
<div align="center">

  <p align="center">
    A modern partially automated music-playing program
    activted by Google Assistant </p>
</div>

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/navendu-pottekkat/awesome-readme?include_prereleases)
![GitHub last commit](https://img.shields.io/github/last-commit/orrmatzkin/jukebox-io-adafruit?color=orange)
![GitHub issues](https://img.shields.io/github/issues/orrMatzkin/jukebox-io-adafruit?color=yellow)
![GitHub pull requests](https://img.shields.io/github/issues-pr/orrmatzkin/jukebox-io-adafruit?color=yellow)
![GitHub repo size](https://img.shields.io/github/repo-size/orrmatzkin/jukebox-io-adafruit)
![GitHub](https://img.shields.io/github/license/orrMatzkin/jukebox-io-adafruit)

<a href="https://www.youtube.com/watch?v=LN7XRFX31c0">View Demo</a> ·
    <a href="https://github.com/OrrMatzkin/jukebox-io-adafruit/issues">Report Bug</a> ·
    <a href="https://github.com/OrrMatzkin/jukebox-io-adafruit/issues">Request Feature</a>
</div>

## About the project


jukebox is a CLI program for playing music videos using Google assistant command from any compatible device such Android phone, Google Home, etc.

I originally design and wrote this program for playing songs on my grandfather old analog CRT TV with a Raspberry pi, controlling it only with my Google Home Mini.

You can see the full article about this project on ..[fill missing]! 

## Table of context
- [Demo](#demo)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Run Locally](#run-locally)   
- [Features](#features)        
- [Adding new Music Videos](#adding-new-music-videos)    
       

## Demo
[![Everything Is AWESOME](https://lh3.googleusercontent.com/4v7ch66v8BYeY9QYbfLwJ648DvfjNm6FOjuk1HPm8bd9lTP-885J3Cgfv8h7xZSAud8GWwcwB4UFyNd899XLb1-Ag-oHQnksk-zGRIrBBUKQErbibalEW-u0aO1bdL-66OuL5sLLh4fLJWn2bwq_MURTPeYovAUIc4evotGOTOKaFhRt9rBUzaxywrPSINR-Z7wGMRytZs6BB_kL4S0XCayqUxkZ1WIfpYrWz2TfnPwS0paVsme8gq-6vB0beIg1zsh0M_7H4JZZt0phci9ASnuYa_qxC7CjyFLbx5Ljqpz0DUe3j_FwZooFhp9-9stT2QC4HwOgastcZWFcgjzUb6hk4M1SVVDST7X48PU24j61xQL8lDxdyy28DFuDcusnbJAM0_bumlxM2bGKrCRF4FJv4c2lE2VM9-UhmVq4u5A9lSoLF51cvPPliMruSXO_FcySasmECxEg92Q0_x5d2PqF3NClxGy8nPI5DymCua5ZrDWv7i6JuDSkMhU82F4UTGIUfHV4EbEkiTJPnqR5K5hxUYzZxmMtiMtY41giUQ6nmnb4kEzmWbKRX47mwnftllfhPxpLehnBzhhi_9Ugm-mTwARjQi7BGFmUIlI4LzgKHevNtB5tihDWw5QuISlLT7by-aqpu5JoMl4fq3ounHfe9SMst8eJI4OxCjYORvsn0eWErvNUSGXnMT92ElFNiC2jNeV_y3eHU8CEblw39NZKUymHF1jtGAnbbHE6kUvx7wkZzDAJFO2-rxBvLqRTKJKHeZ8iL0WkDkQWE1SW8srQSL2TTfYQTw=w2308-h1730-no?authuser=0)](https://www.youtube.com/watch?v=LN7XRFX31c0 "JUKEBOX DEMO")

<p align="right">(<a href="#about-the-project">back to top</a>)</p>


## Requirements

jukebox requires the followin to run:

- Python 3.7.3+
  - python-vlc 3.0.12118+
  - adafruit-io 2.5.0+
- VLC media player 3.0.12+
- Adafruit IO Account 
- IFTT Account
- Google Assistance (Any access)

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

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


### Run Locally

Go to the project directory

```bash
 cd jukebox-io-adafruit
```

Start the the program

```bash
 python3 jukebox.py
```

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

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

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

## Adding new Music Videos

This Repo comes with 6 (great) song:

1. David Bowie - Space Oddity.mp4
2. Louis Armstrong - What a Wonderful World.mp4
3. Marvin Gaye Tammi Terrell - Aint No Mountain High Enough.mp4
4. Oasis - Wonderwall.mp4
5. Roy Orbison - You Got It.mov
6. The Police - Every Breath You Take.mp4

To add a new song follow this steps:

1. Download your favorite music video. *
2. Rename the file to "\<Artist Name\> - \<Song Name\>.\<FIle Format\>" (see exmaple above).
4. Move the file to the `songs` directory.
3. Add the song details in `songs_data.json`
   ```json
   {
        "id": 0,
        "name": "<Song Name>",
        "artist": "<Artist Name>",
        "path": "<Path to song fille>",
        "matches": ["<match1>", "<match2>", "<match3>", "<match4>",...]
    }
   ```

\* VLC supports: ASF, AVI, FLAC, FLV, Fraps, Matroska, MP4, MPJPEG, MPEG-2 (ES, MP3), Ogg, PS, PVA, QuickTime File Format, TS, WAV, WebM

\*\* The Matches field is how a song is picked after a voice command. For an example check the given `songs_data.json` file

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

## Copyright

MIT License

Copyright (c) 2022 OrrMatzkin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
