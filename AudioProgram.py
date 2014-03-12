#!/usr/bin/python
import re, os, random, pygame
from pygame.locals import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

#global variables
allFileNamesSet= set()
randomizedSample = set()
homeDir = "/home/nathan/workspace/AudioProgram/Audio/"
homeDirList = os.listdir(homeDir)
selection = ""

#initialize globals
for entry in homeDirList:
    if re.search(r'.mp3', entry):
        allFileNamesSet.add(entry)
pygame.init()
pygame.mixer.init()

def generate():
     #randomize the sample of music
    randomizedSample = random.sample(allFileNamesSet, len(allFileNamesSet))

    #print playlist
    print "Playlist:"
    for item in reversed(randomizedSample):
        print item

    #localize variable
    selection = ""

    #start playback and ask for next input
    while len(randomizedSample) > 0:
        pygame.mixer.music.load(homeDir + randomizedSample.pop())
        pygame.mixer.music.play(0)
        while pygame.mixer.music.get_busy():
            print "Enter command \"stop\" to stop player, or \"next\" to skip to next track."
            selection = raw_input("Please enter command: ")
            print "You entered ", selection
            if selection=='stop':
                pygame.mixer.music.stop()
                return
            elif selection=='next':
                if len(randomizedSample) == 0:
                    print "Error: End of playlist"
                else:
                    print "Current track: " + randomizedSample[len(randomizedSample)-1]
                    break
            else:
                print "Error: Invalid command"   
    return

def select():
    #take input
    artist = ""
    genre = ""
    artistList = []
    genreList = []
    while artist != 'done':
        artist = raw_input("Enter artist name or enter command \"done\": ")
        if artist != 'done':
            artistList.append(artist)
    while genre != 'done':
        genre = raw_input("Enter genre name or enter command \"done\": ")
        if genre != 'done':
            genreList.append(genre)
    print "Current preferences:"
    print artistList
    print genreList

    #empty the current set
    allFileNamesSet.clear()

    #perform search
    for entry in homeDirList:
        #check if the file is in fact an audio file
    	if re.search(r'.mp3', entry):
            #get ID3 tags from file
            artistTag = ID3(homeDir + entry).getall('TPE1') + ID3(homeDir + entry).getall('TPE1')
            genreTag = ID3(homeDir + entry).getall('TCON')

            #check tags against user created lists
            for item in artistList:
                if item in (artistTag[0], artistTag[1]):
                    allFileNamesSet.add(entry)
            for item in genreList:
                if item in (genreTag[0]):
                    allFileNamesSet.add(entry)
    return

#main program loop
while selection.strip() != 'quit':
    print "Enter command \"select\" to select music preferences, \"play\" to begin to play music, or \"quit\" to exit the program."
    selection = raw_input("Please enter command: ")
    print "You entered ", selection
    if selection=='play':
        generate() #plays files which match current criteria
    elif selection=='select':
        select() #allows user to modify current audio generation criteria
    elif selection=='quit':
        pass
    else:
        print "Error: Invalid command"
