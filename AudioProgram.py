#!/usr/bin/python
import glob, re, os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TCON

def play():
    return

def select():

    #variables that persist within scope of function
    allFileNamesList = []
    totalNumberOfFiles = 0
    homeDir = "/home/nathan/workspace/AudioProgram/Audio/"
    homeDirList = os.listdir(homeDir)

    #take input
    artist = raw_input("Enter Artist name: ")
    genre = raw_input("Enter Genre name: ")

    #perform search
    for entry in homeDirList:
    	if re.search(r'.mp3', entry):
            genreTag = ID3(homeDir + entry).getall('TCON')
            artistTag = ID3(homeDir + entry).getall('TPE1') + ID3(homeDir + entry).getall('TPE1')
            if genre in [genreTag[0]]:
                allFileNamesList.insert(totalNumberOfFiles, entry)
	        totalNumberOfFiles=totalNumberOfFiles+1
            if artist in [artistTag[0]]:
                allFileNamesList.insert(totalNumberOfFiles, entry)
	        totalNumberOfFiles=totalNumberOfFiles+1
            if artist in [artistTag[1]]:
                allFileNamesList.insert(totalNumberOfFiles, entry)
	        totalNumberOfFiles=totalNumberOfFiles+1
            print allFileNamesList
    return
    

#main program loop
selection = ""
while selection.strip() != 'quit':
    print "Press 1 to play"
    print "Press 2 to select"
    selection = raw_input("Please enter command: ")
    print "You entered ", selection
    if selection=="1":
        play() #executes rotate function
    elif selection=="2":
        select() #executes create thumbnail function
