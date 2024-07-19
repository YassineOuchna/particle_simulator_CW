import pygame

pygame.init()
WIDTH, HEIGHT = int(
    pygame.display.Info().current_w), int(pygame.display.Info().current_h)
FONT_SIZE = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def diffusion_mode():

    screen.fill((15,23,42))
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render('Coming soon! (or never lol)', True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(text, text_rect)

    qx = WIDTH //2
    qy = HEIGHT * 0.67
    h = HEIGHT * 0.05
    w = WIDTH * 0.16
    quitButton = pygame.draw.rect(screen, (10, 0, 255),
                         (qx-w//2, qy-h//2, w, h ))
    text = font.render("Main Menu", True, (255, 255, 255))
    text_rect = text.get_rect(center=(qx, qy))
    screen.blit(text, text_rect)
    DIFF_RUNNING = True
    while DIFF_RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                DIFF_RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:     # Left mouse click
                    mx, my = pygame.mouse.get_pos()
                    if quitButton.collidepoint(mx, my):
                        DIFF_RUNNING = False
        pygame.display.update()
    screen.fill((15,23,42))

if __name__ == "__main__":
    diffusion_mode()