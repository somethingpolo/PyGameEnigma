### How to use
1. Run main.py

### How it works
#### To decrypt
1. Need to know reflector / plug board setting (No plug board for this version)
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
- Does not allow the signal to be mapped to itself
- Had fixed wirings for specific versions, cannot be changed

#### Plugboard
- This program is the basest form of the Enigma Machine and has yet to implement the plugboard
- The plugboard is the initial signal switch, where for example A -> G, then the signal goes to the rotors

### How was it broken
- Weakness 1: A letter cannot be encrypted to itself, so a known text position can possibly be found in the cipher text
- Weakness 2: For a rotor position A -> C means C -> A, this allows forming of loops

#### Steps
1. Have a known plaintext (partial or full)
2. Find a crib, the place where the known plaintext could be
3. Loop through different rotor positions and see if the plaintext can produce the ciphertext
4. If a match is found, flag as a potential solution and get someone to check