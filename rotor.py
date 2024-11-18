import pygame
import random
import string


class Rotor:
    def __init__(self, seed=-1, rotorNumber=None):
        
        self.seed = seed                # set seed
        self.setPosition(0)             # set rotation
        self.rotorNumber = rotorNumber  # set number

        # self.rotorToString() # print

    # path through the rotors before signal reaches reflector
    def forward(self, inputIndex):
        outputIndex = self.map[inputIndex]  # get the value at the input 
        return outputIndex

    # path through the rotors after signal reaches reflector
    def backward(self, inputIndex):
        outputIndex = self.map.index(inputIndex) # get index of the input
        return outputIndex

    # prints the rotors mapping
    def rotorToString(self):
        print(f"Rotor {self.rotorNumber} with mapping:")
        print(self.map)

    # rotate down: towards viewer
    def rotateTowards(self):
        last = self.map.pop()
        self.map.insert(0, last)
        for i in range(len(self.map)):
            if self.map[i] == 25:
                self.map[i] = 0
            else:
                self.map[i] += 1

    # rotate up: away from viewer
    def rotateAway(self):
        first = self.map.pop(0)
        self.map.append(first)
        for i in range(len(self.map)):
            if self.map[i] == 0:
                self.map[i] = 25
            else:
                self.map[i] -= 1

    # to set the rotor position
    def setPosition(self, pos):
        pos = pos % 26

        # set seed
        if self.seed != -1:
            random.seed(self.seed)

        arr = list(range(26))
        random.shuffle(arr)
        self.map = arr

        for _ in range(pos):
            self.rotateAway()
