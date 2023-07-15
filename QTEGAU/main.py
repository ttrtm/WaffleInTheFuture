import pygame, time, random, pickle, os
#бібліотека для часу, випадковостей, збереження прогресу, і роботи з файлами
from components import*
from time import sleep
# Ініціалізація Pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 20)  

# Розміри вікна
width = 1280
height = 720

# Ініціалізація вікна
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("РГПУ-2100")
clock = pygame.time.Clock()

# Фон та кольори
blue = (0, 255, 255)
brown = (153, 51, 0)
green = (124, 252, 0)
dark_green = (34,139,34)
purple = (138,43,226)
yellow = (255,255,0)
black = (0,0,0)
white = (255,255,255)
#це мало б бути перед головним циклом, але тоді не вийде працювати з деякими функціями так класами :)
gravity = 1
down_limit = 150 #з якого моменту починає рухатись камера
camera_y = 0   
#клас для тексту
font_path = "fonts/PressStart2P-Regular.ttf"
font = pygame.font.Font(font_path)
class Label(Area):
    def set_text(self, text, font_size=28, text_color=(0, 0, 0)):
        self.text = text
        self.font_size = font_size
        self.image = pygame.font.SysFont(font_path, font_size).render(text, True, text_color)

    def draw(self, window, shift_x=0, shift_y=0):
        window.blit(self.image, (self.rect.x, self.rect.y - camera_y, self.rect.width, self.rect.height))

# об'єкти для початкового меню
menu_start_button = Picture("image/menu_start_button.png", 550, 300, width=160, height=160)
darken_start_button = Picture("image/dark_menu_start_button.png", 550, 300, width=160, height=160)
menu_settings_button = Picture("image/menu_settings.png", 425, 450, width=110, height=110)
darken_settings_button = Picture("image/dark_menu_settings.png", 425, 450, width=110, height=110)
menu_credits_button = Picture("image/menu_credits.png", 575, 550, width=110, height=110)
darken_credits_button = Picture("image/dark_menu_credits.png", 575, 550, width=110, height=110)
menu_exit_button = Picture("image/exit_button.png", 725, 450, width=110, height=110)
darken_exit_button = Picture("image/dark_exit_button.png", 725, 450, width=110,height=110)

#об'єкти для налаштувань
how_to_play = Label(25,125,100,50)
how_to_play.set_text("Донесіть вафельку до фінішу, натискаючи на клавіші, які будуть появлятись на екрані, для того щоб стрибати по платформах.")
levels = Label(200, 525, 100, 50)
levels.set_text("Оберіть рівень складності:")
movement = Label(150, 275, 100, 50)
movement.set_text("Оберіть спосіб пересування:")

first_level = Picture("image/first_level.png",500, 600, 110, 110)
dark_first_level = Picture("image/dark_first_level.png", 500, 600, 110, 110)
second_level = Picture("image/second_level.png", 575, 500, 110,110)
dark_second_level = Picture("image/dark_second_level.png", 575, 500, 110, 110)
thirst_level = Picture("image/thirst_level.png", 650, 600, 110, 110)
dark_thirst_level = Picture("image/dark_thirst_level.png", 650, 600, 110, 110)
wasd = Picture("image/WASD.png", 450, 300, 110, 110)
dark_wasd = Picture("image/dark_WASD.png", 450, 300, 110, 110)
errows = Picture("image/arrows.png", 700, 300, 110, 110)
dark_errows = Picture("image/dark_arrows.png", 700, 300, 110, 110)

#Автори
game_designers = Label(25,125,100,50)
game_designers.set_text("Гейм дизайнер: Юник Вадим")
programmers = Label(25,200,100,50)
programmers.set_text("Програмісти: Юник Вадим")
game_artists = Label(25, 275, 100, 50)
game_artists.set_text("Художники: Юник Вадим")
testers = Label(25, 350, 100, 50)
testers.set_text("Тестери: Юник Вадим")

