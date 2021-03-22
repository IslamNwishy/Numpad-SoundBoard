# Numpad Soundboard

A program that maps the numpad to any sounds of your choice to be used as a simple soundboard. (Direct Download [Here](https://downgit.github.io/#/home?url=https://github.com/IslamNwishy/Numpad-SoundBoard/tree/main/dist))

## How to use it

- This program is intended for Windows only (been tested on Windows 10 only)
- In the dist folder you will find an exe file named `SoundBoard.exe` and a folder named `sounds`
- In the `sounds` folder place your desried sound files, a max of 9 sounds will be used for numpad numbers 1 to 9. (see [pygame mixer music](http://www.pygame.org/docs/ref/music.html) for the supported audio types)
- Run `SoundBoard.exe` it should map keys on its own and start a simple interface with buttons indecating the number in the numpad that the crossponding sound is mapped to.
- **You do not have to keep the window in focus** it will capture the keys pressed regardless.
- The board will only function when the **numlock** is on (when you cannot type numbers)
- Number 0 is reserved for stoping any sound playing
- Pressing on a key while its mapped sound is playing will stop the sound (Like pressing 0)
- Pressing a key while its sound is not playing will stop any sound playing to play its own.

## How to run the code

- Make sure you have python3 and pip installed
- create a virtual enviroment using whatever method you want
- activate the enviroment
- use `pip install -r requirements.txt` to install all the nessecary libraries
- run the python program normally with `python SoundBoard.py` or whichever method you are used to

## What it does not do yet

- There is no way to map sounds to the keys you want other than naming the audio files to be alphabitically the order you want.
- Have decent interface.

## Notes

This program was made for fun. You are free to use it whatever way you want just be cautious that i have not tested it all that much and did not bother with error checking most things.
