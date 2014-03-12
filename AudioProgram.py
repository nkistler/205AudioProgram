#!/usr/bin/python
import re, os, sys, random, pygame
from pygame.locals import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

#global variables
allFileNamesSet= set()
artistList = []
genreList = []
homeDir = "/home/nathan/workspace/AudioProgram/Audio/"
homeDirList = os.listdir(homeDir)
selection = ""

#initialize globals
for entry in homeDirList:
    if re.search(r'.mp3', entry):
        allFileNamesSet.add(entry) #This gives us a non-empty playlist to start with before we even enter our preferences.
pygame.init()
pygame.mixer.init()

def play():
     #randomize the sample of music
    randomizedSample = set()
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
            print "Enter command \"stop\" to stop player, \"next\" to skip to next track, or \"quit\" to exit."
            selection = raw_input("Please enter command: ")
            print "You entered ", selection
            if selection.strip().lower()=='stop':
                pygame.mixer.music.stop()
                return
            elif selection.strip().lower()=='next':
                if len(randomizedSample) == 0:
                    print "Error: End of playlist"
                else:
                    print "Current track: " + randomizedSample[len(randomizedSample)-1]
                    break
            elif selection.strip().lower()=='quit':
                sys.exit()
            else:
                print "Error: Invalid command"   
    return

def select():
    #take input
    artist = ""
    genre = ""
    while artist.strip().lower() != 'done':
        artist = raw_input("Enter artist name or enter command \"done\": ")
        if artist.strip().lower() != 'done':
            artistList.append(artist.strip().lower())
    while genre.strip().lower() != 'done':
        genre = raw_input("Enter genre name or enter command \"done\": ")
        if genre.strip().lower() != 'done':
            genreList.append(genre.strip().lower())
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
            artistTags = ID3(homeDir + entry).getall('TPE1') + ID3(homeDir + entry).getall('TPE1')
            genreTags = ID3(homeDir + entry).getall('TCON')
            artistTag1 = str(artistTags[0])
            artistTag2 = str(artistTags[1])
            genreTag1 = str(genreTags[0])

            #check tags against user created lists
            for item in artistList:
                if item in (artistTag1.lower(), artistTag2.lower()):
                    allFileNamesSet.add(entry)
            for item in genreList:
                if item in (genreTag1.lower()):
                    allFileNamesSet.add(entry)
    return

#main program loop
while selection.strip().lower() != 'quit':
    print "Enter command \"select\" to select music preferences, \"play\" to begin to play music, or \"quit\" to exit."
    selection = raw_input("Please enter command: ")
    print "You entered ", selection
    if selection.strip().lower()=='play':
        play() #plays files which match current criteria
    elif selection.strip().lower()=='select':
        select() #allows user to modify current audio generation criteria
    elif selection.strip().lower()=='quit':
        pass
    else:
        print "Error: Invalid command"
