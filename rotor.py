import pygame
import random
import string


class Rotor:
    def __init__(self, seed=-1, rotorNumber=None):
        # set seed
        if seed != -1:
            random.seed(seed)

        arr = list(range(26))
        random.shuffle(arr)
        self.map = arr
        self.rotorNumber = rotorNumber
        self.rotorToString()

    # the forward path, where the key is pressed
    def forward(self, inputIndex):
        outputIndex = self.map[inputIndex]  # get the value at the input 
        return outputIndex

    # return path to light up the return key
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

    # rotaate up: away from viewer
    def rotateAway(self):
        first = self.map.pop(0)
        self.map.append(first)
        for i in range(len(self.map)):
            if self.map[i] == 0:
                self.map[i] = 25
            else:
                self.map[i] -= 1
