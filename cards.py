import random
import pygame
import math

CARD_IMAGES = pygame.image.load("cards.png")
CARD_BACK = pygame.image.load("card_back.png")

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["H", "D", "S", "C"]

CARD_WIDTH = 30
CARD_HEIGHT = 50

FPS = 30

class Deck:
    def __init__(self, x, y, cards = None):
        self.x = x
        self.y = y
        if cards == None:
            cards = []
            for suit in SUITS:
                for rank in RANKS:
                    cards.append(Card(rank, suit, self))
            self.cards = cards
            self.shuffle()
        else:
            self.cards = cards
    def shuffle(self):
        cards = []
        while len(self.cards) > 0:
            cards.append(self.cards.pop(random.randrange(0, len(self.cards))))
        self.cards = cards
    def draw(self, x = None, y = None, count = 1):
        if count == 1:
            card = self.cards.pop(0)
            card.x = self.x
            card.y = self.y
            return card
        new_deck = Deck(x = x, y = y, cards = self.cards[0:count])
        for card in new_deck.cards:
            card.deck = new_deck
        self.cards = self.cards[count:]
        return new_deck
    def render(self, screen):
        if len(self.cards) == 0:
            pygame.draw.rect(screen, pygame.Color("black"), (self.x, self.y, CARD_WIDTH, CARD_HEIGHT), 1, 3)
        for card in self.cards:
            card.render(screen)
    def add(self, card):
        self.cards.append(card)
        
class Card:
    def __init__(self, rank, suit, deck):
        self.rank = rank
        self.suit = suit
        self.deck = deck
        self.face_up = False
        self.image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        self.dx = 0
        self.dy = 0
        self.x = None
        self.y = None
        self.target = None
        pygame.Surface.blit(self.image, CARD_IMAGES.subsurface(pygame.Rect((RANKS.index(self.rank) * CARD_WIDTH, SUITS.index(self.suit) * CARD_HEIGHT, CARD_WIDTH, CARD_HEIGHT))), (0, 0))
    def __str__(self):
        return self.rank + self.suit
    def is_greater_than(self, other):
        return RANKS.index(self.rank) > RANKS.index(other.rank)
    def equals(self, other):
        return self.rank == other.rank
    def render(self, screen):
        pygame.Surface.blit(screen, self.image if self.face_up else CARD_BACK, (self.deck.x, self.deck.y) if not self.deck == None else (self.x, self.y))
    def move(self, target, time):
        self.deck = None
        self.target = target
        self.dx = (self.target[0] - self.x) / (FPS * time)
        self.dy = (self.target[1] - self.y) / (FPS * time)
    def update(self):
        if not self.target == None:
            self.x += self.dx
            self.y += self.dy
            if (math.hypot(self.x - self.target[0], self.y - self.target[1]) < 1):
                self.target = None
                return True
        else:
            return True
        return False