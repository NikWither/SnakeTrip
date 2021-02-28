import random
import time

import pygame
import pygame_menu
from pygame.locals import *

SIZE = 40
display = 600, 800
bg_image = pygame.image.load('data/mnbg.png')
pygame.init()

# -----------------------------------------------------------------------------------------------------

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('data/apple.jpg')
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 19) * SIZE
        self.y = random.randint(1, 14) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load('data/block.jpg').convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # Тело
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Голова
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('SnakeTrip')

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((800, 600))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load('data/bg_music_1.mp3')
        pygame.mixer.music.play(-1)

    def play_sound(self, sound_name):
        if sound_name == 'crash':
            sound = pygame.mixer.Sound('data/crash.mp3')
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound('data/ding.mp3')

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 + SIZE - 5:
            if y1 >= y2 and y1 <= y2 + SIZE - 5:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load('data/background.jpg')
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Поедание змеи яблоко
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound('ding')
                self.snake.increase_length()
                self.apple.move()


            # Столкновение змеи об себя
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise 'Столкновение'

            # Столкновение змеи с окном
        if not (0 <= self.snake.x[0] <= 800 and 0 <= self.snake.y[0] <= 600):
            self.play_sound('crash')
            raise 'Удар об границу'

    def display_score(self):
        font = pygame.font.SysFont('arial', 42)
        score = font.render(f'Очки: {self.snake.length}', True, (200, 200, 200))
        self.surface.blit(score, (650, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'Вы проиграли! Ваш результат: {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render('Играть снова - Enter. Выйти из игры - Escape!', True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        pygame.mixer.music.play(0)
                        pygame.mixer.music.load('data/bg_music_2.mp3')


                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                            # ------------------------------------------------------------------------------------------------

                        if event.key == K_a:
                            self.snake.move_left()

                        if event.key == K_d:
                            self.snake.move_right()

                        if event.key == K_w:
                            self.snake.move_up()

                        if event.key == K_s:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)

surface = pygame.display.set_mode((800, 600))

def start_the_game():
    if __name__ == '__main__':
        game = Game()
        game.run()


menu = pygame_menu.Menu(500, 600, 'SnakeTrip',
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Имя :', default='')
menu.add_button('Играть', start_the_game)
menu.add_button('Выйти', pygame_menu.events.EXIT)

while True:

    surface.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(surface)

        pygame.display.update()

menu.mainloop(surface)