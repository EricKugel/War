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
MY_PRIZE_SPACES = [(WIDTH / 2 - CARD_WIDTH / 2 + CARD_WIDTH * i, HEIGHT / 2 + MARGIN) for i in range(-1, 2)]
YOUR_PRIZE_SPACES = [(WIDTH / 2 - CARD_WIDTH / 2 + CARD_WIDTH * i, HEIGHT / 2 - CARD_HEIGHT - MARGIN) for i in range(-1, 2)]

FONT = pygame.font.SysFont('sans-serif', 26)
PADDING = 10

STATE_DEAL = -1
STATE_MOVING = 0
STATE_PAUSING = 1
STATE_REVEALING = 1.5
STATE_RESOLVING = 2
STATE_ADD_PAUSE = 3
STATE_ADD_TO_MY_DISCARD = 4
STATE_WAR = 5
STATE_ADD_TO_YOUR_DISCARD = 6
STATE_ADD_TO_MY_DECK = 7
STATE_ADD_TO_YOUR_DECK = 8
STATE_YOU_WIN = 9
STATE_I_WIN = 10
state = STATE_DEAL
next_states = []

SPEED = .5
pause = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    screen.fill(pygame.Color("green"))

    if state == STATE_DEAL:
        if len(my_deck.cards) == 0:
            if len(my_discard.cards) == 0:
                state = STATE_YOU_WIN
            else:
                for card in my_discard.cards:
                    card.faceup = False
                    cards.append(card)
                    card.move((my_deck.x, my_deck.y), SPEED)
                my_discard.cards = []
                state = STATE_MOVING
                next_states = [STATE_ADD_TO_MY_DECK, STATE_DEAL]
        elif len(your_deck.cards) == 0:
            for card in your_discard.cards:
                card.faceup = False
                cards.append(card)
                card.move((your_deck.x, your_deck.y), SPEED)
                your_discard.cards = []
            state = STATE_MOVING
            next_states = [STATE_ADD_TO_YOUR_DECK, STATE_DEAL]
        else:
            my_card = my_deck.draw()
            your_card = your_deck.draw()
            cards.append(my_card)
            cards.append(your_card)
            my_card.move(MY_SPACE, SPEED)
            your_card.move(YOUR_SPACE, SPEED)
            state = STATE_MOVING
            next_states = [STATE_REVEALING, STATE_ADD_PAUSE, STATE_PAUSING, STATE_RESOLVING]
    elif state == STATE_ADD_TO_MY_DECK:
        cards.reverse()
        for card in cards:
            my_deck.add(card)
            card.face_up = False
        cards = []
        my_deck.shuffle()
        state = next_states.pop(0)
    elif state == STATE_ADD_TO_YOUR_DECK:
        cards.reverse()
        for card in cards:
            card.face_up = False
            your_deck.add(card)
        cards = []
        your_deck.shuffle()
        state = STATE_DEAL
    elif state == STATE_I_WIN:
        print("Player one won")
        pygame.quit()
        sys.exit(0)
    elif state == STATE_YOU_WIN:
        print("Player two won")
        pygame.quit()
        sys.exit(0)    
    elif state == STATE_REVEALING:
        for card in cards:
            card.face_up = True
        state = next_states.pop(0)
    elif state == STATE_ADD_PAUSE:
        pause = FPS * SPEED
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
            my_discard.add(card)
        cards = []
        state = next_states.pop(0)
    elif state == STATE_ADD_TO_YOUR_DISCARD:
        cards.reverse()
        for card in cards:
            your_discard.add(card)
        cards = []
        state = next_states.pop(0)
    elif state == STATE_RESOLVING:
        if my_card.equals(your_card):
            state = STATE_WAR
        else:
            i_won = my_card.is_greater_than(your_card)
            for card in cards:
                card.move((my_discard.x, my_discard.y) if i_won else (your_discard.x, your_discard.y), SPEED)
            state = STATE_MOVING
            next_states = [STATE_ADD_TO_MY_DISCARD if i_won else STATE_ADD_TO_YOUR_DISCARD, STATE_DEAL]
    elif state == STATE_WAR:
        my_prize = []
        your_prize = []
        if len(my_deck.cards) < 3:
            if len(my_discard.cards) == 0:
                i = 0
                while len(my_deck.cards) > 0:
                    my_prize_card = my_deck.draw()
                    your_prize_card = your_deck.draw()
                    my_prize.append(my_prize_card)
                    your_prize.append(your_prize_card)
                    cards.append(my_prize_card)
                    cards.append(your_prize_card)
                    my_prize_card.move(MY_PRIZE_SPACES[i], SPEED)
                    your_prize_card.move(YOUR_PRIZE_SPACES[i], SPEED)
                    state = STATE_MOVING
                    next_states = [STATE_ADD_PAUSE, STATE_PAUSING, STATE_YOU_WIN]
                    i += 1
            else:
                for card in my_discard.cards:
                    card.faceup = False
                    cards.append(card)
                    card.move((my_deck.x, my_deck.y), SPEED)
                    my_discard.cards = []
                state = STATE_MOVING
                next_states = [STATE_ADD_TO_MY_DECK, STATE_WAR]
        elif len(your_deck.cards) < 3:
            if len(your_discard.cards) == 0:
                i = 0
                while len(your_deck.cards) > 0:
                    my_prize_card = my_deck.draw()
                    your_prize_card = your_deck.draw()
                    my_prize.append(my_prize_card)
                    your_prize.append(your_prize_card)
                    cards.append(my_prize_card)
                    cards.append(your_prize_card)
                    my_prize_card.move(MY_PRIZE_SPACES[i], SPEED)
                    your_prize_card.move(YOUR_PRIZE_SPACES[i], SPEED)
                    state = STATE_MOVING
                    next_states = [STATE_ADD_PAUSE, STATE_PAUSING, STATE_I_WIN]
                    i += 1
            else:
                for card in your_discard.cards:
                    card.faceup = False
                    cards.append(card)
                    card.move((your_deck.x, your_deck.y), SPEED)
                your_discard.cards = []
                state = STATE_MOVING
                next_states = [STATE_ADD_TO_YOUR_DECK, STATE_WAR]
        else:
            for i in range(3):
                my_prize_card = my_deck.draw()
                your_prize_card = your_deck.draw()
                my_prize.append(my_prize_card)
                your_prize.append(your_prize_card)
                cards.append(my_prize_card)
                cards.append(your_prize_card)
                my_prize_card.move(MY_PRIZE_SPACES[i], SPEED)
                your_prize_card.move(YOUR_PRIZE_SPACES[i], SPEED)
            state = STATE_MOVING
            next_states = [STATE_ADD_PAUSE, STATE_PAUSING, STATE_ADD_PAUSE, STATE_PAUSING, STATE_DEAL]


    for deck in decks:
        deck.render(screen)
    for card in cards:
        card.render(screen)

    my_deck_text = FONT.render(str(len(my_deck.cards)), True, pygame.Color("black"))
    your_deck_text = FONT.render(str(len(your_deck.cards)), True, pygame.Color("black"))
    my_discard_text = FONT.render(str(len(my_discard.cards)), True, pygame.Color("black"))
    your_discard_text = FONT.render(str(len(your_discard.cards)), True, pygame.Color("black"))
    screen.blit(my_deck_text, (my_deck.x + CARD_WIDTH + PADDING, my_deck.y + 16))    
    screen.blit(your_deck_text, (your_deck.x - your_deck_text.get_rect().width - PADDING, your_deck.y + 16))    
    screen.blit(my_discard_text, (my_discard.x + CARD_WIDTH + PADDING, my_discard.y + 16))    
    screen.blit(your_discard_text, (your_discard.x - your_discard_text.get_rect().width - PADDING, your_discard.y + 16))

    clock.tick(FPS)
    pygame.display.update()