import pygame
import string
from pygame.locals import *
pygame.init()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 600

MEOW_LIST = {"pronoun":"mrrp", "noun":"mrrau", "verb":"nya", "adjective":"mrowl", "adverb":"hrru"}
with open("noun_list.txt", "r") as file:
    NOUNS = file.readlines()
with open("verb_list.txt", "r") as file:
    VERBS = file.readlines()
with open("adverb_list.txt", "r") as file:
    ADVERBS = file.readlines()
with open("adjective_list.txt", "r") as file:
    ADJECTIVES = file.readlines()
with open("pronoun_list.txt", "r") as file:
    PRONOUNS = file.readlines()

for i in range(len(NOUNS)):
    NOUNS[i] = NOUNS[i][:-1]
for i in range(len(PRONOUNS)):
    PRONOUNS[i] = PRONOUNS[i][:-1]
for i in range(len(ADVERBS)):
    ADVERBS[i] = ADVERBS[i][:-1]
for i in range(len(VERBS)):
    VERBS[i] = VERBS[i][:-1]
for i in range(len(ADJECTIVES)):
    ADJECTIVES[i] = ADJECTIVES[i][:-1]

class TextBox():
    def __init__(self, x, y, w, h, font, text_color=(0,0,0), bg_color=(255,255,255), border_color=(0,0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = ""
        self.active = False
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == KEYDOWN and self.active:
            if event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == K_RETURN:
                pass
            else:
                self.text += event.unicode
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        words = self.text.split(" ")
        x = self.rect.x + 6
        y = self.rect.y + 6
        max_width = self.rect.width -10

        for word in words:
            text_surface = self.font.render(word + " ", True, self.text_color)
            if x + text_surface.get_width() > self.rect.x + max_width:
                x = self.rect.x + 6
                y += text_surface.get_height()
            screen.blit(text_surface, (x, y))
            x += text_surface.get_width()

class Button():
    def __init__(self, x, y, w, h, text, font, text_color=(0,0,0), bg_color=(200,200,200), hover_color=(170,170,170)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
    
    def draw(self, screen):
        m_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(m_pos) else self.bg_color
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (
            self.rect.centerx - text_surface.get_width()//2,
            self.rect.centery - text_surface.get_height()//2
        ))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class OutputBox():
    def __init__(self, x, y, w, h, font, text_color=(0,0,0), bg_color=(255,255,255), border_color=(0,0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = ""
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
    
    def set_text(self, text):
        self.text = text
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        words = self.text.split(" ")
        x = self.rect.x + 6
        y = self.rect.y + 6
        max_width = self.rect.width -10

        for word in words:
            text_surface = self.font.render(word + " ", True, self.text_color)
            if x + text_surface.get_width() > self.rect.x + max_width:
                x = self.rect.x + 6
                y += text_surface.get_height()
            screen.blit(text_surface, (x, y))
            x += text_surface.get_width()



def convert_to_meow(inp:str):
    inp_list = inp.split()
    converted = []
    for word in inp_list:
        state = "lowercase"
        if word.isupper():
            state = "all_upper"
        elif word[0].isupper():
            state = "capital"
        word = word.lower()
        punctuation_in_word = {}

        for index, char in enumerate(word):
            if char in string.punctuation:
                punctuation_in_word[index] = char
                word = word.replace(char, "", 1)

        if word in PRONOUNS:
            base_word = MEOW_LIST["pronoun"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:2] + ((len(word)-5)//2) * "r" + base_word[2:]
            else:
                new_word = base_word
        elif word in VERBS:
            base_word = MEOW_LIST["verb"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word + ((len(word)-5)//2) * "~a"
            else:
                new_word = base_word
        elif word in ADVERBS:
            base_word = MEOW_LIST["adverb"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:2] + ((len(word)-5)//2) * "r" + base_word[2:]
            else:
                new_word = base_word
        elif word in ADJECTIVES:
            base_word = MEOW_LIST["adjective"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:2] + ((len(word)-5)//2) * "o" + base_word[2:]
            else:
                new_word = base_word
        elif word in NOUNS:
            base_word = MEOW_LIST["noun"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:3] + ((len(word)-5)//2) * "a" + base_word[3:]
            else:
                new_word = base_word
        else:
            base_word = "meow"
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:1] + ((len(word)-5)//2) * "e" + base_word[1:]
            else:
                new_word = base_word
        new_word = list(new_word)
        for key in punctuation_in_word:
            if key > len(new_word):
                new_word.insert(-1, punctuation_in_word[key])
            else:
                new_word.insert(key, punctuation_in_word[key])
        new_word = "".join(new_word)
        if state == "all_upper":
            converted.append(new_word.upper())
        elif state == "capital":
            converted.append(new_word[0].upper() + new_word[1:])
        else:
            converted.append(new_word)

    return " ".join(converted)



screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
font = pygame.font.Font(None, 24)

input_box = TextBox(50, 75, 500, 120, font)
output_box = OutputBox(50, 245, 500, 120, font)
button = Button(50, 203, 200, 35, "Translate <3", font)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_box.handle_event(event)
        if button.clicked(event):
            output_box.set_text(convert_to_meow(input_box.text))
    screen.fill((240, 240, 240))
    input_box.draw(screen)
    button.draw(screen)
    output_box.draw(screen)
    clock.tick(60)
    pygame.display.update()
