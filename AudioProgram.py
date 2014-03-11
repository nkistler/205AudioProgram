#!/usr/bin/python
import glob, re, os, random, pygame, sys, Buttons
from pygame.locals import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

class AudioPlayer:
    def __init__(self):
        self.main()
    
    #Create a display
    def display(self):
        self.screen = pygame.display.set_mode((650,370),0,32)
        pygame.display.set_caption("Audio Player")

    #Update the display and show the button
    def update_display(self):
        self.screen.fill((30,144,255))
        #Parameters: surface, color, x, y, length, height, width, text, text_color
        self.Button1.create_button(self.screen, (107,142,35), 150, 135, 100, 50, 0, "Play", (255,255,255))    
        self.Button2.create_button(self.screen, (107,142,35), 275, 135, 100, 50, 0, "Skip", (255,255,255))
        self.Button3.create_button(self.screen, (107,142,35), 400, 135, 100, 50, 0, "Stop", (255,255,255))
        pygame.display.flip()


    #Run the loop
    def main(self):
        self.Button1 = Buttons.Button()
        self.Button2 = Buttons.Button()
        self.Button3 = Buttons.Button()
        self.display()
        while True:
            self.update_display()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        while len(randomizedSample) > 0: 
                            #Play the file
                            pygame.init()
                            pygame.mixer.init()
                            pygame.mixer.music.load("Audio/" + randomizedSample.pop())
                            pygame.mixer.music.play(0)
                            print "Play"
                    elif self.Button2.pressed(pygame.mouse.get_pos()):
                        print "Skip"
                    elif self.Button3.pressed(pygame.mouse.get_pos()):
                        print "Stop"


def generate():
     #randomize the sample of music
    randomizedSample = random.sample(allFileNamesSet, len(allFileNamesSet))
    
    print "Playlist:"
    for item in reversed(randomizedSample):
        print item

    #initialize GUI
    if __name__ == '__main__':
        obj = AudioPlayer()
    return   

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
