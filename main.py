import pygame
from rotor import Rotor
from reflector import Reflector
import string
import math
import os
from config import INITIAL_ROTOR_OFFSET, ROTAR_1_SEED, ROTAR_2_SEED, ROTAR_3_SEED, REFLECTOR_SEED
slist = list(string.ascii_uppercase)


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


# Initialize Rotors & Reflector
rotor1 = Rotor(ROTAR_1_SEED, 1)
rotor2 = Rotor(ROTAR_2_SEED, 2)
rotor3 = Rotor(ROTAR_3_SEED, 3)
reflector = Reflector(REFLECTOR_SEED)
rotorArray = [rotor1, rotor2, rotor3]
keypressCounter = 0

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Scalable Enigma Machine Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 128, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)  # Highlight color for "front-facing" letter
PURPLE = (128, 0, 128)
GREEN = (0, 128, 0)
ORANGE = (255, 165, 0)

# Font (scaled based on screen size)
pygame.font.init()


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, rotor, index):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.rotor = rotor
        self.index = index

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if is_hovered else self.color

        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border

        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.rect.collidepoint(event.pos):
                return True
        return False


def get_scaled_font(size):
    return pygame.font.Font(None, size)


def get_key_dimensions():
    return WIDTH // 40, HEIGHT // 30  # key width, key height


def draw_arc(surface, color, rect, thickness):
    pygame.draw.arc(surface, color, rect,
                    math.radians(90), math.radians(270), thickness)


