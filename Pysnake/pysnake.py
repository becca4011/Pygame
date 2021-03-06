import pygame
import sys
from time import sleep
import random

from pygame.locals import *
pygame.init() #초기화

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32) #화면 크기
pygame.display.set_caption('Snake Game')

GRID_SIZE = 20 #뱀을 표현할 때 1px은 작기 때문에 지정
GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT / GRID_SIZE

WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
ORANGE = (250, 150, 0)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FPS = 10

eat_sound = pygame.mixer.Sound('sound/341695__projectsu012__coins-1.wav')
gameover_sound = pygame.mixer.Sound('sound/Funeral March.wav')

#뱀
class Snake(object):
    def __init__(self):
        self.create()
        self.color = GREEN

    #뱀 생성
    def create(self):
        self.length = 2 #뱀 처음 길이
        self.positions = [((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))] #뱀 처음 위치(중앙)
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT]) #랜덤한 방향으로 뱀 생성

    #조종
    def control(self, xy):
        if(xy[0] * -1, xy[1] * -1) == self.direction: #왼쪽으로 움직이고 있는데 오른쪽 방향키를 눌렀을 때
            return #가지 않도록 함
        else:
            self.direction = xy

    #움직임
    def move(self):
        cur = self.positions[0] #뱀의 머리
        x, y = self.direction #x, y 좌표를 direction에서 가져옴
        new = (((cur[0] + (x * GRID_SIZE)) % WINDOW_WIDTH), (cur[1] + (y * GRID_SIZE)) % WINDOW_HEIGHT) #뱀의 몸통

        #뱀이 자신의 몸통과 부딪히는 경우
        if new in self.positions[2:]:
            game_over()
            self.create() #게임 다시 시작
        elif cur[0] == 2 * GRID_SIZE or cur[0] == 37 * GRID_SIZE  or cur[1] == 2 * GRID_SIZE  or cur[1] == 27 * GRID_SIZE :
            game_over()
            self.create()
        else:
            self.positions.insert(0, new) #새로 생긴 몸통을 추가

            if len(self.positions) > self.length:
                self.positions.pop() #뱀이 연달아 움직임

    #뱀이 먹이를 먹은 경우
    def eat(self):
        self.length += 1

    #실제 화면에 표현
    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)

#먹이
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.create()

    def create(self):
        #self.position = (random.randint(0, (GRID_WIDTH - 1)) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        self.position = (random.randint(3, 35) * GRID_SIZE, random.randint(3, 25) * GRID_SIZE) #먹이 위치(랜덤)

    def draw(self, surface):
        draw_object(surface, self.color, self.position)

#뱀, 먹이를 그릴 때 사용
def draw_object(surface, color, pos):
    r = pygame.Rect((int(pos[0]), int(pos[1])), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, color, r)

#먹이를 먹었는지 여부
def check_eat(snake, feed):
    if snake.positions[0] == feed.position: #뱀의 머리가 먹이의 위치와 같은 경우
        eat_sound.play()
        snake.eat()
        feed.create() #먹이 다시 생성

#뱀의 길이와 스피드 정보
def show_info(length, speed, surface):
    font = pygame.font.Font('NanumGothic.ttf', 25)
    text = font.render("Length : " + str(length) + "    Speed : " + str(round(speed, 2)), True, GRAY) #round : 반올림

    pos = text.get_rect()
    pos.center = (400, 25)
    
    surface.blit(text, pos)

#화면에 메세지 출력
def write_message(text):
    global window
    textfont = pygame.font.Font('NanumGothic.ttf', 60)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect() #메세지의 위치
    textpos.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2)) #메세지를 가운데에 출력
    window.blit(text, textpos) #화면에 보이게 함
    pygame.display.update()

def music():
    pygame.mixer.music.stop() #배경음악 정지
    gameover_sound.play()
    sleep(7)

#게임 메인화면
def main_page():
    global window
    window.blit(pygame.image.load('image/snake.png'), (0, 0))
    pygame.display.update()

    #space를 누르면 게임 시작
    while True:
        for event in pygame.event.get():
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_SPACE:
                    window.blit(pygame.image.load('image/3.png'), (0, 0))
                    pygame.display.update()
                    sleep(1)

                    window.blit(pygame.image.load('image/2.png'), (0, 0))
                    pygame.display.update()
                    sleep(1)

                    window.blit(pygame.image.load('image/1.png'), (0, 0))
                    pygame.display.update()
                    sleep(1)
                    
                    game() #게임 시작

#게임 오버 메세지 출력
def game_over():
    global window
    window.fill(BLACK)
    window.blit(window, (0, 0))
    write_message('Game Over!')
    music()
    main_page()

#초기화
def game():
    if __name__ == '__main__':
        snake = Snake()
        feed = Feed()
    
        surface = pygame.Surface(window.get_size()) #window의 크기를 넣어줌
        surface = surface.convert()
        surface.fill(WHITE)

        clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 40)

        window.blit(surface, (0, 0))

        pygame.mixer.music.load('sound/8bit attempt.mp3') #배경음악
        pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                #게임 종료
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        snake.control(UP)
                    elif event.key == K_DOWN:
                        snake.control(DOWN)
                    elif event.key == K_LEFT:
                        snake.control(LEFT)
                    elif event.key == K_RIGHT:
                        snake.control(RIGHT)

            surface.fill(WHITE)
            pygame.draw.rect(surface, BLACK, [50, 50, 700, 500], 5)
            snake.move()
            check_eat(snake, feed)
            speed = (FPS + snake.length) / 2 #뱀의 길이가 길어질수록 빨라짐
            show_info(snake.length, speed, surface) #정보
            snake.draw(surface)
            feed.draw(surface)
            window.blit(surface, (0, 0))
            pygame.display.flip()
            pygame.display.update()
            clock.tick(speed)

main_page()

        
