import sys
import json
import time
import pydirectinput
import os
import re
import random

# get json from https://sky-music.github.io/

verbose = False

def main():
    global verbose
    if len(sys.argv) < 2:
        print("Usage: main.py [option] (..arguments)")
        print("\tplay [json music file]\n\t-> Play a local music file\n")
        print("\tlist [search query]\n\t-> List local music files\n")
        print("\tauto\n\t-> Automatically play local music files in folder musics/\n")
        print("\t--verbose\n\tOutput extra information\n")
        exit(0)

    verbose = '--verbose' in sys.argv

    if sys.argv[1] == 'play':
        if len(sys.argv) < 3:
            print("Option play requires another argument")
            exit(0)

        play(sys.argv[2])

    elif sys.argv[1] == 'list':
        list()

    elif sys.argv[1] == 'auto':
        auto();

def auto():
    while True:
        files = os.listdir('./musics/')
        random.shuffle(files)

        print("Starting auto queue in 2 seconds!")
        time.sleep(2)
        for file in files:
            try:
                play(f"./musics/{file}", delay=0)

            except KeyboardInterrupt:
                input("Press [ENTER] to skip or [CTRL] + [C] to quit")

            except:
                print(f"[SKIP] Failed to play {file}")

def list():
    filter = '' if len(sys.argv) < 3 else sys.argv[2]

    files = os.listdir('./musics/')
    for file in files:
        if filter != '' and re.search(filter, file) is None:
            continue

        print(file)

def play(music_file, delay=2):
    with open(music_file, encoding="utf8") as f: # use UTF-8 encoding to open foreign language files
        data = json.load(f)

    song = data[0]
    bpm = song['bpm']
    bits_per_page = song['bitsPerPage']
    pitch_level = song['pitchLevel']

    notes = song['songNotes']
    length = get_length(notes)

    print(f"Name:          {song['name']}")
    print(f"BPM:           {bpm}")
    print(f"Bits per page: {bits_per_page}")
    print(f"Pitch level:   {pitch_level}")
    print(f"Duration:      {int(length / 60)}m {length % 60}s")


    print(f"\nPlaying in {delay} seconds!\n")
    time.sleep(delay)
    pydirectinput.PAUSE = 0.01

    seconds_between_beats = 60 / bpm
    first_time = notes[0]['time']
    current_beat = first_time

    current_index = 0
    while current_index < len(notes):
        executing_beat = notes[current_index]
        note_beat = int(executing_beat['time'])

        if note_beat > current_beat: # This note is in the future
            wait_time = note_beat - current_beat
            if verbose:
                print(f"WAIT for {int(wait_time)}ms")
            
            time.sleep(wait_time / 1000)
            current_beat += wait_time
            continue

        # This note should be played
        key = executing_beat['key']
        
        play_key(key)
        current_index += 1

def get_length(notes):
    start_time = int(notes[0]['time'])
    end_time = int(notes[-1]['time'])
    
    time = end_time - start_time
    return int(time / 1000)

def to_note(key):
    return f"{"ABC"[int(key / 5)]}{(key % 5) + 1}"

def play_key(key):
    # key structure is: 1KeyN where N: key from 0-14 left to right top to bottom
    key = int(key[4:])
    bindings = "yuiophjkl;nm,./"
    mapped = bindings[key]

    if verbose:
        print(f"PLAY note {to_note(key)}: press '{mapped}'")

    pydirectinput.press(mapped)

if __name__ == "__main__":
    main()
