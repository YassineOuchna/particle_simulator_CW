import pygame

# GLOBAL PARAMETERS
WIDTH = 750
HEIGHT = 750
RUNNING = True
FONT_SIZE = 40
XPLACEMENT = int(0.5*WIDTH)
YPLACEMENT = int(0.025*HEIGHT)
BH = int(HEIGHT*0.05)
BW = int(WIDTH*0.15)
# Initializing display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Particle Simulator')

# Setting up first screen


def main_menu():
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render('Particle Simulator', True, (255, 255, 255))
    text_rect = text.get_rect(center=(XPLACEMENT, YPLACEMENT))
    screen.blit(text, text_rect)


def wave_button(x, y, w, h):
    pygame.draw.rect(screen, (10, 0, 255),
                     (x-w//2, y-h//2, w, h))
    font = pygame.font.Font(None, 36)
    text = font.render("Wave mode", True, (255, 255, 255))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def diffusion_button(x, y, w, h):
    pygame.draw.rect(screen, (10, 0, 255),
                     (x-w//2, y-h//2, w, h))
    font = pygame.font.Font(None, 36)
    text = font.render("Diffusion", True, (255, 255, 255))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


main_menu()
wave_button(XPLACEMENT, int(HEIGHT*0.35), 150, 50)
diffusion_button(XPLACEMENT, int(HEIGHT*0.35)+60, 150, 50)
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    pygame.display.flip()

pygame.quit()
