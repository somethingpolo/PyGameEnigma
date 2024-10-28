### How to use
1. Run main.py

### How it works
#### To decrypt
1. Need to know reflector / plug board setting
2. Need to know the rotor scramble + the initial rotation

#### What you will see
1. The set of letters with thin lines connected are the rotors
2. The alpha letters pressed will light up at the bottom (Blue)
3. The return letter will light up on the right (Blue)
4. The path taken can be seen by the thick red line when you hold down the letter you want

#### Lampboard
- On the right
- The corresponding letter will light up for each keypress

#### Keyboard
- On the bottom
- Lights up the corresponding letter pressed

#### Rotor
- Mapping of rotates randomized once at start
- Outputs a corresponding index for a input index
- Mapping shifts after each input press, till it rotates 1 full turn, going back to original mapping
- Per a full turn, the rotor to the left shifts rotates once

#### Plug Board / Reflector
- The most left connector to reflect the signal back
- It is the plug board
