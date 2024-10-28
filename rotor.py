import pygame
import random
import string


class Rotor:
    def __init__(self, seed=-1, rotorNumber=None):
        if seed != -1:
            random.seed(seed)
        arr = list(range(26))
        random.shuffle(arr)
        self.map = arr
        self.rotorNumber = rotorNumber
        self.rotorToString()

    def forward(self, inputIndex):
        outputIndex = self.map[inputIndex]
        return outputIndex

    def backward(self, inputIndex):
        outputIndex = self.map.index(inputIndex)
        return outputIndex

    def rotorToString(self):
        print(f"Rotor {self.rotorNumber} with mapping:")
        print(self.map)

    def rotateTowards(self):
        last = self.map.pop()
        self.map.insert(0, last)

    def rotateAway(self):
        first = self.map.pop(0)
        self.map.append(first)
