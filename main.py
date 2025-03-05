import sys
import pygame, time, random
pygame.font.init()
pygame.mixer.init()
pygame.init()

WIDTH, HEIGHT = 850, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighters")

BG = pygame.transform.scale(pygame.image.load("space.png"), (WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

FONT = pygame.font.SysFont("comicsans", 40)

BULLET_HIT_SOUND = pygame.mixer.Sound("Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Gun+Silencer.mp3")

SPACESHIP_WIDTH = 55
SPACESHIP_VEL = 5

YELLOW_SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load('spaceship_yellow.png'), (SPACESHIP_WIDTH, SPACESHIP_WIDTH))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, -90)

RED_SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load('spaceship_red.png'), (SPACESHIP_WIDTH, SPACESHIP_WIDTH))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP_IMAGE, 90)

BULLET_VEL = 5
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

def draw(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(BG, (0, 0))

    pygame.draw.rect(WIN, "#000000", BORDER)

    red_health_text = FONT.render(f"Health: {red_health}", 1, pygame.color.Color(255, 255, 255))
    yellow_health_text = FONT.render(f"Health: {yellow_health}", 1, pygame.color.Color(255, 255, 255))

    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, "#ffff00", bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, "#ff0000", bullet)

    pygame.display.update()

def yellow_handle_movement(keys, yellow):
    if keys[pygame.K_a] and yellow.x - SPACESHIP_VEL >= 0:
            yellow.x -= SPACESHIP_VEL
    if keys[pygame.K_d] and yellow.x + SPACESHIP_VEL + yellow.width <= BORDER.x:
        yellow.x += SPACESHIP_VEL
    if keys[pygame.K_w] and yellow.y - SPACESHIP_VEL >= 0:
        yellow.y -= SPACESHIP_VEL
    if keys[pygame.K_s] and yellow.y + SPACESHIP_VEL + yellow.height <= HEIGHT:
        yellow.y += SPACESHIP_VEL

def red_hanle_movement(keys, red):
    if keys[pygame.K_LEFT] and red.x - SPACESHIP_VEL >= BORDER.x + BORDER.width:
        red.x -= SPACESHIP_VEL
    if keys[pygame.K_RIGHT] and red.x + SPACESHIP_VEL + red.width <= WIDTH:
        red.x += SPACESHIP_VEL
    if keys[pygame.K_UP] and red.y - SPACESHIP_VEL >= 0:
        red.y -= SPACESHIP_VEL
    if keys[pygame.K_DOWN] and red.y + SPACESHIP_VEL + red.height <= HEIGHT:
        red.y += SPACESHIP_VEL

def bullet_handle(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x + bullet.width >= WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x <= 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    winner_text = FONT.render(text, 1, pygame.color.Color(255, 255, 255))
    WIN.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))

    pygame.display.update()
    pygame.time.delay(2000)

def end_screen():
    play_again_text = FONT.render('Play Again', 1, pygame.color.Color(255, 255, 255))
    quit_text = FONT.render('Quit', 1, pygame.color.Color(255, 255, 255))

    button_x = 300
    button_y = 150

    WIN.blit(play_again_text, (button_x, button_y))
    WIN.blit(quit_text, (button_x, button_y * 3))
    pygame.display.update()

    click = False
    while (click == False):
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (mouse[0] >= button_x and mouse[0] <= button_x + play_again_text.get_width() and mouse[1] <= button_y + play_again_text.get_height()):
                    main()
                    click = True
                
                if (mouse[0] >= button_x and mouse[0] <= button_x + quit_text.get_width() and mouse[1] >= button_y * 3 and mouse[1] <= button_y * 3 + quit_text.get_height()):
                    pygame.quit()
                    sys.exit()

def main():
    run = True

    clock = pygame.time.Clock()

    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_WIDTH)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_WIDTH)

    red_bullets = []
    yellow_bullets = []

    red_health = 3
    yellow_health = 3

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
                #pygame.quit() #don't necessarily need. Will not exit program; just uninitialize all modules

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height / 2 - 2, 10, 5) # - 2 because that's half the bullet size (5 / 2)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height / 2 - 2, 10, 5) # - 2 because that's half the bullet size (5 / 2)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
            
        keys = pygame.key.get_pressed()
        yellow_handle_movement(keys, yellow)
        red_hanle_movement(keys, red)

        bullet_handle(yellow_bullets, red_bullets, yellow, red)

        draw(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    end_screen()

if __name__ == "__main__":
    main()