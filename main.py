import pygame
import string
from pygame.locals import *
try:
    import js
    WEB = True
except ImportError:
    WEB = False
    import pyperclip
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

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
    def __init__(self, x, y, w, h, text, font, text_color=(0,0,0), bg_color=(200,200,200), hover_color=(255, 212, 209)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
    
    def draw(self, screen):
        m_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(m_pos) else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.text_color, self.rect, 2)
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

class Cat(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = [pygame.image.load("cat_still.png"),
                    pygame.image.load("cat_frame_1.png"),
                    pygame.image.load("cat_frame_2.png"),
                    pygame.image.load("cat_frame_1.png")]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.speaking = False
        self.current_frame = 0
        self.frame_time = 120
        self.last_update = 0
        self.cycle = 0

    def start_speak(self, word_num):
        self.speaking = True
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.word_num = word_num
    
    def update(self):
        if self.speaking:
            now = pygame.time.get_ticks()
            
            if now - self.last_update > self.frame_time:
                self.last_update = now
                self.current_frame += 1

                if self.current_frame >= len(self.frames):
                    if self.cycle >= self.word_num:
                        self.speaking = False
                        self.current_frame = 0
                        self.cycle = 0
                    else:
                        self.start_speak(self.word_num)
                        self.cycle += 1

                self.image = self.frames[self.current_frame]

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
        elif word in VERBS or word[:-2] in VERBS or word[:-1] in VERBS: #covers case of ing and ed endings
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
        elif word in NOUNS or word[:-1] in NOUNS: #covers case of plurals
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
            if key > len(new_word) and punctuation_in_word[key] == "\'":
                new_word.insert(-1, punctuation_in_word[key])
            elif key > len(word) - 1:
                new_word.append(punctuation_in_word[key])
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

input_box = TextBox(250, 125, 500, 200, font)
output_box = OutputBox(250, 375, 500, 200, font)
translate_button = Button(250, 333, 160, 35, "Translate <3", font, (0,0,0), (252, 242, 194))
clear_button = Button(417, 333, 160, 35, "Clear!", font, (0,0,0), (252, 242, 194))
copy_button = Button(583, 333, 160, 35, "Copy Meows :D", font, (0,0,0), (252, 242, 194))
cat = Cat((125,455))
all_sprites = pygame.sprite.Group(cat)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_box.handle_event(event)
        if translate_button.clicked(event):
            meow_text = convert_to_meow(input_box.text)
            output_box.set_text(meow_text)
            cat.start_speak(len(meow_text.split()))
        if clear_button.clicked(event):
            input_box.text = ""
            output_box.text = ""
        if copy_button.clicked(event):
            if WEB:
                js.navigator.clipboard.writeText(output_box.text)
            else:
                pyperclip.copy(output_box.text)
    screen.fill((252, 242, 194))
    
    logo_image = pygame.image.load("logo.png").convert_alpha()
    screen.blit(logo_image, logo_image.get_rect(midtop=(400,0)))
    all_sprites.update()
    input_box.draw(screen)
    translate_button.draw(screen)
    clear_button.draw(screen)
    copy_button.draw(screen)
    output_box.draw(screen)
    all_sprites.draw(screen)
    clock.tick(60)
    pygame.display.update()
