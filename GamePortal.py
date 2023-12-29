import random
import os
import sys
import pygame
from pygame.locals import * 
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()

class Button:
    def __init__(self,text,pos,in_color="black",out_color="white",font_size=35,size=(500,75),text_color="white",x_shift = 50,screen = pygame.display.set_mode([900,600])):
        self.text = text
        self.pos = pos
        self.text_color = text_color
        self.in_color = in_color
        self.out_color = out_color
        self.size = size
        self.font_size = font_size
        self.x_shift = x_shift
        self.screen =screen
        self.font = pygame.font.Font("gallery/pixeloid-font/PixeloidSansBold-PKnYd.ttf",self.font_size)
        self.button = pygame.rect.Rect((self.pos[0],self.pos[1]),self.size)
        self.draw()

    def draw(self):
        pygame.draw.rect(self.screen,self.in_color,self.button,0,5)
        pygame.draw.rect(self.screen,self.out_color,self.button,5,5)
        text = self.font.render(self.text, True,self.text_color)
        self.screen.blit(text,(self.pos[0]+self.x_shift,self.pos[1]+(self.size[1]-self.font_size)/2))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

def draw_game():
    # pygame.display.set_mode([900,600]).fill('black')
    button = Button("Main Menu",[525,490],"black","white",30,(300,75))
    return button.check_clicked()

def draw_menu():
    command = 0
    # pygame.display.set_mode([900,600]).fill('black')
    Button("Games",[250,50],"black","black",60,(500,125))
    button1 = Button("Snakes",[40,200])
    button2 = Button("Space Dodge ",[40,275])
    inst_menu = Button("Instruction Menu",[40,350])

    if button1.check_clicked():
        command = 1
    elif button2.check_clicked():
        command = 2
    elif inst_menu.check_clicked():
        command = 3
    return command

