import pygame

# GLOBAL PARAMETERS
WIDTH = 750
HEIGHT = 750
RUNNING = True
FONT_SIZE = 40
XPLACEMENT = int(0.5*WIDTH)
YPLACEMENT = int(0.05*HEIGHT)
BH = int(HEIGHT*0.05)
BW = int(WIDTH*0.15)
# Initializing display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Particle Simulator')

# Setting up first screen


def wave_button(x, y, w, h):
    l = pygame.draw.rect(screen, (10, 0, 255),
                         (x-w//2, y-h//2, w, h))
    font = pygame.font.Font(None, 36)
    text = font.render("Wave Propagation", True, (255, 255, 255))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    return l


def diffusion_button(x, y, w, h):
    l = pygame.draw.rect(screen, (10, 0, 255),
                         (x-w//2, y-h//2, w, h))
    font = pygame.font.Font(None, 36)
    text = font.render("Diffusion", True, (255, 255, 255))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    return l


def quit_button(x, y, w, h):
    l = pygame.draw.rect(screen, (10, 0, 255),
                         (x-w//2, y-h//2, w, h))
    font = pygame.font.Font(None, 36)
    text = font.render("Quit", True, (255, 255, 255))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)
    return l


def main_menu():
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render('Particle Simulator', True, (255, 255, 255))
    text_rect = text.get_rect(center=(XPLACEMENT, YPLACEMENT))
    screen.blit(text, text_rect)
    a = wave_button(XPLACEMENT, int(HEIGHT*0.35), 250, 35)
    b = diffusion_button(XPLACEMENT, int(HEIGHT*0.35)+70, 250, 35)
    c = quit_button(XPLACEMENT, int(HEIGHT*0.35)+140, 250, 35)
    return a, b, c


WaveButton, DiffusionButton, QuitButton = main_menu()
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        # Button management
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:     # Left mouse click
                mx, my = pygame.mouse.get_pos()
                if WaveButton.collidepoint(mx, my):
                    pygame.display.set_mode((500, 500))
                if DiffusionButton.collidepoint(mx, my):
                    print('Diffuse')
                if QuitButton.collidepoint(mx, my):
                    RUNNING = False

    pygame.display.update()

pygame.quit()
