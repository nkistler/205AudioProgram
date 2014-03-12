#!/usr/bin/python
import re, os, sys, random, pygame
from pygame.locals import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

#global variables
allFileNamesSet= set()
userArtistList = []
userGenreList = []
homeDir = "/home/nathan/workspace/AudioProgram/Audio/"
homeDirList = os.listdir(homeDir)
selection = ""

#initialize globals
for entry in homeDirList:
    if re.search(r'.mp3', entry):
        allFileNamesSet.add(entry) #This gives us a non-empty playlist to start with before we even enter our preferences.
pygame.init()
pygame.mixer.init()

#main functions
def play():
     #randomize the sample of music
    randomizedSample = set()
    randomizedSample = random.sample(allFileNamesSet, len(allFileNamesSet))

    #print playlist
    print "Playlist:"
    for item in reversed(randomizedSample):
        #get ID3 tags from file
        artistTag = getArtistTag(item)
        titleTag = getTitleTag(item)
        genreTag = getGenreTag(item)
        print artistTag + ", " + titleTag + ", " + genreTag

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
                    nameOfCurrentFile = randomizedSample[len(randomizedSample)-1]
                    print "Current track: " + nameOfCurrentFile
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
            userArtistList.append(artist.strip().lower())
    while genre.strip().lower() != 'done':
        genre = raw_input("Enter genre name or enter command \"done\": ")
        if genre.strip().lower() != 'done':
            userGenreList.append(genre.strip().lower())
    print "Current preferences:"
    print userArtistList
    print userGenreList

    #empty the current set
    allFileNamesSet.clear()

    #perform search
    for entry in homeDirList:
        #check if the file is in fact an audio file
    	if re.search(r'.mp3', entry):
            #get ID3 tags from file
            artistTag = getArtistTag(entry)
            genreTag = getGenreTag(entry)

            #check tags against user created lists
            for item in userArtistList:
                if (re.search(item, artistTag.lower())): # Need to fix this, possibly has something to do with paces?
                    allFileNamesSet.add(entry)
            for item in userGenreList:
                if re.search(item, genreTag.lower()):
                    allFileNamesSet.add(entry)
    return

#getters and setters
def getArtistTag(fileName):
    artistTag = ID3(homeDir + fileName).getall('TPE1')
    return str(artistTag[0])

def getGenreTag(fileName):
    genreTag = ID3(homeDir + fileName).getall('TCON')
    return str(genreTag[0])

def getTitleTag(fileName):
    titleTag = ID3(homeDir + fileName).getall('TIT2')
    return str(titleTag[0])
    

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
