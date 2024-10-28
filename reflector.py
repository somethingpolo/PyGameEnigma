import random
import string


class Reflector:
    def __init__(self, seed=-1):
        # set seed
        if seed != -1:
            random.seed(seed)
        
        # set the plug board
        arr = list(range(26))
        self.map = [None] * 26
        for i in range(len(arr)):
            if self.map[i] == None:

                # ensure don't map to self
                while (True):
                    target = random.sample(arr, 1)[0]
                    if target != i:
                        break

                # apply the corresponding links
                self.map[i] = target
                self.map[target] = i
                arr.pop(arr.index(target))
                arr.pop(arr.index(i))
        self.reflectorToString()

    # reflect the signal
    def enter(self, inputIndex):
        outputIndex = self.map[inputIndex]
        return outputIndex
    
    def reflectorToString(self):
        print(f"Reflector with mapping:")
        print(self.map)
