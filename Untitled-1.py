from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.SysFont('Modern', 70,)
win = font1.render('Ти виграв!!', True, (0, 255, 0))
lose = font1.render('Ти програв!!', True, (180, 0, 0))
font2 = font.SysFont('Modern', 32)

 
# нам потрібні такі картинки:
img_car1 = "car1.png"  # фон гри
img_car2 = "car2.png"  # герой
img_back = "back.png"

score = 0  # збито кораблів
life = 1
goal = 50

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._option_surfaces.append(font1.render(option, True, (255,255,255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))


    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                draw.rect(surd, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)



class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Клас гравця - автомобіль
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed


# Клас перешкоди
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global score
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            score = score + 1


menu = Menu()
menu.append_option('Hello', lambda: print('hello'))
menu.append_option('Quit', quit)

    
FPS =  60
clock = time.Clock()
win_width = 900
win_height = 700
display.set_caption("Epic Racing")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


car1 = Player(img_car1, 350, win_height - 130, 80, 120, 10)

cars = sprite.Group()
for i in range(1, 6):
    car2= Enemy(img_car2, randint(
        80, win_width - 80), -40, 80, 120, randint(1, 5))
    cars.add(car2)


# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна

bx = 0
while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False

    menu.draw(window 100, 100, 75)


    display.flip()
    # сама гра: дії спрайтів, перевірка правил гри, перемальовка
    if not finish:
        # оновлюємо фон
        window.blit(background, (0, bx))
        window.blit(background, (0, bx + 700))
        

        # рухи спрайтів
        car1.update()
        cars.update()
        
 
        #оновлюємо їх у новому місці при кожній ітерації циклу
        car1.reset()
        cars.draw(window) 

        bx -= 1 
        if bx == -700:
            bx = 0

        if sprite.spritecollide(car1, cars, False):
            sprite.spritecollide(car1, cars, True)
            life = life -1

        
        #програш
        if life == 0:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))


        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))


        if life == 1:
            life_color=(150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650,10))
        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        life = 1
        for m in cars:
            m.kill()
     
        time.delay(3000)
        for i in range(1, 6):
            car2 = Enemy(img_car2, randint(80, win_width - 80), -40, 80, 120, randint(1, 5))
            cars.add(car2)

    # цикл спрацьовує кожні 0.05 секунд

    time.delay(35)