### How to use
1. Run main.py

### How it works
#### To decrypt
1. Need to know reflector / plug board setting
2. Need to know the rotor scramble + the initial rotation

#### What you will see
1. The set of letters with thin lines connected are the rotors
2. The alpha letters pressed will light up at the right (Blue)
3. The return letter will light up on the right (Orange)
4. The path taken can be seen by the thick red line when you hold down the letter you want to encrypt / decrypt

#### Lampboard
- On the right
- The corresponding letter will light up for each keypress
- Blue for input
- Orange for output

#### Rotor
- Mapping of rotors randomized once at start (able to set seed for repeatable results)
- Outputs a corresponding index for a input index
- Mapping shifts after each input press, till it rotates 1 full turn, going back to original mapping
- Per one full turn of any rotor, the next rotor to the left rotates 1 index

#### Reflector
- The leftmost connector to reflect the signal back, mapping relationship is symmetrical between indexes

#### Plugboard
- This program is the basest form of the Enigma Machine and has yet to implement the plugboard
