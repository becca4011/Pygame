import pygame #pygame 라이브러리
import sys #system 라이브러리
from time import sleep #시간

#게임 화면
pad_width = 480
pad_height = 640

#배경 그림 넣기
def draw_object(obj, x, y):
    global game_pad
    game_pad.blit(obj, (int(x), int(y))) #object를 x, y좌표 위치로부터 그리는 것

#게임 초기화
def init_game():
    global game_pad, clock, background, fighter
    pygame.init()
    game_pad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('image/background.png')
    fighter = pygame.image.load('image/fighter.png')
    clock = pygame.time.Clock()

#게임 실행
def run_game():
    global game_pad, clock, background, fighter

    #전투기 크기
    fighter_size = fighter.get_rect().size
    fighter_width = fighter_size[0]
    fighter_height = fighter_size[1]

    #전투기 처음 위치
    x = pad_width * 0.45
    y = pad_height * 0.9
    fighter_x = 0 #전투기 위치

    on_game = False
    
    while not on_game:
        for event in pygame.event.get():
            #게임 종료
            if event.type in [pygame.QUIT]:
                pygame.quit() #pygame 종료
                sys.exit() #system 종료

            #전투기 움직이기(키보드)
            if event.type in [pygame.KEYDOWN]: #키보드를 눌렀을 때
                if event.key == pygame.K_LEFT: #방향키 왼쪽(←)을 눌렀을 때
                    fighter_x -= 5 #왼쪽으로 이동
                    
                elif event.key == pygame.K_RIGHT: #방향키 오른쪽(→)을 눌렀을 때
                    fighter_x += 5 #오른쪽으로 이동

            if event.type in [pygame.KEYUP]: #키보드를 누르지 않을 때
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighter_x = 0

        draw_object(background, 0, 0)

        x += fighter_x #키보드를 눌러서 변경된 위치를 x 좌표 위치로 나타냄

        #게임 화면 왼쪽 끝까지 간 경우
        if x < 0:
            x = 0;
        #게임 화면 오른쪽 끝까지 간 경우
        elif x > pad_width - fighter_width:
            x = pad_width - fighter_width

        draw_object(fighter, x, y)

        pygame.display.update()

        clock.tick(60) #초당 프레임 수 설정

    pygame.quit()

#함수 실행
init_game()
run_game()
