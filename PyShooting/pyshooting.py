import pygame #pygame 라이브러리
import sys #system 라이브러리
import random
from time import sleep #시간

#게임 화면
pad_width = 480
pad_height = 640
rock_image = ['image/rock01.png', 'image/rock02.png', 'image/rock03.png', 'image/rock04.png', 'image/rock05.png', \
              'image/rock06.png', 'image/rock07.png', 'image/rock08.png', 'image/rock09.png', 'image/rock10.png', \
              'image/rock11.png', 'image/rock12.png', 'image/rock13.png', 'image/rock14.png', 'image/rock15.png', \
              'image/rock01.png', 'image/rock01.png', 'image/rock01.png', 'image/rock01.png', 'image/rock20.png', \
              'image/rock21.png', 'image/rock22.png', 'image/rock23.png', 'image/rock24.png', 'image/rock25.png', \
              'image/rock26.png', 'image/rock27.png', 'image/rock28.png', 'image/rock29.png', 'image/rock30.png']

#배경 그림 넣기
def draw_object(obj, x, y):
    global game_pad
    game_pad.blit(obj, (int(x), int(y))) #object를 x, y좌표 위치로부터 그리는 것

#게임 초기화
def init_game():
    global game_pad, clock, background, fighter, missile, explosion
    pygame.init()
    game_pad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('image/background.png') #그림 가져오기
    fighter = pygame.image.load('image/fighter.png')
    missile = pygame.image.load('image/missile.png')
    explosion = pygame.image.load('image/explosion.png')
    clock = pygame.time.Clock()

#게임 실행
def run_game():
    global game_pad, clock, background, fighter, missile, explosion

    #전투기 크기
    fighter_size = fighter.get_rect().size
    fighter_width = fighter_size[0]
    fighter_height = fighter_size[1]

    #전투기 처음 위치
    x = pad_width * 0.45
    y = pad_height * 0.9
    fighter_x = 0 #전투기 위치

    missile_xy = []

    #운석 생성(랜덤)
    rock = pygame.image.load(random.choice(rock_image))
    rock_size = rock.get_rect().size #이미지의 크기를 가져옴
    rock_width = rock_size[0]
    rock_height = rock_size[1]

    #운석 처음 위치(랜덤)
    rock_x = random.randrange(0, pad_width - rock_width)
    rock_y = 0
    rock_speed = 2

    is_shot = False #미사일이 운석에 맞았을 경우 True
    shot_count = 0; #맞춘 운석의 수
    rock_passed = 0; #놓친 운석의 수

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

                elif event.key == pygame.K_SPACE: #스페이스바를 눌렀을 때
                    missile_x = x + fighter_width / 2 #미사일을 전투기의 중간에서 나가게 함
                    missile_y = y - fighter_height #미사일을 전투기의 앞부분에서 나가게 함
                    missile_xy.append([missile_x, missile_y]) #missile_xy 리스트에 저장

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

        #미사일 발사를 화면에 나타내기
        if len(missile_xy) != 0:
            for i, bxy in enumerate(missile_xy): #missile_xy 리스트의 요소를 하나씩 열거
                bxy[1] -= 10 #미사일이 위로 이동(-10씩)
                missile_xy[i][1] = bxy[1] #-10만큼 이동한 값으로 바꿔줌

                #미사일이 운석을 맞추었을 때
                if bxy[1] < rock_y:
                    if bxy[0] > rock_x and bxy[0] < rock_x + rock_width: #미사일과 운석 위치가 겹칠 때
                        missile_xy.remove(bxy) #운석을 맞춘 미사일 제거
                        is_shot = True #미사일이 운석을 맞추어 True
                        shot_count += 1 #운석을 맞추어 1 더함

                #미사일이 화면을 넘어갔을 때
                if bxy[1] <= 0:
                    try:
                        missile_xy.remove(bxy) #넘어간 미사일을 리스트에서 제거
                    except: #에러가 발생할 경우
                        pass

        if len(missile_xy) != 0:
            for bx, by in missile_xy:
                draw_object(missile, bx, by) #미사일을 다시 그려줌

        rock_y += rock_speed #운석이 아래로 내려옴

        #운석이 화면 밖으로 넘어간 경우
        if rock_y > pad_height:
            #새로운 운석 생성(랜덤)
            rock = pygame.image.load(random.choice(rock_image))
            rock_size = rock.get_rect().size
            rock_width = rock_size[0]
            rock_height = rock_size[1]

            rock_x = random.randrange(0, pad_width - rock_width)
            rock_y = 0

        #운석을 맞춘 경우
        if is_shot:
            draw_object(explosion, rock_x, rock_y) #운석 폭발 그림

            rock = pygame.image.load(random.choice(rock_image))
            rock_size = rock.get_rect().size
            rock_width = rock_size[0]
            rock_height = rock_size[1]

            rock_x = random.randrange(0, pad_width - rock_width)
            rock_y = 0

            is_shot = False

        draw_object(rock, rock_x, rock_y)

        pygame.display.update() #화면 업데이트

        clock.tick(60) #초당 프레임 수 설정

    pygame.quit()

#함수 실행
init_game()
run_game()
