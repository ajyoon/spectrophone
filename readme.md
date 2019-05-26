# THIS REPOSITORY IS DEPRECATED

This instrument has been rewritten and significantly improved (including real-time performance, live video input, and much much more) and lives now at [https://gitlab.com/ajyoon/spectrophone](https://gitlab.com/ajyoon/spectrophone). I'm leaving this repo around just to not break links (and to allow reproduction of [the transistorized radio](https://youtu.be/eO98X3JIC48)).

# spectrophone

an electronic instrument which interprets images as sound with oscillators and samplers

### setup

the initial implementation was built in order to create a piece of sound called [the transistorized radio](https://youtu.be/eO98X3JIC48). for now, some additional (small) changes would be required to decouple the current implementation from the piece into one that can be reused for other purposes. the following instructions are for setting up _the transistorized radio_.


1. ensure python 3 is installed (and preferably you are using a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)).
1. install dependencies with `pip3 install -r requirements.txt`
1. download resources [here](https://drive.google.com/open?id=0B-7cpH1IckNMeDVNbWYwQktHeHc) and place them in a top-level directory `resources`.
1. run the script with `python3 the_transistorized_radio_main.py`

to build the score-video:

1. `python3 visualize/main.py`
2. use ffmpeg or whatever tools you prefer to add the output audio to the video.