def snake_game():
    # Colors
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0,0,255)
    violet = (127,0,255)
    black = (0, 0, 0)

    # Creating window
    screen_width = 900
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    #Background Image
    img = pygame.image.load("gallery/sprites/snakes_bgimage.jpg")
    bg_img = pygame.transform.scale(img, (screen_width, screen_height)).convert_alpha()


    # Game Title
    pygame.display.set_caption("Snakes Game")
    pygame.display.update()
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.SysFont(None, 55)

    def text_screen(text, color, x, y):
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, [x,y])


    def plot_snake(screen, color, snk_list, snake_size,head_color):
        for x,y in snk_list:
            if [x,y] in snk_list[:-1]:
                pygame.draw.rect(screen, color, [x, y, snake_size, snake_size])
            else:
                pygame.draw.rect(screen, head_color, [x, y, snake_size, snake_size])

    def welcome():
        exit_game = False
        while not exit_game:
            screen.blit(bg_img, (0, 0))
            text_screen("Welcome to Snakes", black, 260, 220)
            text_screen("Press Space Bar To Play", black, 232, 260)
            text_screen("Press Esc to return to Main Menu", black, 170, 300)
            text_screen("Press R To Restart", black, 232, 340)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameloop()
                    if event.key == pygame.K_ESCAPE:
                        Main_Menu()
            pygame.display.update()
            clock.tick(fps)


    # Game Loop
    def gameloop():
        # Game specific variables
        snake_x = 45
        snake_y = 55
        velocity_x = 0
        velocity_y = 0
        snk_list = []
        snk_length = 1
        exit_game = False
        game_over = False
        # Check if hiscore file exists
        if(not os.path.exists("gallery/snake_hiscore.txt")):
            with open("gallery/snake_hiscore.txt", "w") as f:
                f.write("0")

        with open("gallery/snake_hiscore.txt", "r") as f:
            hiscore = f.read()

        food_x = random.randint(20, screen_width // 2)
        food_y = random.randint(20, screen_height // 2)
        score = 0
        init_velocity = 5
        snake_size = 30
        food_radius = 15
        while not exit_game:
            if game_over:
                with open("gallery/snake_hiscore.txt", "w") as f:
                    f.write(str(hiscore))
                screen.blit(bg_img, (0, 0))
                text_screen("Game Over! Press Enter To Continue", red, 100, 250)

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
                            velocity_y = init_velocity
                            velocity_x = 0

                        if event.key == pygame.K_r:
                            gameloop()

                        if event.key == pygame.K_ESCAPE:
                            Main_Menu()

                snake_x = snake_x + velocity_x
                snake_y = snake_y + velocity_y

                if abs(snake_x- food_x)<25 and abs(snake_y - food_y)<25:
                    score +=10
                    food_x = random.randint(50, screen_width-50)
                    food_y = random.randint(50, screen_height-50)
                    snk_length +=5
                    pygame.mixer.music.load('gallery/audio/eat.mp3')
                    pygame.mixer.music.play()
                    if score>int(hiscore):
                        hiscore = score

                screen.blit(bg_img, (0, 0))
                text_screen("Score: " + str(score) + "  Hiscore: "+str(hiscore), blue, 5, 5)
                pygame.draw.circle(screen, red, [food_x, food_y], food_radius)

                head = []
                head.append(snake_x)
                head.append(snake_y)
                snk_list.append(head)

                if len(snk_list)>snk_length:
                    del snk_list[0]

                if head in snk_list[:-1]:
                    game_over = True
                    pygame.mixer.music.load('gallery/audio/die.wav')
                    pygame.mixer.music.play()

                if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                    game_over = True
                    pygame.mixer.music.load('gallery/audio/wall.mp3')
                    pygame.mixer.music.play()
                plot_snake(screen, violet, snk_list, snake_size,black)
            pygame.display.update()
            clock.tick(fps)
        pygame.quit()
        quit()
    welcome()

def space_dodge_game():
    def welcome():
        while True:
            fps = 60 
            clock = pygame.time.Clock()
            window.blit(BG, (0, 0))
            welcome_text = FONT.render("Welcome to Space Dodge!!", True, "white")
            play_text = FONT.render("Press Space Bar To Play", True, "white")
            return_text = FONT.render("Press Esc to return to Main Menu",True,"white")
             
            window.blit(welcome_text, (width/2 - welcome_text.get_width()/2, height/2 -35 - welcome_text.get_height()/2))
            window.blit(play_text, (width/2 - play_text.get_width()/2, height/2 - play_text.get_height()/2))
            window.blit(return_text, (width/2 - return_text.get_width()/2, height/2 +10+ play_text.get_height()/2 - return_text.get_height()/2))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main()
                    if event.key == pygame.K_ESCAPE:
                        Main_Menu()
            pygame.display.update()
            clock.tick(fps)

    def draw(player, elapsed_time, stars):
        window.blit(BG, (0, 0))

        score = FONT.render(f"Score: {round(elapsed_time)*10}", 1, "white")
        window.blit(score, (10, 10))

        pygame.draw.rect(window, "red", player)

        for star in stars:
            pygame.draw.rect(window, "white", star)

        pygame.display.update()

    def main():
        run = True

        player = pygame.Rect(500, height - player_height, player_width, player_height)
        clock = pygame.time.Clock()
        start_time = time.time()
        elapsed_time = 0

        star_add_increment = 2000
        star_count = 0

        stars = []
        hit = False

        while run:
            star_count += clock.tick(60)
            elapsed_time = time.time() - start_time

            if star_count > star_add_increment:
                for _ in range(3):
                    star_x = random.randint(0, width - star_width)
                    star = pygame.Rect(star_x, -star_height,star_width, star_height)
                    stars.append(star)

                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Main_Menu()
                    if event.key == pygame.K_r:
                        main()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - player_velocity >= 0:
                player.x -= player_velocity
            if keys[pygame.K_RIGHT] and player.x + player_velocity + player.width <= width:
                player.x += player_velocity

            for star in stars[:]:
                star.y += star_velocity
                if star.y > height:
                    stars.remove(star)
                elif star.y + star.height >= player.y and star.colliderect(player):
                    stars.remove(star)
                    hit = True
                    break

            if hit:
                pygame.mixer.music.load('gallery/audio/die.wav')
                pygame.mixer.music.play()
                lost_text = FONT.render("You Lost!", True, "white")
                return_text = FONT.render("Press Esc to return to Main Menu", True, "white")
                restart_text = FONT.render("Please wait till the game restarts",True,"white")
                        
                window.blit(lost_text, (width/2 - lost_text.get_width()/2, height/2 - return_text.get_height()/2 - lost_text.get_height()/2-10))
                window.blit(return_text, (width/2 - return_text.get_width()/2, height/2 - return_text.get_height()/2))
                window.blit(restart_text, (width/2 - restart_text.get_width()/2, height/2 +10+ return_text.get_height()/2 - restart_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(2000)
                main()
                break

            draw(player, elapsed_time, stars)

        pygame.quit()

    width, height = 900, 600
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Space Dodge")

    BG = pygame.transform.scale(pygame.image.load("gallery/sprites/spc.jpg"), (width, height))

    player_width = 20
    player_height = 60

    player_velocity = 5
    star_height = 20
    star_width = 10
    star_velocity = 3

    FONT = pygame.font.SysFont("comicsans", 30)
    welcome()

def Main_Menu():
    w = 900
    h = 600
    screen = pygame.display.set_mode([w,h])
    pygame.display.set_caption("Menu tutorial")

    font = pygame.font.Font("gallery/pixeloid-font/PixeloidSansBold-PKnYd.ttf",15)
    fps = 60
    timer = pygame.time.Clock()

    main_menu = True
    menu_command = 0
    run = True

    while run:
        screen.fill('black')
        timer.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if main_menu:
            menu_command = draw_menu()
            if menu_command>0:
                main_menu = False
        else:
            main_menu = draw_game()
            if menu_command==1:
                snake_game()
            elif menu_command==2:
                space_dodge_game()
            else:
                with open("gallery/instruction.txt","r") as f:
                    ins_text = f.readlines()
                    line = 1
                    for i in ins_text:
                        text = font.render(i, True, 'white')
                        screen.blit(text,(5,20*line))
                        line +=1
        pygame.display.update()
    pygame.quit()

if __name__=="__main__":
    Main_Menu()