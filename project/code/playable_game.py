from sys import exit
import pygame
import time
from random import random, randint, randrange
import os
pygame.init()
main_win = pygame.display.set_mode((800,600)) 
highscore_file = "highscore.txt"

#read high score from file
def read_highscore():
    if os.path.exists(highscore_file):
        with open(highscore_file, 'r') as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    else:
        return 0

#write high score to file
def write_highscore(score):
    with open(highscore_file, 'w') as file:
        file.write(str(score))

# Initialize high score
high_score = read_highscore()

# Update high score function
def update_highscore(score):
    global high_score
    if score > high_score:
        high_score = score
        write_highscore(high_score)

#display high score on screen
def display_highscore():
    highscore_font = pygame.font.Font("Instructions.ttf", 75)
    highscore_surf = highscore_font.render(f"Highscore: {high_score}", True, "black")
    main_win.blit(highscore_surf, (200, 400))


def grid(): # 13 x 10 grid with each box having 50 pixels as side length
    for x in range(50,750,50):
        pygame.draw.line(main_win, "white", (x, 50), (x, 550))
    for y in range(50,750,50):
        pygame.draw.line(main_win,"white", (50, y), (700, y))
dir = [1,2,3,4]
u,d,l,r = dir  #up, down, left, right
snake_dir = r
#green_surf = pygame.Surface((40,40))    
#green_surf.fill("green")
#green_rect = green_surf.get_rect(center = (740, 350))
#yellow_surf = pygame.Surface((40,40))
#yellow_surf.fill("yellow")
#yellow_rect = yellow_surf.get_rect(center = (740, 400))
#red_surf = pygame.Surface((40,40))
#red_surf.fill("red")
#red_rect = red_surf.get_rect(center = (740, 450))


class Food:
    def __init__(self):
        self.x = randrange(50,700,50)
        self.y = randrange(50,550,50)
        self.apple_in_surf = pygame.image.load("apple_in.png").convert_alpha()
        self.apple_in_transform_surf = pygame.transform.rotozoom(self.apple_in_surf, 0, 2)
        self.apple_in_rect = self.apple_in_surf.get_rect(midbottom = ((self.x + 14),(self.y + 25))) 

    def draw(self):
        main_win.blit(self.apple_in_transform_surf, self.apple_in_rect)

    def respawn(self, snake_body):         #apple spawns outside the snake's body
        while True:
            self.x = randrange(50, 700, 50)
            self.y = randrange(50, 550, 50)
            self.apple_in_rect = self.apple_in_surf.get_rect(midbottom=((self.x + 14), (self.y + 25)))
            
            # Check if the new apple position overlaps with any part of the snake's body
            overlapping = False
            for segment in snake_body:
                if self.apple_in_rect.colliderect(segment):
                    overlapping = True
                    break
            
            if not overlapping:
                break


