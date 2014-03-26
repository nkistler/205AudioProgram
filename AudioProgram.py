#!/usr/bin/python

#Program to randomize the playback of some audio files, based on input from the user. This is meant to provide "jukebox" functionality.

#needed libraries
import re, os, pygame, random, sys, time 
from pygame.locals import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

#global variables
selectedFilePathsSet= set()
userArtistList = []
userGenreList = []
homeDir = "/home/nathan/Music" #This is where your music directory is set. DO NOT include trailing slash, and DO include full pathname.x
homeDirList = list()
currentTrack = ""
selection = ""
volume = 1


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
    printPlaylist(randomizedSample)

    #localize variable
    global currentTrack
    selection = ""

    #start playback and ask for next input
    while len(randomizedSample) > 0:
        setCurrentTrack(randomizedSample[len(randomizedSample)-1])
        printCurrentTrack(currentTrack)
        pygame.mixer.music.load(randomizedSample.pop())
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(volume)
        while pygame.mixer.music.get_busy():
            playerInput(randomizedSample)   
    return

#This function takes input from user to define our selection preferences.
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

#This module is run as the player is playing, and allows for the user to enter commands modifying the playback.
def playerInput(playList):
    global volume
    selection = ""
    selection = raw_input("Please enter a command (\"help\" will list available commands): ")
    print "You entered ", selection
    if selection.strip().lower()=='help':
        print "\"down\"\tThis command adjusts the volume on the playback down one unit on a ten unit scale."
        print "\"info\"\tThis command prints out the track information."
        print "\"next\"\tThis command skips to the next track on the playlist."
        print "\"quit\"\tThis command exits the program."
        print "\"stop\"\tThis command stops the playback and destroys the playlist."  
        print "\"up\"\tThis command adjusts the volume on the playback up one unit on a ten unit scale."     
    elif selection.strip().lower()=='stop':
        pygame.mixer.music.stop()
        main()
    elif selection.strip().lower()=='info':
        printCurrentTrack(currentTrack)
    elif selection.strip().lower()=='next':
        if len(playList) == 0:
            print "Error: End of playlist"
        else:
            pygame.mixer.music.stop()
            return
    elif selection.strip().lower()=='up':
        setVolume(volume + 0.1)
        pygame.mixer.music.set_volume(volume)
        print "Volume: " + str(volume*10)
        playerInput(playList)
    elif selection.strip().lower()=='down':
        setVolume(volume - 0.1)
        pygame.mixer.music.set_volume(volume)
        print "Volume: " + str(volume*10)
        playerInput(playList)
    elif selection.strip().lower()=='quit':
        sys.exit()
    else:
        print "Error: Invalid command"
        playerInput(playList)        
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

def setVolume(vol):
    global volume
    if vol>1.0:
        print "Error: Max volume"
        volume=1.0
    elif vol<0.0:
        print "Error: Min volume"
        volume=0.0
    else:
        volume = vol
    return

def setCurrentTrack(pathName):
    global currentTrack
    currentTrack = pathName
    return
    

#print functions
def printCurrentTrack(pathName):
    artistTag = getArtistTag(pathName)
    titleTag = getTitleTag(pathName)
    genreTag = getGenreTag(pathName)
    print "Current track: " +  artistTag + ", " + titleTag + ", " + genreTag
    return

def printDetailedTrackInfo(pathName):
    artistTag = getArtistTag(pathName)
    titleTag = getTitleTag(pathName)
    genreTag = getGenreTag(pathName)
    print "Track info: " +  artistTag + ", " + titleTag + ", " + genreTag
    return

def printPlaylist(playlist):
    print "Playlist:"
    for item in reversed(playlist):
        #get ID3 tags from file
        artistTag = getArtistTag(item)
        titleTag = getTitleTag(item)
        genreTag = getGenreTag(item)
        print artistTag + ", " + titleTag + ", " + genreTag
    return


#main program loop
def main():
    selection = ""
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

main()
