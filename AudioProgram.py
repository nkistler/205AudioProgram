#!/usr/bin/python
import glob, re, os, random, pygame
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
print allFileNamesSet
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
        pygame.mixer.music.load("Audio/" + randomizedSample.pop())
        pygame.mixer.music.play(0)
        while pygame.mixer.music.get_busy():
            selection = raw_input("Please enter command: ")
            if selection=='stop':
                pygame.mixer.music.stop()
                return
            elif selection=='next':
                break    
            else:
                print "Invalid selection"   
    return

def select():
    #take input
    artist = raw_input("Enter Artist name: ")
    genre = raw_input("Enter Genre name: ")

    #empty the current set
    allFileNamesSet.clear()

    #perform search
    for entry in homeDirList:
    	if re.search(r'.mp3', entry):
            genreTag = ID3(homeDir + entry).getall('TCON')
            artistTag = ID3(homeDir + entry).getall('TPE1') + ID3(homeDir + entry).getall('TPE1')
            if genre in [genreTag[0]]:
                allFileNamesSet.add(entry) 
            if artist in [artistTag[0]]:
                allFileNamesSet.add(entry)
            if artist in [artistTag[1]]:
                allFileNamesSet.add(entry)
    print allFileNamesSet
    return

#main program loop
while selection.strip() != 'quit':
    print "Press 1 to generate audio"
    print "Press 2 to select audio criteria"
    selection = raw_input("Please enter command: ")
    print "You entered ", selection
    if selection=="1":
        generate() #plays files which match current criteria
    elif selection=="2":
        select() #allows user to modify current audio generation criteria
    elif selection=='quit': { }
    else:
        print "Invalid selection"