#об'єкти для гри
WIN = Label(width // 2 - 100, width // 4, 100, 50)
WIN.set_text("Перемога!")
lose = Label(width // 2 - 100 ,width // 4, 100, 50)
lose.set_text("Ви програли!")
texture_of_roof = Picture("image/texture_of_roof.png", 0, 515, 1280, 154)

#об'єкти для паузи
newly = Picture("image/newly.png", width // 2.5 - 55, height // 2 - 55, 110, 110)
dark_newly = Picture("image/dark_newly.png", width // 2.5 - 55, height // 2 - 55, 110, 110)
pause_settings = Picture("image/menu_settings.png", width // 2 + width // 8 - 55, height // 2 - 55, 110, 110)
dark_pause_settings = Picture("image/dark_menu_settings.png", width // 2 + width // 8 - 55, height // 2 - 55, 110, 110)
pause_exit_button = Picture("image/exit_button.png", 610, 480, width=110, height=110)
darken_pause_exit_button = Picture("image/dark_exit_button.png", 610, 480, width=110,height=110)

# універсальні об'єкти
back_button = Picture("image/back_button.png", 40, 30, width=95, height=75)
darken_back_button = Picture("image/dark_back_button.png", 40, 30, width=95, height=75)
background = Picture("image/background.png", 0, -8500, 1280, 8500)

# Графіка для гравця і предметів
player_image = pygame.image.load("image/player.png")
player_image = pygame.transform.scale(player_image, (65, 65))
flag_image = pygame.image.load("image/вафелька.png")
flag_image = pygame.transform.scale(flag_image, (30,30))

#прогрес
def save_game():
    progress = {
        'camera_y': camera_y,
        'player_position': (player.rect.x, player.rect.y - camera_y),
        'has_flag': player.has_flag,
        'has_weapon': player.has_weapon,
        'can_win': player.can_win
    }
    with open('data/progress', 'wb') as file:
        pickle.dump(progress, file)
def load_game():
    try:
        with open('data/progress', 'rb') as file:
            progress = pickle.load(file)
        camera_y = progress['camera_y']
        player.rect.x, player.rect.y = progress['player_position'][0], progress['player_position'][1] - camera_y
        player.has_flag = progress['has_flag']
        player.has_weapon = progress['has_weapon']
        player.can_win = progress['can_win']
    except FileNotFoundError:
        print("Збереженого прогресу не знайдено.")
def clear_progress():
    if os.path.exists('data/progress'):
        os.remove('data/progress')


class Player:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.y_velocity = 0
        self.speed = speed
        self.jump_power = 15
        self.has_flag = True
        self.has_weapon = False
        self.can_win = False
        self.jump_key = pygame.K_UP
        self.left_key = pygame.K_a
        self.right_key = pygame.K_d

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.left_key] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[self.right_key] and self.rect.x < width- 50:
            self.rect.x += self.speed
        if keys[self.jump_key]:
            self.y_velocity -= self.jump_power
            self.jump_key = random.choice([pygame.K_SPACE, pygame.K_SPACE, pygame.K_SPACE, pygame.K_SPACE, pygame.K_SPACE, pygame.K_t, pygame.K_f, pygame.K_k, pygame.K_y, pygame.K_l, pygame.K_h, pygame.K_g, pygame.K_m, pygame.K_n, pygame.K_b, pygame.K_v, pygame.K_i, pygame.K_u, pygame.K_o, pygame.K_y, pygame.K_t])
        jump_key_name = pygame.key.name(self.jump_key)
        key_text = Label(100, 100, 100, 50)
        key_text.set_text("Jump key: " + jump_key_name)
        key_text.draw(window)

        self.y_velocity += gravity
        self.rect.y += self.y_velocity
        save_game()

        print(self.rect.y)

        if self.rect.colliderect(finish_platform_.rect) and self.has_flag:
            self.has_flag = False
            self.has_weapon = True
            self.can_win = True
            
        if not self.has_flag:
            window.blit(flag_image, (finish_platform_.rect.x + 200, finish_platform_.rect.y - camera_y))

    def draw(self):
        window.blit(player_image, (self.rect.x, self.rect.y - camera_y))
        if self.has_flag:
            window.blit(flag_image, (self.rect.x + 25, self.rect.y - camera_y + 25))
            

class Platform:
    def __init__(self, window, x, y, width, height, speed, direction, color, graphick):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = direction
        self.color = color
        self.graphick = graphick
        self.window = window
    def move(self):
        self.rect.x += self.speed * self.direction

        if self.rect.right >= width or self.rect.left <= 0:
            self.direction *= -1

    def draw(self):
        self.window.blit(self.graphick, self.rect)

camera_speed = 5
camera_limit = height // 4

#x, y, width, height, speed
player = Player(width // 2 - 25, height - 60, 65, 65, 5)

#платформи
#x, y, width, height, speed, direction, color
platform1 = Platform(window, width // 2 - 70, height - 200, 140, 20, 1, 1, purple, pygame.image.load("image/start_platform 140x20.png"))
platform2 = Platform(window,200, height - 300, 70, 20, 4, 1, brown,pygame.image.load("image/platform 70x20.png"))
platform3 = Platform(window,0, height - 400,70, 20, 0, 1, brown,pygame.image.load("image/platform 70x20.png"))
platform4 = Platform(window,100,height - 500,70, 20, 5, 1, brown,pygame.image.load("image/platform 70x20.png"))
platform5 = Platform(window,700,height - 600,70, 20, 0, 1, brown,pygame.image.load("image/platform 70x20.png"))
platform6 = Platform(window,860,height - 700,70, 20, 0, 1, brown,pygame.image.load("image/platform 70x20.png"))
platform7 = Platform(window,150,height - 800,70, 20, 5, 1, brown,pygame.image.load("image/platform 70x20.png"))
platform8 = Platform(window,0,-180, 620, 20, 0, 1, dark_green,pygame.image.load("image/platform 620x20.png"))
platform8_9= Platform(window,width // 2, -320, 70, 20, 3,-1, dark_green,pygame.image.load("image/platform 70x20.png")) 
platform9 = Platform(window,0,-450,500, 20, 0, 1, dark_green,pygame.image.load("image/platform 500x20.png"))
platform10 = Platform(window,800, -580, 100, 20, 3, -1, brown,pygame.image.load("image/platform 100x20.png"))
platform11 = Platform(window,0, -750, 40, 20, 3, 1, dark_green,pygame.image.load("image/platform 40x20.png"))
platform12 = Platform(window,640, -850, 40, 20, 3, -1, dark_green,pygame.image.load("image/platform 70x20.png"))
platform13 = Platform(window,100, -950, 40, 20, 3, 1, dark_green,pygame.image.load("image/platform 70x20.png"))
platform14 = Platform(window,100, -1050, 70, 20, 0, 1, purple,pygame.image.load("image/elevator.png"))
platform15 = Platform(window,100, -1150, 70, 20, 0, 1, purple, pygame.image.load("image/elevator.png"))
platform16 = Platform(window,100, -1250, 70, 20, 0, 1, purple, pygame.image.load("image/elevator.png"))
platform17 = Platform(window,100, -1350, 70, 20, 0, 1, purple, pygame.image.load("image/elevator.png"))
platform18 = Platform(window,100, -1450, 70, 20, 0, 1, purple, pygame.image.load("image/elevator.png"))
platform14_2 = Platform(window,1110, -1050, 70, 20, 0, 1, purple, pygame.image.load("image/elevator.png"))
platform15_2 = Platform(window,1110, -1150, 70, 20, 0, 1, purple, pygame.image.load("image/elevator.png"))
platform16_2 = Platform(window,1110, -1250, 70, 20, 0, 1, purple, pygame.image.load("image/elevator.png"))
platform17_2 = Platform(window,1110, -1350, 70, 20, 0, 1, purple, pygame.image.load("image/elevator.png"))
platform18_2 = Platform(window,1110, -1450, 70, 20, 0, 1, purple, pygame.image.load("image/elevator.png"))
platform19 = Platform(window,500, -1600, 70, 20, 5, 1, dark_green,pygame.image.load("image/platform 70x20.png"))
platform20 = Platform(window,0, -1650, 90, 20, 4, 1, dark_green, pygame.image.load("image/platform 90x20.png"))
platform21 = Platform(window,0, -1750, 50, 20, 2, 1, dark_green, pygame.image.load("image/platform 50x20.png"))
platform22 = Platform(window,0, -1850, 60, 20, 3, 1, dark_green, pygame.image.load("image/platform 60x20.png"))
platform23 = Platform(window,0, -1950, 150, 20, 5, 1, dark_green, pygame.image.load("image/platform 150x20.png"))
platform24 = Platform(window,0, -2050, 20, 20, 1, 1, dark_green, pygame.image.load("image/mini_elevator.png"))
platform25 = Platform(window,0, -2150, 50, 20, 2, 1, dark_green, pygame.image.load("image/platform 50x20.png"))
platform26 = Platform(window,0, -2250, 70, 20, 4, 1, dark_green,pygame.image.load("image/platform 70x20.png"))
platform27 = Platform(window,0, -2350, 40, 20, 3, 1, dark_green, pygame.image.load("image/platform 40x20.png"))
platform28 = Platform(window,0, -2450, 100, 20, 4, 1, dark_green, pygame.image.load("image/platform 100x20.png"))
platform29 = Platform(window,0, -2550, 90, 20, 2, 1, dark_green, pygame.image.load("image/platform 90x20.png"))
platform30 = Platform(window,width - 200, -2650, 100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform31 = Platform(window,width - 350, -2800, 100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform32 = Platform(window,width - 500, -2950, 100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform33 = Platform(window,width - 650, -3100, 100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform34 = Platform(window,width - 800, -3250, 100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform35 = Platform(window,width - 950, -3400,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform36 = Platform(window,width - 1100, -3550,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform37 = Platform(window,50, -3700,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform38 = Platform(window,200, -3850,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform39 = Platform(window,350, -4000,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform40 = Platform(window,500, -4150,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform41 = Platform(window,650, -4300,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform42 = Platform(window,800, -4450,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform43 = Platform(window,950, -4600,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform44 = Platform(window,1100, -4750,  100, 15, 0, 1, yellow, pygame.image.load("image/platform 100x20.png"))
platform45 = Platform(window,0, -4900,  1030, 20, 0, 1, dark_green, pygame.image.load("image/platrform 1030x20.png"))
platform46 = Platform(window,0, -5050, 200, 17, 0, 1, dark_green, pygame.image.load("image/platform 200x17.png"))
platform46_47 = Platform(window,0, -5200,80, 17, 5, 1, dark_green, pygame.image.load("image/platform 80x17.png"))
platform47 = Platform(window,480, -5300, 800, 17, 0, 1, dark_green, pygame.image.load("image/platform 800x17.png"))
platform48 = Platform(window,width // 2, -5450, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform49 = Platform(window,width // 2, -5600, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform50 = Platform(window,width // 2, -5750, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform51 = Platform(window,width // 2, -5900, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform52 = Platform(window,width // 2, -6050, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform53 = Platform(window,width // 2, -6200, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform54 = Platform(window,width // 2, -6350, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform55 = Platform(window,width // 2, -6500, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform56 = Platform(window,width // 2, -6650, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform57 = Platform(window,width // 2, -6800, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform58 = Platform(window,width // 2, -6950, 20,20, 0, 1, purple,pygame.image.load("image/mini_elevator.png"))
platform59 = Platform(window,0, -7100, 70, 15, 5, 1, brown, pygame.image.load("image/platform 70x15.png"))
platform60 = Platform(window,500, -7250, 70, 15, 5, -1, brown, pygame.image.load("image/platform 70x15.png"))
platform61 = Platform(window,0, -7400, 70, 15, 5, 1, brown, pygame.image.load("image/platform 70x15.png"))
base_platform = Platform(window,0, height - 60, width, 1000, 0, 0, green,pygame.image.load("image/base_platform.png"))
finish_platform = Platform(window,0, -7550 - 439, width - 100, 30, 0, 0, green, pygame.image.load("image/finish_platform.png"))
finish_platform_ = Platform(window, 0, -7560,width - 100, 30, 0, 0, green, pygame.image.load("image/finish_platform_.png"))

platforms = [base_platform, finish_platform,platform1, platform2, platform3, platform4,platform5, platform6, platform7, platform8,platform9,platform8_9,platform10,platform11,platform12,platform13,platform14,platform15,platform16,platform17,platform18,platform14_2,platform15_2,platform16_2,platform17_2,platform18_2,platform19,platform20,platform21,platform22,platform23,platform24,platform25,platform26,platform27,platform28,platform29,platform30,
platform31, platform32,platform33, platform34, platform35, platform36, platform37, platform38, platform39, platform40, platform41,platform42, platform43,platform44, platform45, platform46, platform46_47, platform47, platform48, platform49, platform50, platform51,platform52,platform53,platform54,platform55,platform56, platform57, platform58, platform59, platform60, platform61, finish_platform_]

# Головний цикл гри
running = True
full_screen = False
screen = "menu"
screen_ = "menu"
paused = False
counter = 0
load_game()


while running:
    window.fill(blue)
    counter += 1
    
    if screen == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # зміна форми вікна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu_settings_button.rect.collidepoint(x, y):
                    screen = "settings"
                elif menu_credits_button.rect.collidepoint(x, y):
                    screen = "credits"
                elif menu_start_button.rect.collidepoint(x, y):
                    screen = "game"
                elif menu_exit_button.rect.collidepoint(x,y):
                    running = False
                

        # Кнопка старту
        mouse_pos = pygame.mouse.get_pos()
        if menu_start_button.rect.collidepoint(mouse_pos):
            darken_start_button.draw(window)
        else:
            menu_start_button.draw(window)

        # Кнопка налаштування
        if menu_settings_button.rect.collidepoint(mouse_pos):
            darken_settings_button.draw(window)
        else:
            menu_settings_button.draw(window)

        # Кнопка credits
        if menu_credits_button.rect.collidepoint(mouse_pos):
            darken_credits_button.draw(window)
        else:
            menu_credits_button.draw(window)
        
        #кнопка виходу з гри
        if menu_exit_button.rect.collidepoint(mouse_pos):
            darken_exit_button.draw(window)
        else:
            menu_exit_button.draw(window)


    elif screen == "settings":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # зміна форми вікна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button.rect.collidepoint(x, y):
                    if screen_ == "pause":
                        screen = "pause"
                    else:
                        screen = "menu"
                #зміна рівня складності
                elif first_level.rect.collidepoint(x, y):
                    levels.set_text("Рівень складності = 1")
                    down_limit = 150
                    gravity = 0.75
                elif second_level.rect.collidepoint(x, y):
                    levels.set_text("Рівень складності = 2")
                    down_limit = 70
                    gravity = 1
                elif thirst_level.rect.collidepoint(x, y):
                    levels.set_text("Рівень складності = 3")
                    down_limit = 0
                    gravity = 1
                #зміна управління
                elif wasd.rect.collidepoint(x, y):
                    player.left_key = pygame.K_a
                    player.right_key = pygame.K_d
                    movement.set_text("Управління тепер відбувається за допомогою клавіш WASD")
                elif errows.rect.collidepoint(x, y):
                    player.left_key = pygame.K_LEFT
                    player.right_key = pygame.K_RIGHT
                    movement.set_text("Управління відбувається за допомогою стрілок")
                    
        mouse_pos = pygame.mouse.get_pos()
        if first_level.rect.collidepoint(mouse_pos):
            dark_first_level.draw(window)
        else:
            first_level.draw(window)
        mouse_pos = pygame.mouse.get_pos()
        if second_level.rect.collidepoint(mouse_pos):
            dark_second_level.draw(window)
        else:
            second_level.draw(window)
        if thirst_level.rect.collidepoint(mouse_pos):
            dark_thirst_level.draw(window)
        else:
            thirst_level.draw(window)
        if wasd.rect.collidepoint(mouse_pos):
            dark_wasd.draw(window)
        else:
            wasd.draw(window)
        if errows.rect.collidepoint(mouse_pos):
            dark_errows.draw(window)
        else:
            errows.draw(window)

        mouse_pos = pygame.mouse.get_pos()
        if back_button.rect.collidepoint(mouse_pos):
            darken_back_button.draw(window)
        else:
            back_button.draw(window)
        
        how_to_play.draw(window)
        levels.draw(window)
        movement.draw(window)

    elif screen == "credits":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # зміна форми вікна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button.rect.collidepoint(x, y):
                    screen = "menu"

        # Вихід
        mouse_pos = pygame.mouse.get_pos()
        if back_button.rect.collidepoint(mouse_pos):
            darken_back_button.draw(window)
        else:
            back_button.draw(window)
        # Автори
        game_designers.draw(window)
        programmers.draw(window)
        game_artists.draw(window)
        testers.draw(window)
    
    elif screen == "win or lose":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # зміна форми вікна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button.rect.collidepoint(x, y):
                    screen = "menu"
        mouse_pos = pygame.mouse.get_pos()
        if back_button.rect.collidepoint(mouse_pos):
            darken_back_button.draw(window)
        else:
            back_button.draw(window)
        if win_or_lose == "win":
            gravity = 0
            player.rect.x = width//2
            player.rect.y = height//2
            WIN.draw(window)
            clear_progress()
        if win_or_lose == "lose":
            lose.draw(window)
            clear_progress()
    elif screen == "pause":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                if event.key == pygame.K_ESCAPE:
                    screen = "game"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x, y)
                if pause_settings.rect.collidepoint(x, y):
                    screen = "settings"
                    screen_ = "pause"
                elif newly.rect.collidepoint(x, y):
                    player.has_flag = True
                    clear_progress()
                    player.has_weapon = False
                    player.can_win = False
                    player.rect.x = width // 2 - 25
                    player.rect.y = base_platform.rect.y - 50
                elif pause_exit_button.rect.collidepoint(x,y):
                    screen = "menu"
        mouse_pos = pygame.mouse.get_pos()
        if newly.rect.collidepoint(mouse_pos):
            dark_newly.draw(window)
        else:
            newly.draw(window)
        if pause_settings.rect.collidepoint(mouse_pos):
            dark_pause_settings.draw(window)
        else:
            pause_settings.draw(window)
        if pause_exit_button.rect.collidepoint(mouse_pos):
            darken_pause_exit_button.draw(window)
        else:
            pause_exit_button.draw(window)
            
    elif screen == "game":
        window.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                if event.key == pygame.K_q:
                    gravity = 0
                if event.key == pygame.K_e:
                    gravity = 1
                if event.key == pygame.K_ESCAPE:
                    screen = "pause"
        background.draw(window)
        #платформи та гравець
        if player.rect.y < camera_limit:
            camera_y = player.rect.y - camera_limit
        elif player.rect.y + player.rect.height > height - down_limit:
            camera_y = player.rect.y + player.rect.height - (height - down_limit)
        else:
            camera_y = 0
        
        player.rect.y -= camera_y
        for platform in platforms:
            platform.rect.y -= camera_y
        for platform in platforms:
            platform.draw()
        
            
        if player.rect.colliderect(platform1) and player.can_win:
            screen = "win or lose"
            win_or_lose = "win"
        if player.rect.colliderect(base_platform) and player.can_win:
            screen = "win or lose"
            win_or_lose = "lose"
        for platform in platforms:
            if player.rect.colliderect(platform.rect):
                player.y_velocity = 0
                player.rect.y = platform.rect.y - player.rect.height

        for platform in platforms:
            platform.move()
        player.draw()
        player.update()
        texture_of_roof.draw(window)
        texture_of_roof.rect.y -= camera_y
        pygame.display.update()
        
    pygame.display.flip()
    clock.tick(60)
pygame.quit()