def get_key_positions():
    # Position keyboard keys along the bottom of the screen
    key_width, key_height = get_key_dimensions()
    start_x = WIDTH // 20
    margin_x = WIDTH // 100
    y_pos = HEIGHT - key_height - (HEIGHT // 30)
    return [(start_x + i * (key_width + margin_x), y_pos) for i in range(26)]


def get_lampboard_positions():
    return (31*WIDTH // 32, HEIGHT // 6 - 20)


def find_lampboard_position(i):
    y = lamp_positions[1] + i * (font.get_height() + 4)
    x = lamp_positions[0]
    return (x, y)


def get_rotor_positions():
    # Position rotors in the middle of the screen
    return [
        (3 * WIDTH // 4 + WIDTH//5 - WIDTH//20, HEIGHT // 6 - 20),
        (WIDTH // 2 + WIDTH//5 - WIDTH//20, HEIGHT // 6 - 20),
        (WIDTH // 4 + WIDTH//5 - WIDTH//20, HEIGHT // 6 - 20)
    ]


def find_rotor_position(i, rotor_positions, rotor_output_positions):
    locations = []
    for r in range(3):
        input_x = rotor_positions[r][0]
        input_y = rotor_positions[r][1] + i * (font.get_height() + 4)
        output_x = rotor_output_positions[r][0]
        output_y = rotor_output_positions[r][1] + \
            rotorArray[r].map[i] * (font.get_height() + 4)
        i = rotorArray[r].map[i]
        locations.append(((input_x, input_y), (output_x, output_y)))
    return locations, i


def find_rotor_position_reversed(i, rotor_positions, rotor_output_positions):
    locations = []
    for r in range(3-1, -1, -1):
        input_x = rotor_output_positions[r][0]
        input_y = rotor_output_positions[r][1] + i * (font.get_height() + 4)
        output_x = rotor_positions[r][0]
        output_y = rotor_positions[r][1] + \
            rotorArray[r].map.index(i) * (font.get_height() + 4)
        i = rotorArray[r].map.index(i)
        locations.append(((input_x, input_y), (output_x, output_y)))
    return locations, i


def get_rotor_output_positions():
    return [(3 * WIDTH // 4 - WIDTH//20, HEIGHT // 6 - 20), (WIDTH // 2 - WIDTH//20, HEIGHT // 6 - 20), (WIDTH // 4 - WIDTH//20, HEIGHT // 6 - 20)]


def get_rotor_radius():
    return min(WIDTH, HEIGHT) // 10


def get_reflector_positions():
    return (WIDTH // 5 - WIDTH//20, HEIGHT // 6 - 20)


def find_reflector_position(i, reflector):
    y = reflector_positions[1] + i * (font.get_height() + 4)
    x = reflector_positions[0]
    input = (x, y)
    i = reflector.map[i]
    y = reflector_positions[1] + i * (font.get_height() + 4)
    x = reflector_positions[0]
    output = (x, y)
    return (input, output), i

# collect the coordinates of the wiring connections that the signal travelled through


def make_path(i, j):
    positions = []
    lampboard = find_lampboard_position(i)
    positions.append(lampboard)
    rotors, i = find_rotor_position(i, rotor_positions, rotor_output_positions)
    for a in range(3):
        for b in range(2):
            positions.append(rotors[a][b])
    reflector_pos, i = find_reflector_position(i, reflector)
    positions.append(reflector_pos[0])
    positions.append(reflector_pos[1])
    rotors_reversed, i = find_rotor_position_reversed(
        i, rotor_positions, rotor_output_positions)
    for a in range(3):
        for b in range(2):
            positions.append(rotors_reversed[a][b])
    lampboard_end = find_lampboard_position(j)
    positions.append(lampboard_end)
    return positions

# draw a path along make_path() above


def draw_path_lines(positions, color, thickness):
    for i in range(len(positions)):
        if i + 1 >= len(positions):
            break

        curr_pos = positions[i]
        next_pos = positions[i+1]
        if i == 7:
            rect = ((curr_pos[0]+next_pos[0])//2-abs(curr_pos[1]-next_pos[1])//2,
                    min(curr_pos[1], next_pos[1])-HEIGHT//400,
                    abs(curr_pos[1]-next_pos[1]),
                    abs(curr_pos[1]-next_pos[1])+HEIGHT//200)
            draw_arc(screen, RED, rect, 5)
            continue
        pygame.draw.line(screen, color,
                         curr_pos, next_pos, thickness)


letters = list(string.ascii_uppercase)

# Initial rotor configurations and offsets``
rotors = [list(letters), list(letters), list(letters)]
rotor_offsets = INITIAL_ROTOR_OFFSET
rotor1.setPosition(rotor_offsets[0])
rotor2.setPosition(rotor_offsets[1])
rotor3.setPosition(rotor_offsets[2])
rotor1.rotorToString()
rotor2.rotorToString()
rotor3.rotorToString()

# initialise rotor buttons
rotor_positions = get_rotor_positions()
rotor_output_positions = get_rotor_output_positions()
button_positions = []
button_bot_positions = []
for i in range(len(rotor_positions)):
    x = (rotor_positions[i][0] + rotor_output_positions[i][0])//2 - 30
    y = rotor_positions[i][1] - 40
    button_positions.append((x, y))
    button_bot_positions.append((x, y+4*HEIGHT//5))
rotor1away = Button(
    button_positions[0][0], button_positions[0][1], 80, 20, "away", DARK_GRAY, RED, WHITE, rotor1, 0)
rotor1towards = Button(
    button_bot_positions[0][0], button_bot_positions[0][1], 80, 20, "towards", DARK_GRAY, RED, WHITE, rotor1, 0)
rotor2away = Button(
    button_positions[1][0], button_positions[1][1], 80, 20, "away", DARK_GRAY, RED, WHITE, rotor2, 1)
rotor2towards = Button(
    button_bot_positions[1][0], button_bot_positions[1][1], 80, 20, "towards", DARK_GRAY, RED, WHITE, rotor2, 1)
rotor3away = Button(
    button_positions[2][0], button_positions[2][1], 80, 20, "away", DARK_GRAY, RED, WHITE, rotor3, 2)
rotor3towards = Button(
    button_bot_positions[2][0], button_bot_positions[2][1], 80, 20, "towards", DARK_GRAY, RED, WHITE, rotor3, 2)

buttons = [rotor1away, rotor1towards, rotor2away,
           rotor2towards, rotor3away, rotor3towards]

# Variable to track the last key pressed
pressed_key = None
cipher_key = None
plaintext = ""
ciphertext = ""
key_pressed = False
# Main loop
running = True
while running:
    # Refresh dimensions and positions on each frame for scalability
    key_width, key_height = get_key_dimensions()
    key_positions = get_key_positions()
    lamp_positions = get_lampboard_positions()
    rotor_positions = get_rotor_positions()
    rotor_output_positions = get_rotor_output_positions()
    rotor_radius = get_rotor_radius()
    reflector_positions = get_reflector_positions()
    font = get_scaled_font(min(WIDTH, HEIGHT) // 30)

    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(f"Plaintext: {plaintext}")
            print(f"Ciphertext: {ciphertext}")
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.unicode.upper() in letters:
                # Track the pressed key to light it up
                pressed_key = event.unicode.upper()
                cipher_key = encode(
                    pressed_key, rotorArray, reflector, keypressCounter)
                plaintext += pressed_key
                ciphertext += cipher_key
                # draw used lines heavier
                key_pressed = True
                pressed_index = list(string.ascii_uppercase).index(pressed_key)
                cipher_index = list(string.ascii_uppercase).index(cipher_key)
                positions = make_path(pressed_index, cipher_index)
                draw_path_lines(positions, RED, 4)
        elif event.type == pygame.KEYUP:
            # Update rotor positions (advance the first rotor, cascading if necessary)
            key_pressed = False
            rotor_offsets[0] = (rotor_offsets[0] + 1) % 26
            if rotor_offsets[0] == 0:
                rotor_offsets[1] = (rotor_offsets[1] + 1) % 26
                if rotor_offsets[1] == 0:
                    rotor_offsets[2] = (rotor_offsets[2] + 1) % 26
            keypressCounter = rotateRotors(keypressCounter, rotorArray)
        for button in buttons:
            if button.is_clicked(event):
                if button.text == "away":
                    button.rotor.rotateAway()
                    rotor_offsets[button.index] += 1
                elif button.text == "towards":
                    button.rotor.rotateTowards()
                    rotor_offsets[button.index] -= 1

                # print current rotor setting
                print("Current rotor setting: ", rotor_offsets)

    if key_pressed:
        if pressed_key:  # Check if there was a key pressed
            pressed_index = list(string.ascii_uppercase).index(pressed_key)
            positions = make_path(pressed_index, cipher_index)
            # Continuously draw while key is pressed
            draw_path_lines(positions, RED, 4)

    # >>>>> Visuals >>>>>>>

    for button in buttons:
        button.draw(screen)

    # Draw lampboard
    # The return letter on the right
    for i in range(26):
        letter = list(string.ascii_uppercase)[i]
        y_offset = i * (font.get_height() + 4)

        # Change color based on the light_up variable
        color = BLACK
        if letter == cipher_key:
            color = ORANGE
        elif letter == pressed_key:
            color = BLUE
        label = font.render(letter, True, color)
        label_rect = label.get_rect(
            center=(lamp_positions[0], lamp_positions[1] + y_offset))
        if letter == cipher_key or letter == pressed_key:
            rect = pygame.Rect(lamp_positions[0]-font.get_height()//2, lamp_positions[1] +
                               y_offset-font.get_height()//2, font.get_height(), font.get_height())
            pygame.draw.rect(screen, BLACK, rect)

        screen.blit(label, label_rect)

    # Draw rotors (front-facing)
    # The right side of the rotor
    for r, pos in enumerate(rotor_positions):
        # Display only the top few letters (simulate front-facing)
        for i in range(26):  # Show letters slightly above and below
            letter_index = (rotor_offsets[r] + i) % 26
            letter = rotors[r][letter_index]
            y_offset = i * (font.get_height() + 4)

            color = RED if i == 0 else BLACK
            label = font.render(letter, True, color)
            label_rect = label.get_rect(center=(pos[0], pos[1] + y_offset))
            screen.blit(label, label_rect)

    # Draw rotor outputs (front-facing)
    # The left side of the rotor
    for r, pos in enumerate(rotor_output_positions):
        for i in range(26):
            letter_index = (rotor_offsets[r] + i) % 26
            letter = rotors[r][letter_index]
            y_offset = i * (font.get_height() + 4)

            color = RED if i == 0 else BLACK
            label = font.render(letter, True, color)
            label_rect = label.get_rect(center=(pos[0], pos[1] + y_offset))
            screen.blit(label, label_rect)

    # Draw lines between input and output of each rotor
    for r in range(3):  # Three rotors
        for i in range(26):  # Connect each letter position
            input_x = rotor_positions[r][0]
            input_y = rotor_positions[r][1] + i * (font.get_height() + 4)
            output_x = rotor_output_positions[r][0]
            output_y = rotor_output_positions[r][1] + \
                rotorArray[r].map[i] * (font.get_height() + 4)

            pygame.draw.line(screen, GRAY,
                             (input_x, input_y), (output_x, output_y), 2)

    # Draw self lines for reflectors
    drawn = []
    for i in range(26):
        letter = list(string.ascii_uppercase)[i]
        y_offset = i * (font.get_height() + 4)

        color = BLACK
        label = font.render(letter, True, color)
        label_rect = label.get_rect(
            center=(reflector_positions[0], reflector_positions[1] + y_offset))
        screen.blit(label, label_rect)

        if i not in drawn:
            # starting rect = label_rect
            # ending rect = target_rect
            target_index = reflector.map[i]
            y_offset = target_index * (font.get_height() + 4)
            target_rect = label.get_rect(
                center=(reflector_positions[0], reflector_positions[1] + y_offset))

            # Rect(left, top, width, height) -> Rect
            # draw_arc(surface, color, rect, thickness)
            radius = abs(label_rect.center[1]-target_rect.center[1])//2

            x = label_rect.centerx - radius
            y = label_rect.centery
            temp_rect = (x, y, radius*2, radius*2)
            drawn.append(i)
            drawn.append(reflector.map[i])

            draw_arc(screen, GRAY, temp_rect, 2)
    pygame.display.flip()

pygame.quit()
