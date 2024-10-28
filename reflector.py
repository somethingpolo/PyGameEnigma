import random
import string


class Reflector:
    def __init__(self, seed=-1):
        if seed != -1:
            random.seed(seed)
        arr = list(range(26))
        self.map = [None] * 26
        for i in range(len(arr)):
            if self.map[i] == None:

                while (True):
                    target = random.sample(arr, 1)[0]
                    if target != i:
                        break
                self.map[i] = target
                self.map[target] = i
                arr.pop(arr.index(target))
                arr.pop(arr.index(i))
        self.reflectorToString()

    def enter(self, inputIndex):
        outputIndex = self.map[inputIndex]
        return outputIndex

    def reflectorToString(self):
        print(f"Reflector with mapping:")
        print(self.map)
