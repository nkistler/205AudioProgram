#!/usr/bin/python
#needed libraries
import re, os, sys, random, pygame
from pygame.locals import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

#global variables
selectedFilePathsSet= set()
userArtistList = []
userGenreList = []
homeDir = "/home/nathan/Music" #DO NOT include trailing slash
homeDirList = list()
selection = ""

#initialize globals
#this starts our audio modules
pygame.init()
pygame.mixer.init()

#This allows us to recursively search our "home" directory. Places all possible audio file paths in homeDirList.
def getAllHomeFolder(x, dir_name, files): 
    for item in files:
        if re.search(r'.mp3', item):
            homeDirList.append(dir_name + "/" + item)
os.path.walk(homeDir, getAllHomeFolder, 0)

#This gives us a non-empty playlist to start with before we even enter our preferences
for entry in homeDirList:
    if re.search(r'.mp3', entry):
        selectedFilePathsSet.add(entry) 


#main functions
def play():
     #randomize the sample of music
    randomizedSample = set()
    randomizedSample = random.sample(selectedFilePathsSet, len(selectedFilePathsSet))

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
        pygame.mixer.music.load(randomizedSample.pop())
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
                    artistTag = getArtistTag(nameOfCurrentFile)
                    titleTag = getTitleTag(nameOfCurrentFile)
                    genreTag = getGenreTag(nameOfCurrentFile)
                    print "Current track: " +  artistTag + ", " + titleTag + ", " + genreTag
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
    selectedFilePathsSet.clear()

    #perform search
    for entry in homeDirList:
        #check if the file is in fact an audio file
    	if re.search(r'.mp3', entry):
            #get ID3 tags from file
            artistTag = getArtistTag(entry)
            genreTag = getGenreTag(entry)

            #check tags against user created lists
            for item in userArtistList:
                if (re.search(item, artistTag.lower())):
                    selectedFilePathsSet.add(entry)
            for item in userGenreList:
                if re.search(item, genreTag.lower()):
                    selectedFilePathsSet.add(entry)
    return

#getters and setters
def getArtistTag(pathName):
    artistTag = ID3(pathName).getall('TPE1')
    if (artistTag):
        return str(artistTag[0])
    else:
        return ""

def getGenreTag(pathName):
    genreTag = ID3(pathName).getall('TCON')
    if (genreTag):
        return str(genreTag[0])
    else:
        return ""

def getTitleTag(pathName):
    titleTag = ID3(pathName).getall('TIT2')
    if (titleTag):
        return str(titleTag[0])
    else:
        return ""

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
