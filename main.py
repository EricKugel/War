import pygame
import sys
from cards import *

MARGIN = 30
HEIGHT = 400
WIDTH = 400
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WAR SIMULATOR 🔥🔥🔥 (the card game)")
clock = pygame.time.Clock()

my_deck = Deck(WIDTH / 2 - CARD_WIDTH / 2, HEIGHT - MARGIN - CARD_HEIGHT)
your_deck = my_deck.draw(x = WIDTH / 2 - CARD_WIDTH / 2, y = MARGIN, count = 26)
my_discard = Deck(MARGIN, HEIGHT - MARGIN - CARD_HEIGHT, cards = [])
your_discard = Deck(WIDTH - MARGIN - CARD_WIDTH, MARGIN, cards = [])

decks = [my_deck, your_deck, my_discard, your_discard]
cards = []

MY_SPACE = (WIDTH / 2 - CARD_WIDTH / 2, HEIGHT / 2 + MARGIN / 2)
YOUR_SPACE = (WIDTH / 2 - CARD_WIDTH / 2, HEIGHT / 2 - CARD_HEIGHT - MARGIN / 2)

STATE_DEAL = -1
STATE_MOVING = 0
STATE_PAUSING = 1
STATE_REVEALING = 1.5
STATE_RESOLVING = 2
STATE_ADD_PAUSE = 3
STATE_ADD_TO_MY_DISCARD = 4
state = STATE_DEAL
next_states = []

pause = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    screen.fill(pygame.Color("green"))

    if state == STATE_DEAL:
        my_card = my_deck.draw()
        your_card = your_deck.draw()
        cards = [my_card, your_card]
        my_card.move(MY_SPACE, 1)
        your_card.move(YOUR_SPACE, 1)
        state = STATE_MOVING
        next_states = [STATE_REVEALING, STATE_ADD_PAUSE, STATE_PAUSING, STATE_RESOLVING]
    elif state == STATE_REVEALING:
        for card in cards:
            card.face_up = True
        state = next_states.pop(0)
    elif state == STATE_ADD_PAUSE:
        pause = FPS
        state = next_states.pop(0)
    elif state == STATE_MOVING:
        done = True
        for card in cards:
            if not card.update():
                done = False
        if done:
            state = next_states.pop(0)
    elif state == STATE_PAUSING:
        pause -= 1
        if pause < 0:
            state = next_states.pop(0)
    elif state == STATE_ADD_TO_MY_DISCARD:
        cards.reverse()
        for card in cards:
            cards.remove(card)
            my_discard.add(card)
        state = next_states.pop(0)
    elif state == STATE_RESOLVING:
        for card in cards:
            card.move((my_discard.x, my_discard.y), 1)
        state = STATE_MOVING
        next_states = [STATE_ADD_TO_MY_DISCARD, STATE_DEAL]

    for deck in decks:
        deck.render(screen)
    for card in cards:
        card.render(screen)

    clock.tick(FPS)
    pygame.display.update()