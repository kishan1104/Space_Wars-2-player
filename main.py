import pygame
import os
pygame.font.init()
pygame.mixer.init()
HEIGHT, WIDTH = 800,1200

YELLOW_HIT = pygame.USEREVENT + 1
PURPLE_HIT = pygame.USEREVENT + 2

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SPACE WARS")
WHITE = (255,255,255)


FPS = 60
VEL = 5


BULLETS_VEL = 30
MAX_BULLETS = 100

HEALTH = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans",100)

SHIP_WIDTH= 40
SHIP_HEIGHT = 30

FIRE_SOUND = pygame.mixer.Sound(os.path.join("assets","fireSound.mp3"))
EXPLOSION = pygame.mixer.Sound(os.path.join("assets","explosion.mp3"))

BACKGROUND_IMG = pygame.image.load(os.path.join("assets","background.png"))
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG,(WIDTH,HEIGHT))

TEXT_BACKGROUND = pygame.Rect(0,0,WIDTH,70)
Y_SHIP = pygame.image.load(os.path.join('assets','yellow.png.png'))
Y_SHIP = pygame.transform.scale(Y_SHIP, (SHIP_WIDTH,SHIP_HEIGHT))
Y_SHIP = pygame.transform.rotate(Y_SHIP, -90)
P_SHIP = pygame.image.load(os.path.join('assets','ship3.png'))
P_SHIP = pygame.transform.scale(P_SHIP, (SHIP_WIDTH,SHIP_HEIGHT))
P_SHIP = pygame.transform.rotate(P_SHIP, 90)


def move_yellow(keypressed,yellow,border):
    if keypressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -=VEL
    if keypressed[pygame.K_d] and yellow.x + VEL < border.x-yellow.width:
        yellow.x +=VEL 
    if keypressed[pygame.K_s] and yellow.y + VEL + SHIP_HEIGHT < HEIGHT:
        yellow.y +=VEL  
    if keypressed[pygame.K_w] and yellow.y - VEL > 70:
        yellow.y -=VEL

def move_purple(keypressed,purple,border):
    if keypressed[pygame.K_LEFT] and purple.x - VEL > border.x + 15:
        purple.x -=VEL
    if keypressed[pygame.K_RIGHT] and purple.x + VEL < WIDTH:
        purple.x +=VEL 
    if keypressed[pygame.K_DOWN] and purple.y + VEL + SHIP_HEIGHT < HEIGHT:
        purple.y +=VEL  
    if keypressed[pygame.K_UP] and purple.y - VEL > 70:
        purple.y -=VEL
    
        
        
def handle_bullets(bullets,yellow,purple):
    
    for yellow_bullet in bullets[0]:
        yellow_bullet.x += BULLETS_VEL
        if purple.colliderect(yellow_bullet):
            pygame.event.post(pygame.event.Event(PURPLE_HIT))
            bullets[0].remove(yellow_bullet)
            
            
    
        elif yellow_bullet.x > WIDTH:
            bullets[0].remove(yellow_bullet)
            

    for purple_bullet in bullets[1]:
        purple_bullet.x -= BULLETS_VEL
        if yellow.colliderect(purple_bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            bullets[1].remove(purple_bullet)
            
        elif purple_bullet.x < 0:
            bullets[1].remove(purple_bullet)
    

def winner_text(winner):
    draw_text = WINNER_FONT.render(winner, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2-draw_text.get_width()//2,HEIGHT/2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)
def draw_display(yellow,purple,border,bullets,yellow_health,purple_health):
    WIN.blit(BACKGROUND_IMG,(0,70))
    pygame.draw.rect(WIN, (0,0,0),TEXT_BACKGROUND)
    pygame.draw.rect(WIN, (0,0,0),border)
    
    yellow_h_text= HEALTH.render("Health:"+str(yellow_health), 1, WHITE)
    purple_h_text= HEALTH.render("Health:"+str(purple_health), 1, WHITE)
    
    WIN.blit(yellow_h_text, (0,10))
    WIN.blit(purple_h_text, (WIDTH-purple_h_text.get_width(),10))
    
    WIN.blit(Y_SHIP, (yellow.x,yellow.y))
    WIN.blit(P_SHIP, (purple.x,purple.y))
    for i in bullets[0]:
        pygame.draw.rect(WIN,(255,0,70),i)
    for i in bullets[1]:
        pygame.draw.rect(WIN,(255,0,70),i)
        
    pygame.display.update()
    
    
def main():
    purple = pygame.Rect(800,500,SHIP_WIDTH,SHIP_HEIGHT)
    yellow = pygame.Rect(10,80,SHIP_WIDTH,SHIP_HEIGHT)
    border = pygame.Rect(WIDTH/2 - 10, 0, 20, HEIGHT)
    clock = pygame.time.Clock()
    bullets = [[],[]]
    yellow_health = 5
    purple_health = 5
    run = True
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and len(bullets[0])<MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width - 2, yellow.y + yellow.width//2 -9, 10, 5)
                    bullets[0].append(bullet)
                    FIRE_SOUND.play()
                    
                if event.key == pygame.K_RCTRL and  len(bullets[1])<MAX_BULLETS:
                    bullet = pygame.Rect(purple.x , purple.y + purple.width//2 -2, 10, 5)
                    bullets[1].append(bullet)
                    FIRE_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -=1 
                EXPLOSION.play()
            if event.type == PURPLE_HIT:
                purple_health -=1
                EXPLOSION.play()
        
        winner = ""
        if yellow_health <=0:
            winner = "Purple is the Winner!"
        
        if purple_health <=0:
            winner = "Yellow is the Winner!"
        
        if winner !="":
            winner_text(winner)
            break
        draw_display(yellow,purple,border,bullets,yellow_health,purple_health)
        keypressed = pygame.key.get_pressed()
        
        move_yellow(keypressed, yellow,border)
        move_purple(keypressed, purple,border)
        handle_bullets(bullets,yellow,purple)
    main()

if __name__ == "__main__":
    main()