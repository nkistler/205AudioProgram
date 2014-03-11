#!/usr/bin/python
import glob, re, os, random, pygame, sys
from pygame.locals import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
pygame.init()

def generate():
     #randomize the sample of music
    randomizedSample = random.sample(allFileNamesSet, len(allFileNamesSet))
    
    while len(randomizedSample) > 0:
        print "Playlist:"
        for item in reversed(randomizedSample):
            print item
        play(randomizedSample.pop())
    return

def play(fileName):
    #Play the file
    pygame.mixer.init() 
    pygame.mixer.music.load("Audio/" + fileName)
    pygame.mixer.music.play(1) 

def select():
    #take input
    artist = raw_input("Enter Artist name: ")
    genre = raw_input("Enter Genre name: ")

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
    else:
        print "Invalid selection"
