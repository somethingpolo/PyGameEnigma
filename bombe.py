from rotor import *
from reflector import *


def encode(plaintext, rArr, ref, counter):
    cIndexes = []
    for c in range(len(plaintext.upper())):
        cIndexes.append(list(string.ascii_uppercase).index(plaintext[c]))

    # forwards
    for r in range(len(rArr)):
        for c in range(len(cIndexes)):
            cIndexes[c] = rArr[r].forward(cIndexes[c])

    # reflector
    for c in range(len(cIndexes)):
        cIndexes[c] = ref.enter(cIndexes[c])

    # backwards
    for r in range(len(rArr)-1, -1, -1):
        for c in range(len(cIndexes)):
            cIndexes[c] = rArr[r].backward(cIndexes[c])

    # convert from indexes to string
    outputStr = ""
    for c in cIndexes:
        outputStr += string.ascii_uppercase[c]
    return outputStr

def rotateRotors(counter, rArr):
    counter += 1
    rArr[0].rotateAway()
    if counter % 26 == 0:
        rArr[1].rotateAway()
    if counter % (26 * 26) == 0:
        rArr[2].rotateAway()
    return counter


class Bombe:

    def __init__(self) -> None:
        self.rotor1 = Rotor(11, 1)
        self.rotor2 = Rotor(22, 2)
        self.rotor3 = Rotor(33, 3)
        self.reflector = Reflector(44)
        self.rotorArray = [self.rotor1, self.rotor2, self.rotor3]

        self.rotor_offsets = [0, 0, 0] # the current offsets

        # test settings
        # rotor_offsets = [4, 0, 10]
        self.cipher = "NYZMVYBKGIQVO" # HEYHELLOTHERE
        self.known = "HELLO"

        self.cipher = input("Enter ciphertext: ").strip().upper()
        self.known = input("Input known part: ").strip().upper()

        self.possible_settings = []

        self.find_crib()
        self.run()


    def run(self):
        print("Running Bombe...")
        while True:
            # test current offset
            self.test_offset()

            # go to next offset
            self.rotor_offsets[0] = (self.rotor_offsets[0] + 1) % 26
            if self.rotor_offsets[0] == 0:
                self.rotor_offsets[1] = (self.rotor_offsets[1] + 1) % 26
                if self.rotor_offsets[1] == 0:
                    self.rotor_offsets[2] = (self.rotor_offsets[2] + 1) % 26

            # end condition
            if self.rotor_offsets == [0, 0, 0]:
                print("Done!")

                if not self.possible_settings:
                    print("Error, nothing found !")

                for setting in self.possible_settings:
                    print("Setting: ", setting, " | ", self.print_plain(*setting))
                break


    def find_crib(self):
        self.crib_positions = []
        self.cipher_len = len(self.cipher)
        self.known_len = len(self.known)

        for i in range(self.cipher_len - self.known_len + 1):
            possible = True
            for j in range(self.known_len):
                # if maps to itself reject
                if self.cipher[i + j] == self.known[j]:
                    possible = False
                    break
            if possible:
                self.crib_positions.append(i)


    def test_offset(self):
        # go through each crib
        for start in self.crib_positions:
            # set start position
            self.rotor1.setPosition(self.rotor_offsets[0])
            self.rotor2.setPosition(self.rotor_offsets[1])
            self.rotor3.setPosition(self.rotor_offsets[2])

            self.counter = 0

            # match to start of crib
            for _ in range(start):
                self.counter = rotateRotors(self.counter, self.rotorArray)

            # is this setting good for the crib
            possible = True

            # go through each char of the known
            for i in range(self.known_len):
                c = self.cipher[start + i]  # actual cipher
                p = self.known[i]           # known plain
                # cipher after running plain through machine
                c_found = encode(
                    p,
                    self.rotorArray, 
                    self.reflector, 
                    self.counter
                )

                if (c_found != c):
                    # not correct
                    possible = False
                    break
                
                # next position for next char
                rotateRotors(0, self.rotorArray)

            if possible:
                print("Possible setting: ", self.rotor_offsets)
                self.possible_settings.append(self.rotor_offsets.copy())


    def print_plain(self, rot1, rot2, rot3):
        self.rotor1.setPosition(rot1)
        self.rotor2.setPosition(rot2)
        self.rotor3.setPosition(rot3)

        plain = ""
        self.counter = 0
        for c in self.cipher:
            p_found = encode(
                    c,
                    self.rotorArray, 
                    self.reflector, 
                    self.counter
                )
            plain = plain + p_found

            # next position for next char
            self.counter = rotateRotors(self.counter, self.rotorArray)

        return plain


if __name__ == "__main__":
    app = Bombe()
    print("Exit...")