apple = Food()

      
class Snake: 
    def __init__(self):
        self.xmov = 1
        self.ymov = 0
        self.x = 350
        self.y = 250
        #self.lives_count = 3
        self.snake_head = pygame.Rect(self.x, self.y, 50,50) 
        self.snake_body = [pygame.Rect(self.x - 50,self.y, 50, 50)] #list so that on eating, new body (block) is generated
        #head needs to be a block ahead of the body in x dir
        self.snake_eyes = [pygame.Rect(self.x + 10, self.y + 10, 10, 10), #snake's eyes
                           pygame.Rect(self.x + 30, self.y + 10, 10, 10)]
        self.is_dead = False
        self.game_over = False
        #self.lives_list = [green_surf, yellow_surf, red_surf]
        #self.lives_rect = [green_rect, yellow_rect, red_rect]
    

    def positioning(self): #predecessing block gets the position of the block ahead of it and updates for every block ahead of it
        for s in self.snake_body:
            if(self.snake_head.colliderect(s)):
                self.is_dead = True
            if(self.snake_head.x not in range(50, 700) or self.snake_head.y not in range(50,550)):
                self.is_dead = True
                pygame.draw.rect(main_win,"black", self.snake_head)
        if(self.is_dead):
            self.game_over = True
            global apple  #on collision, apple needs to be positioned to a different place 
            #self.lives_count -=1           -> three lives implementation has been removed
            #if(self.lives_count == 2):
                #self.lives_list.remove(green_surf)
            #elif (self.lives_count == 1):
                #self.lives_list.remove(yellow_surf)
           #elif (self.lives_count == 0):
                #self.lives_list.remove(red_surf)     
            #elif(self.lives_count <0):
                #self.lives_count = -1
            #self.xmov = 1
            #self.ymov = 0
            #self.x = 350
            #self.y = 250
            #self.snake_head = pygame.Rect(self.x, self.y, 50,50) 
            #self.snake_body = [pygame.Rect(self.x - 50,self.y, 50, 50)] 
            #self.is_dead = False
            #apple = Food()
           
        self.snake_body.append(self.snake_head) #appends head and body as the snake "collides" with apple -> given in later method
        l = len(self.snake_body)
        for i in range(l-1):
            self.snake_body[i].x = self.snake_body[i+1].x
            self.snake_body[i].y = self.snake_body[i+1].y
        self.snake_head.x += self.xmov * 50  #responds to input event
        self.snake_head.y += self.ymov * 50
        self.snake_body.remove(self.snake_head)


    def draw_eyes(self):
        for eye in self.snake_eyes:
            pygame.draw.rect(main_win, "black", eye)

    def update_eyes_position(self):
        # Update eyes positions based on the snake's head position
        self.snake_eyes[0].x = self.snake_head.x + 10
        self.snake_eyes[0].y = self.snake_head.y + 10
        self.snake_eyes[1].x = self.snake_head.x + 30
        self.snake_eyes[1].y = self.snake_head.y + 10

        
snake = Snake()

def show_game_over(): #wait 2 seconds after game over to execute following code
    game_over_font = pygame.font.Font("Instructions.ttf", 75)
    game_over_surf = game_over_font.render("GAME OVER!", True, "Red")
    main_win.blit(game_over_surf, (180,250))
    pygame.display.flip()
    time.sleep(2)

grid_surf = pygame.Surface((650,500))
grid_surf.fill("mediumpurple2")
grid_rect = grid_surf.get_rect(topleft = (50,50))
#game_win = pygame.display.set_mode((800,800)) #1600, 800 covers the whole main_win
pygame.display.set_caption("Snake game")
snake_front_surf = pygame.image.load("SnakeHeader_Front.png").convert_alpha()
background_front_surf = pygame.Surface((800,600))
background_front_surf.fill("green2")
apple_front_surf = pygame.image.load("apple_front.png").convert_alpha()
apple_front_transform_right = pygame.transform.rotozoom(apple_front_surf, 315, 1)
font_front = pygame.font.Font("Font1.ttf", 50)
font_front_surf = font_front.render("Mr. Snake's Snack", True, "deeppink")
font_front_ins = pygame.font.Font("Instructions.ttf", 35)
font_front_ins_surf = font_front_ins.render("Press Space to Play!", True, "black")
#score_front = pygame.font.Font("Instructions.ttf", 70)
highscore_surf = pygame.image.load("highscore_front.png").convert_alpha()
highscore_transform_surf = pygame.transform.rotozoom(highscore_surf, 0, 0.3)
score_game = pygame.font.Font("Instructions.ttf", 40)
#timer_ins = pygame.USEREVENT + 1
#pygame.time.set_timer(timer_ins,1000)
active = False
active_in = False
active_in_temp = True
game_over = False
#timer = 0
score = 0
#ind = 0


