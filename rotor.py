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
        for i in range(len(self.map)):
            if self.map[i] == 25:
                self.map[i] = 0
            else:
                self.map[i] += 1

    def rotateAway(self):
        first = self.map.pop(0)
        self.map.append(first)
        for i in range(len(self.map)):
            if self.map[i] == 0:
                self.map[i] = 25
            else:
                self.map[i] -= 1
