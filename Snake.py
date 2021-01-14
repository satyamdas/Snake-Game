import pygame
import random
import os

pygame.mixer.init()
# pygame.mixer.music.load("")
# pygame.mixer.music.play()

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

screen_width = 900
screen_height = 500

clock = pygame.time.Clock()

# Creating Window
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snakes")
pygame.display.update()

# background image
bgimg = pygame.image.load("img.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


font = pygame.font.SysFont(None, 55)
def screen_score(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((21, 123, 150))
        screen_score("Welcome to Snakes", black, 250, 200)
        screen_score("Press Space Bar to Play", black, 230, 250 )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        pygame.display.update()
        clock.tick(60)

# Creating a game loop
def game_loop():
    # Game specific variables
    exit_game = False
    game_over = False 

    snake_x = 45
    snake_y = 55

    velocity_x = 0
    velocity_y = 0

    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)

    snake_list = []
    snake_length = 1 

    score = 0
    init_velocity = 5

    snake_size = 10
    fps = 60

    # Check if hiscore file exists
    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            screen_score("Game Over! Press Enter to Continue", red, 100, 200) 

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome() 

        else:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y =  init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 5

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6:
                score += 10
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snake_length += 5
                if score > int(hiscore):
                    hiscore = score


            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            screen_score("Score: " + str(score) + "  Hiscore: "+ str(hiscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)> snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True

            plot_snake(gameWindow, blue, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)



        
    pygame.quit()
    quit() 

# game_loop()
welcome()