clock = pygame.time.Clock()
while True: 
    if(not active): #home screen
        #timer_temp = pygame.time.get_ticks()//1000
        timer_front = pygame.time.get_ticks()//750
        main_win.blit(background_front_surf, (0,0))
        if (timer_front%2 == 0):
            main_win.blit(apple_front_surf, (200,125))
        else:
            main_win.blit(apple_front_transform_right, (200,125))

        
        main_win.blit(font_front_surf, (40,25))
        main_win.blit(snake_front_surf, (400,-50))
        main_win.blit(font_front_ins_surf, (75,275))
        main_win.blit(highscore_transform_surf, (50,350))
        display_highscore()
        #score_front_surf = score_front.render(f"Highscore: {score}", True, "Black")
        #main_win.blit(score_front_surf, (200, 400))



    
    #timer = (pygame.time.get_ticks())//1000 - timer_temp 
    #timer_game_over = pygame.time.get_ticks()//1000

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            exit()
        if(event.type == pygame.KEYDOWN):
            if event.key == pygame.K_UP and snake_dir != d:
                snake_dir = u
            elif event.key == pygame.K_DOWN and snake_dir != u:
                snake_dir = d
            elif event.key == pygame.K_LEFT and snake_dir != r:
                snake_dir = l
            elif event.key == pygame.K_RIGHT and snake_dir != l:
                snake_dir = r
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_SPACE):
                active = True

    
    if snake_dir == u:
        snake.xmov = 0
        snake.ymov = -1
    elif snake_dir == d:
        snake.xmov = 0
        snake.ymov = 1
    elif snake_dir == l:
        snake.xmov = -1
        snake.ymov = 0
    elif snake_dir == r:
        snake.xmov = 1
        snake.ymov = 0


    if(active):
        if(active_in == False or active_in == True):
            background_surf = pygame.Surface((800,600))
            background_surf.fill("Black")
            main_win.blit(background_surf, (0,0))
            main_win.blit(grid_surf, grid_rect)
            grid()
            pygame.draw.rect(main_win, "green2", snake.snake_head)
            snake.draw_eyes()
            for s in snake.snake_body:
                 pygame.draw.rect(main_win, "green2", s)
            apple.draw() 

            if(active_in_temp):
                press_key = pygame.font.Font("Instructions.ttf", 25)
                press_key_surf = press_key.render("Press Right Key to start", True, "white")
                main_win.blit(press_key_surf, (250,15))
                    #main_win.blit(red_surf, red_rect)
                    #main_win.blit(yellow_surf,yellow_rect)
                    #main_win.blit(green_surf, green_rect)
                keys = pygame.key.get_pressed()
                if(keys[pygame.K_RIGHT]):
                    active_in = True
                    active_in_temp = False


        if(active_in):
            if(not game_over):
                score_game_surf = score_game.render(f"{score}", True, "White")
                main_win.blit(score_game_surf, (725, 200))
                snake.positioning()
                snake.update_eyes_position()
                #if(snake.lives_list):         -> used for "three lives" in the first stage of the development
                    #for l in snake.lives_list:       
                        #main_win.blit(l, snake.lives_rect[ind])
                        #ind += 1
                        #if(ind >= len(snake.lives_list)):
                            #ind = 0
                #if(not snake.lives_list):
                    #game_over = True
                if(snake.snake_head.colliderect(apple.apple_in_rect)):
                    score +=1
                    snake.snake_body.append(pygame.Rect(s.x, s.y, 50,50))
                    apple.respawn(snake.snake_body)
                    
        if(snake.game_over):
                #for i in [green_surf, yellow_surf, red_surf]:
                # snake.lives_list.append(i)
                #snake.lives_count = 3
                #ind = 0
            background_surf = pygame.Surface((800,600))
            background_surf.fill("Black")
            main_win.blit(background_surf, (0,0))
            main_win.blit(grid_surf, grid_rect)
            grid()
            show_game_over()
            update_highscore(score)
            snake.game_over = False
            exit()
            
            #active_in_temp = True
            #active = False
            #game_over = False
        #if(timer % 2 == 0): #-> just to check if the apples are being place randomly in a box
           #x = randrange(50,750,50)
            #y = randrange(50,750,50)
           #apple_pos(x,y)


    pygame.display.update()
    clock.tick(10)
