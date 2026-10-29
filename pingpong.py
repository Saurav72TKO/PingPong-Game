import pygame, sys
import random
from pygame import mixer #to play music and sound effect

def reset_ball (): #reset the ball after every point
    global ball_vel_x, ball_vel_y
    ball.x = WIDTH/2
    ball.y = random.randint(200,600)
    ball_vel_x *= random.choice([-1,1])
    ball_vel_y *= random.choice([-1,1])
    

def point_won (winner): #points music 
    global cpu_points , player_points
    
    if winner == cpu:
        lost_sound.play()  # plays once
        cpu_points += 1
        
    if winner == player:
        won_sound.play()  # plays once
        player_points += 1
        
    reset_ball()
    

def animate_ball(): #ball movement
    
    global ball_vel_x, ball_vel_y
    
    ball.x += ball_vel_x
    ball.y += ball_vel_y
        
        
    if ball.bottom >= HEIGHT or ball.top <= 0:  #edges / wall 
        ball_vel_y *= -1
        
    if ball.right >= WIDTH:
        point_won(cpu)
        
              
    if ball.left <= 0:
        point_won(player)
        
        
    if ball.colliderect(player) or ball.colliderect(cpu):
        ball_vel_x *= -1
        
def animate_player():
    player.y += player_vel
    
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT
        
def animate_cpu ():
    global  cpu_speed
    cpu.y += cpu_speed
    
    if ball.centery + random.randint(-85,85)<= cpu.centery: #adding error to the cpu position to make it imperfect
        cpu_speed = -6
    if ball.centery + random.randint(-85,85) >= cpu.centery:
        cpu_speed = 6
        
    if cpu.bottom >= HEIGHT:
        cpu.bottom = HEIGHT
    if cpu.top <= 0:
        cpu.top = 0
        


#Game screen and initialization
pygame.init()
mixer.init()

WIDTH = 1280
HEIGHT = 800
FRAMERATE = 60

screen = pygame.display.set_mode ((WIDTH,HEIGHT)) #screen (display surface) and caption 
pygame.display.set_caption("Pongg Game!!!")


# game music
mixer.music.load("Deck the Halls Jazz Loop.ogg")
mixer.music.set_volume(0.25)
mixer.music.play(-1)  # start playing

# game sound effect
won_sound = mixer.Sound("won.mp3")  
won_sound.set_volume(0.7)
lost_sound = mixer.Sound("lost.mp3")  
lost_sound.set_volume(0.7)





clock = pygame.time.Clock() #for fps

ball = pygame.Rect(0,0,35,35)
ball.center = (WIDTH/2,HEIGHT/2)

cpu = pygame.Rect(0,0,30,155)
cpu.centery = HEIGHT/2

player = pygame.Rect(0,0,30,155)
player.midright = (WIDTH,HEIGHT/2)


cpu_strip = pygame.Rect(0,0,WIDTH/2,HEIGHT)
cpu_strip.centery = HEIGHT/2

player_strip = pygame.Rect(0,0,WIDTH/2,HEIGHT)
player_strip.midright = (WIDTH,HEIGHT/2)



ball_vel_x = 6
ball_vel_y = 6
player_vel = 0
cpu_speed = 4

cpu_points , player_points = 0 , 0

score_font = pygame.font.Font (None, 125)

while True:
    for event in pygame.event.get():  #checking for the events
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_UP:
                player_vel = -6
            if event.key == pygame.K_DOWN:
                player_vel = 6
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_UP:
                player_vel = 0
            if event.key == pygame.K_DOWN:
                player_vel = 0
           
           
    #animating ball and player
    animate_ball()
    animate_player()
    animate_cpu()
    
   
    
    #drawing all objects
    screen.fill("black")
    
    cpu_score_surface = score_font.render(str(cpu_points),True,"green")
    player_score_surface = score_font.render(str(player_points),True,"red")
    
    screen.blit(cpu_score_surface, (WIDTH/4,20))
    screen.blit(player_score_surface, (WIDTH*3/4,20))
    
    ball_color = "White"
    
    if ball.x >= WIDTH/2:
        ball_color = "red"
    else:
        ball_color = "green"
        
    
    pygame.draw.rect(screen,"red",cpu_strip)
    pygame.draw.rect(screen,"green",player_strip)
    
    pygame.draw.ellipse(screen,ball_color,ball)   #drawing ball
    
    screen.blit(cpu_score_surface, (WIDTH/4,20)) #score cpu
    screen.blit(player_score_surface, (WIDTH*3/4,20)) #score player
    
    pygame.draw.rect(screen,"white",cpu)
    pygame.draw.rect(screen,"white",player)
    pygame.draw.aaline(screen,"white",(WIDTH/2,0),(WIDTH/2,HEIGHT))
            
    pygame.display.update() #update the display
    clock.tick(FRAMERATE)    #frame rate (every computer will have same speed)
