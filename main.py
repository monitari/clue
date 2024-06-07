import pygame as pg # 파이게임 라이브러리 불러오기
import random # 랜덤 라이브러리 불러오기
import tkinter as tk # 티컨 라이브러리 불러오기
from tkinter import ttk # 테마 불러오기
from tkinter import messagebox as msg # 메시지 박스 불러오기
import ctypes # 윈도우 API 사용
import time # 시간 라이브러리 불러오기
import win32gui # 윈도우 API 사용
import threading # 스레드 라이브러리 불러오기
import os # 운영체제 라이브러리 불러오기
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit # PyQt5 라이브러리 불러오기
from PyQt5.QtGui import QFont # 폰트 불러오기
import sys # 시스템 라이브러리 불러오기

pg.init() # pygame 초기화
os.system('cls') # 콘솔 화면 지우기

BLACK = (0, 0, 0, 255) # 검은색
WHITE = (255, 255, 255, 255) # 흰색
BLUE = (0, 0, 255, 255) # 파란색
PURPLE = (128, 0, 128, 255) # 보라색
RED = (255, 0, 0, 255) # 빨간색
YELLOW = (255, 255, 0, 255) # 노란색
GREEN = (0, 128, 0, 255) # 초록색
GRAY = (200, 200, 200, 255) # 회색

square_size = 30  # 기본 사각형 크기 설정
window_size = (square_size * 40, square_size * 24) # 창 크기 설정
bg_color = WHITE # 창 배경색 설정
wall_color = BLACK # 벽의 색상 설정
wall_pos = pg.Rect(window_size[0] / 2 - square_size * 19, window_size [1] / 2 - square_size * 10, 20 * square_size, 20 * square_size) # 벽의 위치 설정

grid_color = GRAY  # 그리드 색상
thickness = square_size // 10 # 선 두께 설정
window = pg.display.set_mode(window_size) # 창 크기 설정
pg.display.set_caption("CLUE - board game") # 창 제목 설정
window.fill(bg_color) # 창 배경색으로 채우기
cluedo_logo = pg.image.load("images/cluedo_logo.png") # 클루 로고 이미지 불러오기
cluedo_logo = pg.transform.scale(cluedo_logo, (square_size * 12, square_size * 4)) # 클루도 로고 이미지 크기 조정
main_theme = pg.mixer.Sound("sounds/ES_Covert Affairs - Christoffer Moe Ditlevsen.mp3") # 메인 테마 소리 불러오기
roll_dice_sound = pg.mixer.Sound("sounds/dice.mp3") # 주사위 굴리는 소리 불러오기
show_game_rule_sound = pg.mixer.Sound("sounds/show_game_rule.mp3") # 게임 규칙 소리 불러오기
move_sound = pg.mixer.Sound("sounds/move.mp3") # 이동하는 소리 불러오기
put_player_sound = pg.mixer.Sound("sounds/put_player.mp3") # 플레이어를 놓는 소리 불러오기
enter_room_sound = pg.mixer.Sound("sounds/enter_room.mp3") # 방에 들어가는 소리 불러오기
exit_room_sound = pg.mixer.Sound("sounds/exit_room.mp3") # 방을 나가는 소리 불러오기
ambient_arcade= pg.mixer.Sound("sounds/ambient_arcade_room.mp3") # 게임룸 배경음 불러오기
ambient_arcade.set_volume(0.02) # 게임룸 배경음 볼륨 설정
ambient_bathroom = pg.mixer.Sound("sounds/ambient_bathroom.mp3") # 욕실 배경음 불러오기
ambient_bathroom.set_volume(0.11) # 욕실 배경음 볼륨 설정
ambient_bedroom = pg.mixer.Sound("sounds/ambient_bedroom.mp3") # 침실 배경음 불러오기
ambient_bedroom.set_volume(0.71) # 침실 배경음 볼륨 설정
ambient_cafeteria = pg.mixer.Sound("sounds/ambient_cafeteria.mp3") # 식당 배경음 불러오기
ambient_cafeteria.set_volume(0.18) # 식당 배경음 볼륨 설정
ambient_garage = pg.mixer.Sound("sounds/ambient_garage.mp3") # 차고 배경음 불러오기
ambient_garage.set_volume(0.1) # 차고 배경음 볼륨 설정
ambient_kitchen = pg.mixer.Sound("sounds/ambient_kitchen_room.mp3") # 부엌 배경음 불러오기
ambient_kitchen.set_volume(0.6) # 부엌 배경음 볼륨 설정
ambient_library = pg.mixer.Sound("sounds/ambient_library_room.mp3") # 서재 배경음 불러오기
ambient_library.set_volume(0.09) # 서재 배경음 볼륨 설정
ambient_livingroom = pg.mixer.Sound("sounds/ambient_living_room.mp3") # 거실 배경음 불러오기
ambient_livingroom.set_volume(0.5) # 거실 배경음 볼륨 설정
ambient_yard = pg.mixer.Sound("sounds/ambient_yard.mp3") # 마당 배경음 불러오기
ambient_yard.set_volume(0.3) # 마당 배경음 볼륨 설정
walking_sound = pg.mixer.Sound("sounds/walking.mp3") # 걷는 소리 불러오기
reasoning_sound = pg.mixer.Sound("sounds/reasoning.mp3") # 추리하는 소리 불러오기
final_reasoning_sound = pg.mixer.Sound("sounds/final_reasoning.mp3") # 최종 추리하는 소리 불러오기
win_sound = pg.mixer.Sound("sounds/win.mp3") # 승리하는 소리 불러오기
lose_sound = pg.mixer.Sound("sounds/lose.mp3") # 패배하는 소리 불러오기
laugh_sound = pg.mixer.Sound("sounds/laugh.mp3") # 웃는 소리 불러오기

suspects = { # 용의자카드
    "피콕": BLUE,
    "플럼": PURPLE,
    "스칼렛": RED,
    "머스타드": YELLOW,
    "그린": GREEN,
    "화이트": WHITE
}
weapons = ["파이프", "밧줄", "단검", "렌치", "권총", "촛대"]  # 도구카드
locs = {"침실" : "bedroom", "욕실" : "bathroom", "서제" : "library", "부엌" : "kitchen",
        "식당" : "cafeteria", "거실" : "livingroom", "마당" : "yard", "차고" : "garage", "게임룸" : "arcade" } # 장소카드
room_names = list(locs.keys()).copy() # 방 이름
room_names.insert(1, "") # 이름 빈 방
room_names.insert(8, "") # 이름 빈 방
room_names.insert(9, "") # 이름 빈 방
room_names.insert(12, "시작점") # 시작점 방
bonus_cards = { # 보너스카드 (더미 데이터)
        "차례를 한 번 더 진행합니다." : "지금 사용하거나 필요할 때 사용합니다.",
        "원하는 장소로 이동합니다." : "지금 사용합니다.",
        "카드 엿보기" : "누군가 다른 사람에게 추리 카드를 보여줄 때 그 카드를 볼 수 있습니다. 필요할 때 사용합니다.",
        "나온 주사위에 6을 더할 수 있습니다." : "지금 사용하거나 필요할 때 사용합니다.",
        "다른 사람의 카드 한 장을 공개합니다." : "한 사람을 정해 이 카드를 보여주면, 그 사람은 자기 카드 중 한 장을 모두에게 보여주어야 합니다. 지금 사용합니다.",
        "한 번 더 추리합니다." : "자기 말이나 다른 사람의 말 또는 토큰을 이용하지 않고 원하는 장소, 사람, 도구를 정해 추리할 수 있습니다. 지금 사용합니다."
}
bonus_cards_list = [card for card in bonus_cards for _ in range(2)] # 각 카드를 원하는 수만큼 복제합니다.
bonus_cards_list.extend(["원하는 장소로 이동합니다."]) # 보너스카드 목록에 추가
room_size = [ # 방의 크기 설정
    (6, 6),  # 침실
    (1, 2),  # 침실(옆에 튀어나온 곳)
    (4, 4),  # 욕실
    (4, 5),  # 서재
    (6, 6),  # 부엌
    (7, 5),  # 식당
    (6, 6),  # 거실
    (4, 3),  # 마당1
    (2, 4),  # 마당2
    (2, 4),  # 마당3
    (5, 6),  # 차고
    (5, 6),  # 게임룸
    (4, 3),  # 시작점
]
room_pos = [ # 방의 위치 설정
    (0, 2),  # 침실
    (6, 6),  # 침실(옆에 튀어나온 곳)
    (6, 0),  # 욕실
    (10, 1),  # 서재
    (14, 2),  # 부엌
    (13, 8),  # 식당
    (14, 13),  # 거실
    (8, 17),  # 마당1
    (6, 16),  # 마당2
    (12, 16),  # 마당3
    (1, 14),  # 차고
    (1, 8),  # 게임룸
    (8, 10),  # 시작점
]
rooms = [(wall_pos[0] + x * square_size, wall_pos[1] + y * square_size, w * square_size, h * square_size) 
         for (x, y), (w, h) in zip(room_pos, room_size)] # 방의 위치와 크기를 결합
room_door_pos = { # 방의 문 위치 설정
    list(locs.keys())[0]: (6,5), # 침실
    list(locs.keys())[1]: (8, 4), # 욕실
    list(locs.keys())[2]: (9, 4), # 서제
    list(locs.keys())[3]: (13, 6), # 부엌
    list(locs.keys())[4]: (12, 10), # 식당
    list(locs.keys())[5]: (13, 14), # 거실
    list(locs.keys())[6]: (9, 16), # 마당
    list(locs.keys())[7]: (6, 15), # 차고
    list(locs.keys())[8]: (6, 11),  # 게임룸
}
room_walls_pos = [ # 방 벽 위치 설정
    ((0, 2), (6, 2)),
    ((6, 0), (6, 3)),
    ((6, 4), (6, 5)),
    ((6, 6), (7, 6)),
    ((7, 6), (7, 8)),
    ((7, 8), (0, 8)), # 방 1번
    ((10, 0), (10, 4)),
    ((10, 4), (9, 4)),
    ((8, 4), (6, 4)), # 방 2번
    ((10, 1), (14, 1)),
    ((14, 1), (14, 6)),
    ((14, 6), (9, 6)),
    ((10, 6), (10, 5)), # 방 3번
    ((9, 6), (9, 8)), # 방 1,2,3 앞 복도
    ((14, 2), (20, 2)),
    ((20, 8), (18, 8)),
    ((16, 8), (13, 8)),
    ((14, 7), (14, 8)), # 방 4번
    ((13, 8), (13, 10)),    
    ((13, 11), (13, 13)),
    ((13, 13), (20, 13)), # 방 5번  
    ((14, 13), (14, 14)),
    ((14, 15), (14, 20)),
    ((14, 19), (20, 19)), # 방 6번
    ((6, 20), (6, 16)),
    ((6, 16), (8, 16)),
    ((8, 16), (8, 17)),
    ((8, 17), (9, 17)),
    ((11, 17), (12, 17)),
    ((12, 17), (12, 16)),
    ((12, 16), (14, 16)), # 방 7번 (바깥) 구현
    ((1, 8), (1, 20)),
    ((1, 14), (6, 14)),
    ((6, 15), (6, 12)), # 방 8번
    ((6, 8), (6, 11)), # 방 9번
    ((8, 10), (10, 10)),
    ((11, 10), (12, 10)),
    ((12, 10), (12, 11)),
    ((12, 12), (12, 13)),
    ((12, 13), (11, 13)),
    ((10, 13), (8, 13)),
    ((8, 13), (8, 12)),
    ((8, 11), (8, 10)), # 시작점 방
]
room_walls = [((x[0][0]*square_size + wall_pos[0], x[0][1]*square_size + wall_pos[1]), # 방 벽 설정
                (x[1][0]*square_size + wall_pos[0], x[1][1]*square_size + wall_pos[1])) for x in room_walls_pos]
room_shortcut_pos = ((0, 2), (14, 2), (5, 19), (14, 18)) # 방의 통로 위치 설정
start_room_door_pos = ((7, 11), (10, 9), (12, 11), (10, 13)) # 시작방의 문 위치 설정
grid_bonus_pos = ((8, 5), (10, 6), (9, 13), (12, 12), (11, 15)) # 보너스카드 위치 설정
grid_bonus = [(wall_pos[0] + x * square_size, wall_pos[1] + y * square_size) for x, y in grid_bonus_pos] #`grid_bonus_pos` 위치에 보너스카드 추가
card_pos = wall_pos[0] + wall_pos[2] + 1 * square_size, wall_pos[1] # 카드 위치 설정
card_width = square_size * 2 # 카드 너비
card_height = square_size # 카드 높이
card_font = pg.font.SysFont('malgungothic', square_size) # 카드 폰트
border_color = wall_color # 테두리 색상
border_thickness = thickness # 테두리 두께
player_size = square_size / 3 # 플레이어 크기
gmrule_btn_pos = wall_pos[0] + 33 * square_size, wall_pos[1] + 17 * square_size, 4 * square_size, 2 * square_size # 게임 규칙 버튼 위치 설정
hasReasoned = { # 추리 여부
    list(suspects.keys())[0]: False, # 피콕
    list(suspects.keys())[1]: False, # 플럼
    list(suspects.keys())[2]: False, # 스칼렛
    list(suspects.keys())[3]: False, # 머스타드
}
isLosed = { # 패배 여부
    list(suspects.keys())[0]: False, # 피콕
    list(suspects.keys())[1]: False, # 플럼
    list(suspects.keys())[2]: False, # 스칼렛
    list(suspects.keys())[3]: False, # 머스타드
}

def shuffle_and_distribute_cards(): # 카드 섞고 나눠주기
    su = list(suspects.keys()) # 용의자 카드
    wp = list(weapons) # 도구 카드
    lo = list(locs.keys()) # 장소 카드
    random.shuffle(su) # 용의자 카드 섞기
    random.shuffle(wp) # 도구 카드 섞기
    random.shuffle(lo) # 장소 카드 섞기
    case_envelope = { # 사건봉투
        'suspect': su.pop(), # 용의자 카드
        'tool': wp.pop(), # 도구 카드
        'place': lo.pop() # 장소 카드
    }
    all_cards = list(su) + list(wp) + list(lo)  # 모든 카드를 합칩니다.
    random.shuffle(all_cards)  # 카드를 섞습니다.
    player_cards = {} # 플레이어 카드를 저장할 딕셔너리 생성
    for i in range(0, 4): # 4명의 플레이어에게 카드 나눠주기
        player_cards[list(suspects.keys())[i]] = all_cards[i * 4:i * 4 + 4] # 플레이어에게 카드 나눠주기
        print(list(suspects.keys())[i], "카드:", player_cards[list(suspects.keys())[i]]) # 플레이어 카드 출력
    last_cards = all_cards[4 * 4:] # 남은 카드
    print("사건봉투:", case_envelope, "남은 카드:", last_cards) # 사건봉투와 남은 카드 출력
    return case_envelope, player_cards, last_cards
case_envelope, player_cards, all_cards = shuffle_and_distribute_cards() # 카드 섞고 나눠주기
def auto_close_msgbox(delay=2): # 메시지 박스 자동 닫기 함수
    time.sleep(delay)
    try: # try문을 사용하여 예외 처리
        win = win32gui.FindWindow(None, "알림") # 창을 찾습니다.
        ctypes.windll.user32.PostMessageA(win, 0x0010, 0, 0) # 창을 닫습니다.
    except Exception as e: print(e) # 예외 처리 
def show_message(title, message): # 메시지 표시 함수
    threading.Thread(target=auto_close_msgbox).start() # 자동 닫기 스레드 시작
    if title == "경고": # 경고
        msg.showwarning(title, message)
        return True
    elif title == "실패": # 실패
        msg.showerror(title, message)
        return True
    elif title == "예/아니오": # 예/아니오
        return msg.askyesno(title, message)
    else: # 알림, 취소
        msg.showinfo(title, message)
        return True
def brighten_color(color, isBrigther): # 색상을 밝게 만드는 함수
    if isBrigther == True: # 밝은 모드인 경우
        brightened_color = [min(int(channel * 255 + 0.6 * 255), 255) for channel in color] # 각 색상 채널의 값을 증가시켜 색상을 밝게 만듭니다.
        return brightened_color # 밝은 색상을 반환합니다.
    else: return color
def draw_card(cards, start_height, cur_player, lastShowing = False, Lose = False): # 카드 그리기
    small_font = pg.font.SysFont('malgungothic', 15)  # 작은 폰트 설정
    text1 = small_font.render("현재 플레이어", True, wall_color) # 현재 플레이어
    text1_rect = text1.get_rect(center=(card_pos[0] + card_width * 8, card_pos[1] +  3 * square_size)) # 현재 플레이어 위치 설정
    text2 = card_font.render(cur_player, True, wall_color) # 플레이어 이름
    text2_rect = text2.get_rect(center=(card_pos[0] + card_width * 8, text1_rect.bottom + text2.get_height() / 2)) # 플레이어 이름 위치 설정
    # 플레이어 순서 출력
    p1 = small_font.render(list(player_cards.keys())[0], True, RED if cur_player == list(player_cards.keys())[0] else wall_color) # 플레이어 피콕
    p2 = small_font.render(list(player_cards.keys())[1], True, RED if cur_player == list(player_cards.keys())[1] else wall_color) # 플레이어 플럼
    p3 = small_font.render(list(player_cards.keys())[2], True, RED if cur_player == list(player_cards.keys())[2] else wall_color) # 플레이어 스칼렛
    p4 = small_font.render(list(player_cards.keys())[3], True, RED if cur_player == list(player_cards.keys())[3] else wall_color) # 플레이어 머스타드
    p1_rect = p1.get_rect(center=(card_pos[0] + card_width * 8, card_pos[1] + -1 * square_size)) # 플레이어 피콕 위치 설정
    p2_rect = p2.get_rect(center=(card_pos[0] + card_width * 8, card_pos[1] + 0 * square_size)) # 플레이어 플럼 위치 설정
    p3_rect = p3.get_rect(center=(card_pos[0] + card_width * 8, card_pos[1] + 1 * square_size)) # 플레이어 스칼렛 위치 설정
    p4_rect = p4.get_rect(center=(card_pos[0] + card_width * 8, card_pos[1] + 2 * square_size)) # 플레이어 머스타드 위치 설정
    
    if lastShowing is False: # 아직 때가 아님
        window.blit(p1, p1_rect) # 플레이어 피콕 출력
        window.blit(p2, p2_rect) # 플레이어 플럼 출력
        window.blit(p3, p3_rect) # 플레이어 스칼렛 출력
        window.blit(p4, p4_rect) # 플레이어 머스타드 출력
        window.blit(text1, text1_rect) # 플레이어 순서 출력
        window.blit(text2, text2_rect) # 플레이어 이름 출력

    for i, card in enumerate(cards): # 각 카드에 대해
        row = i // 4
        col = i % 4 # 행 및 열 설정
        if lastShowing is not True:
            e_card_width, e_card_height = card_width * 2, card_height * 5
            e_card_font = pg.font.SysFont('malgungothic', square_size) # 폰트 설정
            x = card_pos[0] + col * (e_card_width + square_size // 2) # x 좌표 설정
            y = card_pos[1] + row * (e_card_height + square_size // 4) + start_height * (e_card_height + square_size // 4) # 시작 높이에 따라 y 좌표 설정
            if len(card) > 5: card = card[:5] + "..." # 카드 이름이 5글자를 넘어가면 ...으로 표시
            if card in case_envelope.values(): card = "???"
        else: # 승리/패배하고 사건 봉투를 열었을 때, 화면 가운데에 사건 봉투 세장 공개
            e_card_width, e_card_height = card_width * 4, card_height * 10
            e_card_font = pg.font.SysFont('malgungothic', square_size * 2) # 폰트 설정
            x = square_size * 15 / 2 + col * (e_card_width + square_size // 2) # x 좌표 설정
            y = square_size * 6 + row * (e_card_height + square_size // 4) + start_height * (e_card_height + square_size // 4) # 시작 높이에 따라 y 좌표 설정
        pg.draw.rect(window, brighten_color(WHITE, False), (x, y, e_card_width, e_card_height))
        pg.draw.rect(window, wall_color, (x, y, e_card_width, e_card_height), border_thickness) # 카드 테두리 그리기
        text = e_card_font.render(card, True, wall_color) # 카드 이름 설정
        text_rect = text.get_rect(center=(x + e_card_width / 2, y + e_card_height / 2)) # 텍스트 위치 설정
        window.blit(text, text_rect)
    if lastShowing is True:
        message = "승리하셨습니다!" if Lose is False else "패배하셨습니다!" # 승리/패배 메시지
        text_title = e_card_font.render(message, True, wall_color)
        text_title_rect = text_title.get_rect(center=(x - e_card_width / 2, y + e_card_height * 5 / 4))
        window.blit(text_title, text_title_rect)
def add_rooms_to_grid(grid): # 방을 그리드에 추가하는 함수
    for room in rooms: # 각 방에 대해
        room = pg.Rect(*room) # 방의 위치 및 크기를 가져옵니다.
        for x in range(room.left, room.right, square_size): # 방의 좌우 범위에 대해
            for y in range(room.top, room.bottom, square_size): grid.add((x, y)) # 방의 각 좌표를 그리드에 추가
def add_walls_to_grid(grid, grid_color, thickness): # 벽을 그리드에 추가하는 함수
    font = pg.font.Font(None, square_size) # 폰트 객체 생성
    # question_mark = font.render("?", True, RED) # "?" 문자를 Surface 객체로 변환
    for x in range(wall_pos.left, wall_pos.right, square_size): # 벽의 각 좌표에 대해
        for y in range(wall_pos.top, wall_pos.bottom, square_size): # 벽의 각 좌표에 대해
            rect = pg.Rect(x, y, square_size, square_size) # 사각형 생성
            if (x, y) in grid: pg.draw.rect(window, bg_color, rect) # 그리드에 있는 경우 배경색으로 채우기
            else: # 그리드에 없는 경우
                # if (rect[0], rect[1]) in grid_bonus: # 보너스카드 위치에 있는 경우
                #     pg.draw.rect(window, brighten_color(RED, True), rect) # 보너스카드 위치에 연한 빨간색으로 채우기
                #     window.blit(question_mark, (rect[0] + square_size / 4, rect[1] + square_size / 4)) # 보너스카드 위치에 "?" 표시
                pg.draw.rect(window, grid_color, rect, thickness // 2) # 그리드에 없는 경우 그리드 색상으로 선 그리기
def draw_wall(thickness): # 벽 그리기
    pg.draw.rect(window, wall_color, wall_pos, thickness) 
def draw_room_walls(room_walls, thickness): # 방 벽 그리기
    for wall in room_walls: pg.draw.line(window, wall_color, wall[0], wall[1], thickness) # 각 방 벽에 대해 선 그리기
def draw_room_names(font): # 방 이름 그리기
    if len(rooms) >= len(room_names): # 방의 수가 방 이름의 수보다 많거나 같은 경우
        for i, room in enumerate(rooms): # 각 방에 대해
            text = font.render(room_names[i], True, GRAY) # 방 이름 설정
            text_rect = text.get_rect(center=(room[0] + square_size * (6 if len(room_names[i]) == 3 else 4) / 5, room[1] + square_size * 2 / 5))
            window.blit(text, text_rect)
def create_player(player_name, loc): # 플레이어 생성
    x, y = (loc[0] - 6) * square_size + (square_size - player_size) / 2 , (loc[1] - 6) * square_size + (square_size - player_size) / 2 # x 좌표 및 y 좌표 설정
    player = (player_name, pg.Rect(rooms[1][0] + x, rooms[1][1] + y, player_size, player_size))
    return player
def draw_player(player, isBrigther, soundPlay): # 플레이어 그리기
    color = brighten_color(suspects[player[0]], isBrigther) # 플레이어 색상 설정
    pg.draw.rect(window, color, player[1]) 
    pg.display.flip()
    if soundPlay is True: move_sound.play() # 이동하는 소리 재생
    return player
def create_and_draw_players(player_pos, soundPlay): # 플레이어 생성 및 그리기
    players = [create_player(player_name, loc) for player_name, loc in player_pos.items()] # 플레이어 생성
    for player in players: draw_player(player, False, soundPlay) # 플레이어 그리기
def roll_dice(): # 주사위 굴리기
    pg.display.flip() # 창 업데이트
    dice = random.randint(1, 6) # 주사위 굴리기
    return dice
def draw_dice(dice1, dice2): # 주사위 그리기
    dice1_pos = wall_pos[0] + 21 * square_size, wall_pos[1] + 17 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    dice2_pos = wall_pos[0] + 24 * square_size, wall_pos[1] + 17 * square_size, 2 * square_size, 2 * square_size # 주사위 위치 및 크기 설정
    pg.draw.rect(window, bg_color, dice1_pos) # 주사위 1의 배경색 설정
    pg.draw.rect(window, bg_color, dice2_pos) # 주사위 2의 배경색 설정
    pg.draw.rect(window, wall_color, dice1_pos, thickness) # 주사위 1의 외곽선 그리기
    pg.draw.rect(window, wall_color, dice2_pos, thickness) # 주사위 2의 외곽선 그리기
    dice_font = pg.font.SysFont('malgungothic', square_size) # 주사위 폰트 설정
    dice1_text = dice_font.render(str(dice1), True, wall_color) # 주사위 1의 결과
    dice2_text = dice_font.render(str(dice2), True, wall_color) # 주사위 2의 결과
    window.blit(dice1_text, ((dice1_pos[0] + square_size) - square_size / 4, (dice1_pos[1] + square_size / 4))) # 주사위 1의 결과 표시
    window.blit(dice2_text, ((dice2_pos[0] + square_size) - square_size / 4, (dice2_pos[1] + square_size / 4))) # 주사위 2의 결과 표시
def draw_btn(pos, text, font, thickness): # 버튼 그리기
    font = pg.font.SysFont('malgungothic', square_size // 2) # 폰트 설정
    pg.draw.rect(window, wall_color, pos, thickness) # 버튼 외곽선 그리기
    text = font.render(text, True, BLACK)
    text_rect = text.get_rect(center=(pos[0] + square_size * 2, pos[1] + square_size * 1))
    window.blit(text, text_rect)
def show_game_rules(): # 게임 규칙 표시
    show_game_rule_sound.play() # 게임 규칙 소리 재생
    game_rule = open("game_rule.txt", "r", encoding="utf-8")
    app = QApplication(sys.argv) # 어플리케이션 생성

    window = QWidget() # 창 생성
    window.setWindowTitle("게임 규칙") # 창 제목 설정
    window.setFixedSize(900, 500) # 창 크기 설정 

    layout = QVBoxLayout() # 레이아웃 생성
    text = QTextEdit() # 텍스트 생성
    text.setReadOnly(True) # 텍스트 읽기 전용 설정
    text.setPlainText(game_rule.read()) # 텍스트 설정
    font = QFont("맑은 고딕", 12) # 폰트 설정
    text.setFont(font) # 폰트 설정
    layout.addWidget(text) # 레이아웃에 텍스트 추가
    button = QPushButton("닫기") # 버튼 생성
    button.clicked.connect(window.close) # 버튼 클릭 시 창 닫기 
    layout.addWidget(button) # 레이아웃에 버튼 추가

    window.setLayout(layout) # 창에 레이아웃 설정
    window.show() # 창 표시
    app.exec_() # 어플리케이션 실행
def handle_dice_click(x, y, btn_pos): # 클릭한 위치 처리
    if btn_pos[0] <= x <= btn_pos[0] + btn_pos[2] and btn_pos[1] <= y <= btn_pos[1] + btn_pos[3]: # 버튼을 클릭한 경우
        roll_dice_sound.play() # 주사위 굴리는 소리 재생
        return True
def outStartRoom(new_pos, room, isOutStartRoom, cur_player): # 시작점 방을 나가는 경우
    room_x_start, room_y_start, width, height = room  # 방의 위치 및 크기 설정
    room_x_end = room_x_start + width # 방의 끝 위치 설정
    room_y_end = room_y_start + height # 방의 끝 위치 설정
    room_x_start, room_x_end = room_x_start / square_size - 1, room_x_end / square_size - 1 # 방의 시작 및 끝 위치 보정
    room_y_start, room_y_end = room_y_start / square_size - 2, room_y_end / square_size - 2 # 방의 시작 및 끝 위치 보정
    if (room_x_start <= (new_pos[0] + player_size / 20) <= room_x_end and room_y_start < (new_pos[1] + player_size / 20) 
        <= room_y_end and isOutStartRoom[cur_player]) is False: return False # 시작점 방을 나가지 않은 경우
    else: return True # 시작점 방을 나간 경우
def handle_room_entry(new_pos, cur_player, isOutStartRoom, other_players_pos, cur_room_loc): # 방에 들어가는 경우
    for room in rooms: # 각 방에 대해
        x_start, y_start, width, height = room # 방의 위치 및 크기
        x_end = x_start + width # 방의 끝 위치
        y_end = y_start + height # 방의 끝 위치
        x_start, x_end = x_start / square_size - 1, x_end / square_size - 1 # 방의 시작 및 끝 위치 보정
        y_start, y_end = y_start / square_size - 2, y_end / square_size - 2 # 방의 시작 및 끝 위치 보정
        if isOutStartRoom[cur_player] is True : # 시작점 방을 나간 경우
            if x_start <= (new_pos[0] + player_size / 20) <= x_end and y_start < (new_pos[1] + player_size / 20) <= y_end: # 방에 들어온 경우
                print(cur_player, "이/가", cur_room_loc[cur_player], "에서", room_names[rooms.index(room)], "방에 들어옴")
                enter_room_sound.play() # 방에 들어가는 소리 재생
                cur_room_loc[cur_player] = room_names[rooms.index(room)] # 현재 방 위치 설정
                while True: # 다른 플레이어가 있거나 방의 통로 위치인 경우
                    new_pos = (random.randint(int(x_start), int(x_end) - 1), random.randint(int(y_start), int(y_end) - 1))
                    if new_pos not in other_players_pos.values() and new_pos not in room_shortcut_pos: break
                if hasReasoned[cur_player] is True and cur_room_loc[cur_player] == "시작점": # 추리를 했고 시작점 방에 있는 경우
                    show_message("알림", "최종 추리를 실행합니다.")
                    if final_reasoning(cur_player) == False: 
                        isLosed[cur_player] = True
                        cur_room_loc[cur_player] = "바깥"
                        return 0, -1
    return new_pos
def do_dice_roll(previous_dice1, previous_dice2, dice1, dice2, player_pos): # 주사위 굴리기
    if previous_dice1 is None and previous_dice2 is None:  # 이전 주사위 결과가 없는 경우
        dice1 = roll_dice()  # 주사위를 굴립니다.
        dice2 = roll_dice()  # 주사위를 굴립니다.
    else: # 이전 주사위 결과가 있는 경우
        dice1 = previous_dice1  # 이전 주사위 결과를 사용합니다.
        dice2 = previous_dice2  # 이전 주사위 결과를 사용합니다.
        previous_dice1 = None  # 이전 주사위 결과를 초기화합니다.
        previous_dice2 = None  # 이전 주사위 결과를 초기화합니다.
    return player_pos, dice1, dice2, previous_dice1, previous_dice2
def move_player(cur_player, player_pos, dice1, dice2, other_players_poss, isOutStartRoom, cur_room_loc): # 플레이어 이동
    def exit_room(cur_player, new_pos, dice_roll): # 방을 나가는 경우
        print("방을 나감")
        cur_room_loc[cur_player] = "복도" # 현재 방 위치를 복도로 설정
        player_pos = new_pos # 플레이어 위치를 새로운 위치로 설정
        dice_roll -= 1 # 주사위 결과를 1 감소시킵니다.
        draw_player(create_player(cur_player, new_pos), True, True) # 플레이어 그리기
        exit_room_sound.play() # 방을 나가는 소리 재생
        return player_pos, dice_roll # 플레이어 위치 및 주사위 결과 반환
    reason = None # 이동 사유(추리), 이동하지 않고 추리만 했을때 이동하지 않은 경우 때문에 무한 루프에 빠지는 것을 방지하기 위해 추가
    new_poss = [player_pos]  # 이동한 모든 좌표를 저장하는 리스트
    new_pos = player_pos  # 새로운 위치
    old_pos = player_pos # 이전 위치
    dice_roll = dice1 + dice2 # 주사위 결과
    cur_dir = None # 현재 방향
    will_start_pos = 0,0 # 시작하는 위치
    player_room_loc = cur_room_loc[cur_player] # 현재 방 위치
    for room in rooms: # 각 방에 대해
        x_start, y_start, width, height = room # 방의 위치 및 크기
        x_end = x_start + width # 방의 끝 위치
        y_end = y_start + height # 방의 끝 위치
        x_start, x_end = x_start / square_size - 1, x_end / square_size - 1 # 방의 시작 및 끝 위치 보정
        y_start, y_end = y_start / square_size - 2, y_end / square_size - 2 # 방의 시작 및 끝 위치 보정
        if isOutStartRoom[cur_player] is True: # 시작점 방을 나간 경우
            if x_start <= (new_pos[0] + player_size / 20) <= x_end and y_start < (new_pos[1] + player_size / 20) <= y_end: # 방에 들어온 경우
                player_room_loc = room_names[rooms.index(room)] # 현재 방 위치 설정
    room_transitions = { # 방 사이 이동
        "부엌": {"next_room": "식당", "new_pos": (random.randint(13, 19), random.randint(8, 12))},
        "식당": {"next_room": "부엌", "new_pos": (random.randint(14, 19), random.randint(2, 7))},
        "침실": {"next_room": "욕실", "new_pos": (random.randint(6, 9), random.randint(0, 3))},
        "욕실": {"next_room": "침실", "new_pos": (random.randint(0, 5), random.randint(2, 7))}
    }
    print(cur_player, "현재 방 위치 :", player_room_loc, cur_room_loc[cur_player]) # 현재 방 위치 출력
    if new_pos == (0, -1): return player_pos, False # 이동하지 않은 경우
    if cur_room_loc[cur_player] != "복도": # 현재 방이 복도가 아닌 경우
        if isOutStartRoom[cur_player] is True and cur_room_loc[cur_player] == player_room_loc: # 시작점 방을 나갔고 현재 방이 그대로인 경우 (다른 방 이동을 위한)
            cur_room = cur_room_loc[cur_player] # 현재 방 설정
            if cur_room in room_transitions: # 현재 방이 방 사이 이동 목록에 있는 경우
                if show_message("예/아니오", "이 방에서 다른 방으로 이동하시겠습니까?"): # 다른 방으로 이동하는 경우
                    print("다른 방으로 이동할 수 있음")
                    cur_room_loc[cur_player] = room_transitions[cur_room]["next_room"] # 다음 방으로 이동
                    new_pos = room_transitions[cur_room]["new_pos"] # 새로운 위치 설정
                    while new_pos in other_players_poss.values(): # 다른 플레이어가 있는 경우
                        new_pos = room_transitions[cur_room]["new_pos"]
                        if new_pos not in other_players_poss.values(): break # 다른 플레이어가 없는 경우 이동
                    player_pos = new_pos # 플레이어 위치 설정
                    dice_roll = 0 # 주사위 결과 초기화
                    walking_sound.play() # 걷는 소리 재생
                else:  # 다른 방으로 이동하지 않는 경우
                    print("다른 방으로 이동하지 않음")
                    if show_message("예/아니오", "이 방에서 나가시겠습니까?"):
                        new_pos = room_door_pos[cur_room_loc[cur_player]] # 방의 문 위치로 이동
                        if new_pos in other_players_poss.values(): # 다른 플레이어가 있는 경우
                            if cur_room_loc[cur_player] == "마당": # 마당인 경우 (마당은 입구가 2칸 넓이)
                                if (10, 16) in other_players_poss.values() or (9, 16) in other_players_poss.values(): # 다른 플레이어가 있는 경우
                                    print("다른 플레이어가 막고 있음. 이동할 수 없는 위치", new_pos, other_players_poss)
                                    show_message("실패", "다른 플레이어가 가로막고 있습니다. 이동할 수 없는 위치입니다.")
                                    dice_roll = 0 # 주사위 결과 초기화
                                else: player_pos, dice_roll = exit_room(cur_player, new_pos, dice_roll) # 방을 나가는 경우
                            else: # 마당이 아닌 경우
                                print("다른 플레이어가 막고 있음. 이동할 수 없는 위치", new_pos, other_players_poss)
                                show_message("실패", "다른 플레이어가 가로막고 있습니다. 이동할 수 없는 위치입니다.")
                                dice_roll = 0  # 주사위 결과 초기화
                        else: player_pos, dice_roll = exit_room(cur_player, new_pos, dice_roll) # 방을 나가는 경우
                    else : # 취소, 방을 나가지 않는 경우
                        print("방을 나가지 않음")
                        dice_roll = 0 # 주사위 결과 초기화
                        if hasReasoned[cur_player] is True: # 한 방에서 연속으로 추리를 한 경우
                            print("한 방에서 연속으로 추리를 할 수 없음") 
                            show_message("경고", "한 방에서 연속으로 추리를 할 수 없습니다.")
                            return player_pos, False # 플레이어 위치 및 이동 여부 반환
            else: # 나가는 경우
                if show_message("예/아니오", "이 방에서 나가시겠습니까?"): # 방을 나가는 경우
                    new_pos = room_door_pos[cur_room_loc[cur_player]] # 방의 문 위치로 이동
                    if new_pos in other_players_poss.values(): # 다른 플레이어가 있는 경우
                        print("다른 플레이어가 막고 있음. 이동할 수 없는 위치", new_pos, other_players_poss)
                        show_message("실패", "다른 플레이어가 가로막고 있습니다. 이동할 수 없는 위치입니다.")
                        dice_roll = 0 # 주사위 결과 초기화
                    else: player_pos, dice_roll = exit_room(cur_player, new_pos, dice_roll) # 방을 나가는 경우
                else: # 취소, 방을 나가지 않는 경우
                    print("방을 나가지 않음")
                    if hasReasoned[cur_player] is True: # 한 방에서 연속으로 추리를 한 경우
                        print("한 방에서 연속으로 추리를 할 수 없음")
                        show_message("경고", "한 방에서 연속으로 추리를 할 수 없습니다.")
                        return player_pos, False # 플레이어 위치 및 이동 여부 반환
                    dice_roll = 0

    if isOutStartRoom[cur_player] is False and cur_room_loc[cur_player] == "시작점": # 시작점 방에 나간적이 없고 현재 방이 시작점인 경우
        while True:
            event = pg.event.wait() # 이벤트 대기
            if event.type == pg.KEYDOWN: # 키를 누른 경우
                if event.key == pg.K_UP: # 위쪽 방향키를 누른 경우
                    pos = (int(start_room_door_pos[1][0] * square_size + wall_pos[0] + square_size / 2), 
                           int(start_room_door_pos[1][1] * square_size + wall_pos[1] + square_size / 2)) # 위치 설정
                    if (window.get_at(pos) == BLUE or window.get_at(pos) == RED or 
                        window.get_at(pos) == YELLOW or window.get_at(pos) == PURPLE): # 다른 플레이어가 있는 경우
                        print("다른 플레이어가 이미 있음. 이동할 수 없는 위치")
                        show_message("실패", "다른 플레이어가 있습니다. 이동할 수 없는 위치입니다.")
                        continue
                    pg.draw.rect(window, bg_color, ((2 * will_start_pos[0] + square_size - player_size - 5) / 2, 
                        (2 * will_start_pos[1] + square_size - player_size - 5) / 2, player_size + 5, player_size + 5)) # 플레이어 이동 전 위치 배경색으로 채우기
                    will_start_pos = wall_pos[0] + start_room_door_pos[1][0] * square_size, wall_pos[1] + start_room_door_pos[1][1] * square_size # 이동할 위치 설정
                    player_pos = start_room_door_pos[1]
                    draw_player(create_player(cur_player, start_room_door_pos[1]), True, True) # 플레이어 그리기
                elif event.key == pg.K_DOWN: # 아래쪽 방향키를 누른 경우
                    pos = (int(start_room_door_pos[3][0] * square_size + wall_pos[0] + square_size / 2), 
                           int(start_room_door_pos[3][1] * square_size + wall_pos[1] + square_size / 2)) # 위치 설정
                    if (window.get_at(pos) == BLUE or window.get_at(pos) == RED or 
                        window.get_at(pos) == YELLOW or window.get_at(pos) == PURPLE): # 다른 플레이어가 있는 경우 
                        print("다른 플레이어가 이미 있음. 이동할 수 없는 위치")
                        show_message("실패", "다른 플레이어가 있습니다. 이동할 수 없는 위치입니다.")
                        continue
                    pg.draw.rect(window, bg_color, ((2 * will_start_pos[0] + square_size - player_size - 5) / 2, 
                        (2 * will_start_pos[1] + square_size - player_size - 5) / 2, player_size + 5, player_size + 5)) # 플레이어 이동 전 위치 배경색으로 채우기
                    will_start_pos = wall_pos[0] + start_room_door_pos[3][0] * square_size, wall_pos[1] + start_room_door_pos[3][1] * square_size # 이동할 위치 설정
                    player_pos = start_room_door_pos[3]
                    draw_player(create_player(cur_player, start_room_door_pos[3]), True, True) # 플레이어 그리기
                elif event.key == pg.K_LEFT: # 왼쪽 방향키를 누른 경우
                    pos = (int(start_room_door_pos[0][0] * square_size + wall_pos[0] + square_size / 2), 
                           int(start_room_door_pos[0][1] * square_size + wall_pos[1] + square_size / 2)) # 위치 설정
                    if (window.get_at(pos) == BLUE or window.get_at(pos) == RED or 
                        window.get_at(pos) == YELLOW or window.get_at(pos) == PURPLE): # 다른 플레이어가 있는 경우
                        print("다른 플레이어가 이미 있음. 이동할 수 없는 위치")
                        show_message("실패", "다른 플레이어가 있습니다. 이동할 수 없는 위치입니다.")
                        continue
                    pg.draw.rect(window, bg_color, ((2 * will_start_pos[0] + square_size - player_size - 5) / 2, 
                        (2 * will_start_pos[1] + square_size - player_size - 5) / 2, player_size + 5, player_size + 5)) # 플레이어 이동 전 위치 배경색으로 채우기
                    will_start_pos = wall_pos[0] + start_room_door_pos[0][0] * square_size, wall_pos[1] + start_room_door_pos[0][1] * square_size # 이동할 위치 설정
                    player_pos = start_room_door_pos[0]
                    draw_player(create_player(cur_player, start_room_door_pos[0]), True, True) # 플레이어 그리기
                elif event.key == pg.K_RIGHT: # 오른쪽 방향키를 누른 경우
                    pos = (int(start_room_door_pos[2][0] * square_size + wall_pos[0] + square_size / 2), 
                           int(start_room_door_pos[2][1] * square_size + wall_pos[1] + square_size / 2)) # 위치 설정
                    if (window.get_at(pos) == BLUE or window.get_at(pos) == RED or 
                        window.get_at(pos) == YELLOW or window.get_at(pos) == PURPLE): # 다른 플레이어가 있는 경우
                        print("다른 플레이어가 이미 있음. 이동할 수 없는 위치")
                        show_message("실패", "다른 플레이어가 있습니다. 이동할 수 없는 위치입니다.")
                        continue
                    pg.draw.rect(window, bg_color, ((2 * will_start_pos[0] + square_size - player_size - 5) / 2, 
                        (2 * will_start_pos[1] + square_size - player_size - 5) / 2, player_size + 5, player_size + 5)) # 플레이어 이동 전 위치 배경색으로 채우기
                    will_start_pos = wall_pos[0] + start_room_door_pos[2][0] * square_size, wall_pos[1] + start_room_door_pos[2][1] * square_size # 이동할 위치 설정
                    player_pos = start_room_door_pos[2] 
                    draw_player(create_player(cur_player, start_room_door_pos[2]), True, True) # 플레이어 그리기
                elif event.key == pg.K_ESCAPE or event.type == pg.QUIT: exit() # 게임 종료
                elif event.key == pg.K_RETURN: # 엔터 키를 누른 경우
                    if will_start_pos == (0, 0): # 이동할 위치가 없는 경우
                        show_message("경고", "이동할 위치를 선택해주세요.")
                        print("경고, 이동할 위치를 선택")
                        continue # 다시 선택
                    print(cur_player, "이/가 이동을", will_start_pos, "에서 시작함") 
                    put_player_sound.play() # 플레이어 이동 소리 재생
                    isOutStartRoom[cur_player] = True # 시작점 방을 나간 경우
                    cur_room_loc[cur_player] = "복도" # 현재 방 위치를 복도로 설정
                    new_poss.append(player_pos) # 이동한 위치 추가
                    dice_roll -= 1 # 주사위 결과 1 감소
                    break
    print("주사위 결과 :", dice1, "+", dice2, "=", dice1 + dice2)
    print("현재 방 위치 :", cur_room_loc)
    while dice_roll > 0: # 주사위를 모두 사용할 때까지
        event = pg.event.wait()
        if event.type == pg.KEYDOWN: # 키를 누른 경우
            if event.key == pg.K_UP: # 위쪽 방향키를 누른 경우
                new_pos = player_pos[0], player_pos[1] - 1
                cur_dir = "위쪽"
            elif event.key == pg.K_DOWN: # 아래쪽 방향키를 누른 경우
                new_pos = player_pos[0], player_pos[1] + 1
                cur_dir = "아래쪽"
            elif event.key == pg.K_LEFT: # 왼쪽 방향키를 누른 경우
                new_pos = player_pos[0] - 1, player_pos[1]
                cur_dir = "왼쪽"
            elif event.key == pg.K_RIGHT: # 오른쪽 방향키를 누른 경우
                new_pos = player_pos[0] + 1, player_pos[1]
                cur_dir = "오른쪽"
            elif event.key == pg.K_ESCAPE or event.type == pg.QUIT: exit() # 게임 종료
            elif event.key == pg.K_RETURN: # 엔터 키를 누른 경우
                print(cur_player, "는 아직", dice_roll, "칸 이동하지 않았음")
                if dice_roll == dice1 + dice2: # 주사위를 모두 사용하지 않은 경우
                    show_message("경고", "한 칸 이상 이동해야합니다.")
                    print("경고, 한 칸 이상 이동해야함")
                    continue 
                if show_message("예/아니오", "아직 " + str(dice_roll) + "칸 이동하지 않았습니다. 정말 끝내시겠습니까?"): # Yes/No 대화상자를 표시합니다.
                    print(cur_player, "이/가 이동을 끝냄")
                    move_sound.play() # 이동하는 소리 재생
                    return player_pos, None # 플레이어 위치 및 이동 사유 반환
                else: # No를 누른 경우
                    print("취소, 계속 진행함")
                    continue
            else: continue # 다른 키를 누른 경우
            mid_pos = ((player_pos[0] + new_pos[0]) / 2, (player_pos[1] + new_pos[1]) / 2) # 중간 위치
            mid = (int(mid_pos[0]*square_size + wall_pos[0] + square_size / 2), 
                   int(mid_pos[1]*square_size + wall_pos[1] + square_size / 2)) # 중간 위치(벽 판별 위해)
            if window.get_at(mid) == BLACK: # 벽이 있는 경우
                print("이동 불가,", cur_dir, "에 벽이 있음, 위치 :", new_pos)
                show_message("실패", cur_dir + "에 벽이 있어 이동할 수 없습니다. 다시 선택해주세요.")
                player_pos = new_poss[-1] # 마지막으로 성공한 위치로 돌아갑니다.
            else: # 벽이 없는 경우
                enter_room = handle_room_entry(new_pos, cur_player, isOutStartRoom, other_players_poss, cur_room_loc) # 방에 들어가는 경우
                if new_pos in other_players_poss.values(): # 다른 플레이어가 있는 경우 
                    print("이동 불가, 다른 플레이어가 있음, 위치 :", new_pos)
                    show_message("실패", "다른 플레이어가 있어 이동할 수 없습니다. 다시 선택해주세요.")
                    player_pos = new_poss[-1]  # 마지막으로 성공한 위치로 돌아갑니다.
                    continue
                elif (isOutStartRoom[cur_player] is True and cur_room_loc[cur_player] == "시작점" 
                      and enter_room != new_pos and hasReasoned[cur_player] is False): # 시작점 방을 나가고 추리 없이 다시 들어가는 경우
                    print("이동 불가, 추리를 먼저 해야함")
                    show_message("경고", "시작점 방을 나가고 다시 들어가려면 추리를 먼저 해야합니다.")
                    cur_room_loc[cur_player] = "복도"
                    player_pos = new_poss[-1] # 마지막으로 성공한 위치로 돌아갑니다.
                    continue
                elif enter_room != new_pos: # 방에 들어가는 경우
                    new_poss.append(enter_room) # 새로운 위치를 리스트에 추가
                    player_pos = enter_room # 플레이어 위치를 새로운 위치로 설정
                    dice_roll = 0 # 주사위 결과 초기화
                elif new_pos[-1] == player_pos: # 이미 이동한 위치인 경우 1
                    print("이동 불가, 이미 이동한 위치:", new_pos)
                    show_message("실패", "이미 이동한 위치입니다. 다시 선택해주세요.")
                    player_pos = new_pos # 마지막으로 성공한 위치로 돌아갑니다.
                    continue
                elif new_pos in new_poss: # 이미 이동한 위치인 경우 2
                    print("이동 불가, 이미 이동한 위치:", new_pos)
                    show_message("실패", "이미 이동한 위치입니다. 다시 선택해주세요.")
                    player_pos = new_poss[-1]  # 마지막으로 성공한 위치로 돌아갑니다.
                    continue
                else: # 이동 가능한 경우
                    draw_player(create_player(cur_player, new_pos), True, True) # 플레이어 그리기
                    new_poss.append(new_pos)  # 새로운 위치를 리스트에 추가
                    player_pos = new_pos
                    dice_roll -= 1
    if dice_roll == 0: # 주사위를 모두 사용한 경우
        print(cur_player, "위치 이동", old_pos, " -> ", player_pos)
        print("이동 후 방 위치 : ", cur_room_loc)
        if (cur_room_loc[cur_player] != "시작점" and isOutStartRoom[cur_player] is True and 
            cur_room_loc[cur_player] != "복도" and cur_room_loc[cur_player] != "바깥"): # 시작점 방을 나간 경우
            reason = reasoning(cur_player, cur_room_loc) # 추리
            if reason is None: # 추리를 하지 않은 경우
                print("추리를 하지 않음. 다음 차례.")
                show_message("알림", "추리를 하지 않아 다음 차례로 넘어갑니다.")
            elif reason is True:
                print("추리를 함. 다음 차례.")
                show_message("알림", "추리를 하여 다음 차례로 넘어갑니다.")
                hasReasoned[cur_player] = True # 추리를 했음
            return player_pos, reason
    return player_pos, reason
def draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, btn_pos, cur_player): # 모두 그리기
    window.fill(bg_color) # 창 배경색으로 채우기
    window.blit(cluedo_logo, (wall_pos[0] + 21 * square_size, wall_pos[1])) # 로고 그리기
    add_walls_to_grid(grid, grid_color, thickness) # 벽을 그리드에 추가
    draw_wall(thickness) # 벽 그리기
    draw_room_walls(room_walls, thickness) # 방 벽 그리기
    draw_room_names(font) # 방 이름 그리기
    if cur_player is not None: 
        draw_card(list(player_cards[cur_player]), 1, cur_player) # 플레이어 카드 그리기
        #draw_card(bonus_cards_list, 4) # 보너스 카드 그리기
        draw_card(list(case_envelope.values()), 2, cur_player) # 사건봉투 카드 그리기
    create_and_draw_players(player_pos, False) # 플레이어 생성 및 그리기
    draw_dice(dice1, dice2) # 주사위 그리기
    draw_btn(btn_pos, "주사위 굴리기", font, thickness) # 주사위 굴리기 버튼 그리기
    draw_btn((btn_pos[0] + 6 * square_size, btn_pos[1], btn_pos[2], btn_pos[3]), "게임 규칙", font, thickness) # 게임 규칙 버튼 그리기
    pg.display.flip() # 창 업데이트
def reasoning(cur_player, cur_room_loc): # 추리
    def make_guess(): # 추리하기
        reasoning_sound.play() # 추리 소리 재생
        selected_suspect = suspect_var.get() # 선택한 용의자
        selected_weapon = weapon_var.get() # 선택한 무기
        selected_room = cur_room_loc[cur_player] # 선택한 방 (현재 방)
        if not selected_suspect or not selected_weapon: # 선택한 용의자 또는 무기가 없는 경우
            msg.showwarning("경고", "모든 항목을 선택하세요.")
            return
        print(f"추리 : 용의자 - {selected_suspect}, 무기 - {selected_weapon}, 장소 - {selected_room}")
        msg.showinfo("추리", f"용의자 - {selected_suspect}, 무기 - {selected_weapon}, 장소 - {selected_room}")
        for player in player_cards.keys(): # 다른 플레이어가 가지고 있는 카드
            if player != cur_player: # 현재 플레이어가 아닌 경우
                if (selected_suspect in player_cards[player] or  # 선택한 용의자 또는 무기 또는 방이 다른 플레이어가 가지고 있는 경우
                    selected_weapon in player_cards[player] or 
                    selected_room in player_cards[player]):
                    print(player, "가 가지고 있는 카드:", player_cards[player]) # 다른 플레이어가 가지고 있는 카드 출력
                    while True: # 무작위로 카드 선택
                        card = random.choice(player_cards[player]) # 무작위로 카드 선택
                        if card in [selected_suspect, selected_weapon, selected_room]: break # 선택한 카드가 아닌 경우 다시 선택
                    msg.showinfo("카드", f"{player}님이 가지고 있는 카드 중 하나는 {card}입니다.") # 다른 플레이어가 가지고 있는 카드 중 하나를 알림
        root.destroy()
    app_width, app_height = 300, 100
    root = tk.Tk()
    root.title("추리")
    windows_width = root.winfo_screenwidth()
    windows_height = root.winfo_screenheight()
    center_width = (windows_width / 2) - (app_width / 2)
    center_height = (windows_height / 2) - (app_height / 2)
    root.geometry(f"{app_width}x{app_height}+{int(center_width)}+{int(center_height)}")
    
    main_theme.set_volume(0.06) # 메인 테마 볼륨 설정
    eval(f"ambient_{locs[cur_room_loc[cur_player]]}").play(-1) # 현재 방의 배경음악 재생
    tk.Label(root, text="용의자 선택").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(root, text="살인 도구 선택").grid(row=1, column=0, padx=10, pady=5)
    suspects_list = list(suspects.keys()) # 용의자 목록
    weapons_list = list(weapons) # 무기 목록
    suspect_var = tk.StringVar() # 용의자 변수
    weapon_var = tk.StringVar() # 무기 변수
    suspect_menu = ttk.Combobox(root, textvariable=suspect_var, values=suspects_list, state="readonly") # 용의자 메뉴
    suspect_menu.grid(row=0, column=1, padx=10, pady=5) # 용의자 메뉴 그리기
    weapon_menu = ttk.Combobox(root, textvariable=weapon_var, values=weapons_list, state="readonly") # 무기 메뉴
    weapon_menu.grid(row=1, column=1, padx=10, pady=5) # 무기 메뉴 그리기

    tk.Button(root, text="추리하기", command=make_guess).grid(row=2, columnspan=2, pady=10) # 추리하기 버튼
    root.mainloop()
    if suspect_var.get() not in suspects or weapon_var.get() not in weapons: 
        eval(f"ambient_{locs[cur_room_loc[cur_player]]}").fadeout(500) # 현재 방의 배경음악 정지
        return None # 선택한 용의자 또는 무기가 없는 경우
    else:
        eval(f"ambient_{locs[cur_room_loc[cur_player]]}").fadeout(500) # 현재 방의 배경음악 정지
        return True # 추리를 한 경우
def final_reasoning(cur_player): # 최종 추리
    main_theme.set_volume(0) # 메인 테마 볼륨 설정
    final_reasoning_sound.set_volume(0.2) # 최종 추리 소리 볼륨 설정
    final_reasoning_sound.play(-1) # 최종 추리 소리 재생
    def make_guess(): # 추리하기
        selected_suspect = suspect_var.get() # 선택한 용의자
        selected_weapon = weapon_var.get() # 선택한 무기
        selected_room = room_var.get() # 선택한 방
        if not selected_suspect or not selected_weapon or not selected_room: # 선택한 용의자, 무기, 방이 없는 경우
            msg.showwarning("경고", "모든 항목을 선택하세요.")
            return
        print(f"추리: 용의자 - {selected_suspect}, 무기 - {selected_weapon}, 장소 - {selected_room}")
        msg.showinfo("추리", f"용의자 - {selected_suspect}, 무기 - {selected_weapon}, 장소 - {selected_room}")
        root.destroy()
    app_width, app_height = 300, 150
    root = tk.Tk()
    root.title("최종 추리")
    windows_width = root.winfo_screenwidth()
    windows_height = root.winfo_screenheight()
    center_width = (windows_width / 2) - (app_width / 2)
    center_height = (windows_height / 2) - (app_height / 2)
    root.geometry(f"{app_width}x{app_height}+{int(center_width)}+{int(center_height)}")

    tk.Label(root, text="용의자 선택").grid(row=0, column=0, padx=10, pady=5) # 용의자 선택 레이블
    tk.Label(root, text="살인 도구 선택").grid(row=1, column=0, padx=10, pady=5) # 살인 도구 선택 레이블
    tk.Label(root, text="장소 선택").grid(row=2, column=0, padx=10, pady=5) # 장소 선택 레이블
    suspects_list = list(suspects.keys()) # 용의자 목록
    weapons_list = list(weapons) # 무기 목록
    rooms_list = list(locs.keys()) # 방 목록
    suspect_var = tk.StringVar() # 용의자 변수
    weapon_var = tk.StringVar() # 무기 변수
    room_var = tk.StringVar() # 방 변수
    suspect_menu = ttk.Combobox(root, textvariable=suspect_var, values=suspects_list, state="readonly") # 용의자 메뉴
    suspect_menu.grid(row=0, column=1, padx=10, pady=5) # 용의자 메뉴 그리기
    weapon_menu = ttk.Combobox(root, textvariable=weapon_var, values=weapons_list, state="readonly") # 무기 메뉴
    weapon_menu.grid(row=1, column=1, padx=10, pady=5) # 무기 메뉴 그리기
    room_menu = ttk.Combobox(root, textvariable=room_var, values=rooms_list, state="readonly") # 방 메뉴
    room_menu.grid(row=2, column=1, padx=10, pady=5) # 방 메뉴 그리기
    
    tk.Button(root, text="추리하기", command=make_guess).grid(row=3, columnspan=2, pady=10)
    root.mainloop()
    # 추리 결과가 사건 봉투 내용과 일치하는 경우, 최종 추리 성공, 게임 승리, 해당 플레이어는 이제 게임에 참여 불가
    if suspect_var.get() == case_envelope["suspect"] and weapon_var.get() == case_envelope["tool"] and room_var.get() == case_envelope["place"]: 
        final_reasoning_sound.stop() # 최종 추리 소리 정지
        win_sound.set_volume(0.2) # 승리 소리 볼륨 설정
        win_sound.play() # 승리 소리 재생
        print("최종 추리 성공, ", cur_player, "승리")
        show_message("승리", f"{cur_player}님, 최종 추리 성공으로 승리하셨습니다.")
        end_screen(False) # 게임 종료 화면
    else: # 추리 결과가 사건 봉투 내용과 일치하지 않는 경우, 최종 추리 실패, 게임 패배, 해당 플레이어는 이제 게임에 참여 불가
        final_reasoning_sound.stop() # 최종 추리 소리 정지
        lose_sound.play() # 패배 소리 재생
        print("최종 추리 실패,", cur_player, "패배")
        show_message("패배", f"{cur_player}님, 최종 추리 실패로 패배하셨습니다.")
        lose_sound.stop() # 패배 소리 정지
        return False
def end_screen(Losed): # 게임 종료 화면
    cluedo_logo = pg.image.load("images/cluedo_logo.png") # 클루 로고 이미지 로드
    cluedo_logo = pg.transform.scale(cluedo_logo, (12 * square_size, 4 * square_size))
    pg.draw.rect(window, bg_color, (0, 0, window_size[0], window_size[1])) # 창 배경색으로 채우기
    window.blit(cluedo_logo, (wall_pos[0] + 13 * square_size, wall_pos[1] - square_size)) # 로고 그리기
    draw_card(list(case_envelope.values()), 0, None, True, Losed) # 사건 봉투 카드 그리기
    font = pg.font.SysFont('malgungothic', square_size) # 폰트 설정
    end_btn_pos = wall_pos[0] + 27 * square_size, wall_pos[1] + 17 * square_size, 4 * square_size, 2 * square_size # 버튼 위치 설정
    draw_btn(end_btn_pos, "게임 종료", font, thickness)
    pg.display.flip() # 창 업데이트
    event = pg.event.wait() # 이벤트를 기다립니다
    while True: # 무한 루프
        for event in pg.event.get(): # 이벤트를 가져옵니다
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos() # 마우스 위치를 가져옵니다
                if end_btn_pos[0] <= x <= end_btn_pos[0] + end_btn_pos[2] and end_btn_pos[1] <= y <= end_btn_pos[1] + end_btn_pos[3]: 
                    exit() # 게임 종료 버튼을 누른 경우
def main(): # 메인 함수
    pg.init() # pg 초기화
    dice1 = 0  # 주사위 초기값 설정
    dice2 = 0  # 주사위 초기값 설정
    cnt = 0  # 카운트 초기값 설정
    grid = set() # 그리드 설정
    font = pg.font.SysFont('malgungothic', square_size * 2 // 3) # 폰트 설정
    add_rooms_to_grid(grid) # 방을 그리드에 추가
    dice_btn_pos = wall_pos[0] + 27 * square_size, wall_pos[1] + 17 * square_size, 4 * square_size, 2 * square_size # 버튼 위치 설정
    player_pos = { # 각 플레이어의 초기 위치를 설정합니다.
        list(suspects.keys())[0] : (8, 10),
        list(suspects.keys())[1] : (11, 10),
        list(suspects.keys())[2] : (8, 12),
        list(suspects.keys())[3] : (11, 12),
    }
    isOutStartRoom = { # 시작점 방을 나갔는지 여부
        list(suspects.keys())[0]: False,
        list(suspects.keys())[1]: False,
        list(suspects.keys())[2]: False,
        list(suspects.keys())[3]: False,
    }
    cur_room_loc = { # 현재 플레이어의 방 위치
        list(suspects.keys())[0]: room_names[rooms.index(rooms[12])],
        list(suspects.keys())[1]: room_names[rooms.index(rooms[12])],
        list(suspects.keys())[2]: room_names[rooms.index(rooms[12])],
        list(suspects.keys())[3]: room_names[rooms.index(rooms[12])],
    }
    draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, None) # 모든 요소 그리기
    pg.display.flip() # 창 업데이트
    running = True # 게임 실행 여부
    previous_dice1 = None  # 이전 주사위 결과를 저장하는 변수
    previous_dice2 = None  # 이전 주사위 결과를 저장하는 변수
    notMoved = False # 이동하지 않은 경우
                     
    while running: # 게임이 실행 중인 동안
        main_theme.set_volume(0.18) # 메인 테마 볼륨 설정
        if main_theme.get_num_channels() == 0: main_theme.play(-1) # 메인 테마 소리 재생 (재생 중이 아닌 경우)
        for event in pg.event.get(): # 이벤트 리스트 반복
            cur_player = list(player_pos.keys())[cnt % 4] # 현재 플레이어      
            if isLosed[cur_player] is True: # 해당 플레이어가 패배한 경우
                laugh_sound.play() # 웃음소리 재생
                print(cur_player, "이/가 이미 패배함. 다음 차례로 넘어감")
                show_message("패배", f"{cur_player}님, 이미 패배하셨습니다. 다음 차례로 넘어갑니다.")
                cnt += 1
                laugh_sound.stop() # 웃음소리 정지
                continue
            elif all(isLosed[player] for player in player_pos.keys()): # 모든 플레이어가 패배한 경우
                lose_sound.set_volume(0.1) # 패배 소리 볼륨 설정
                lose_sound.play() # 패배 소리 재생
                print("모든 플레이어가 패배함")
                show_message("알림", "모든 플레이어가 패배하여 게임이 종료되었습니다. 사건 봉투를 공개합니다.")
                end_screen(True) # 게임 종료 화면
            if event.type == pg.MOUSEBUTTONDOWN: # 마우스 버튼을 누른 경우
                x, y = event.pos  # 마우스 위치를 가져옵니다
                if (gmrule_btn_pos[0] <= x <= gmrule_btn_pos[0] + gmrule_btn_pos[2] 
                and gmrule_btn_pos[1] <= y <= gmrule_btn_pos[1] + gmrule_btn_pos[3]): # 게임 규칙 버튼을 누른 경우
                    show_game_rules() # 게임 규칙 표시
            if notMoved: # 이동하지 않은 경우
                player_pos, dice1, dice2, previous_dice1, previous_dice2 = do_dice_roll(previous_dice1, previous_dice2, dice1, dice2, player_pos)
                draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, cur_player) # 모든 요소 그리기
                other_players_poss = {player[0]: (player[1][0], player[1][1]) 
                                      for player in player_pos.items() if player[0] != cur_player} # 나머지 플레이어들의 좌표를 가져옵니다
                new_pos, reason = move_player(cur_player, player_pos[cur_player], dice1, dice2, other_players_poss, isOutStartRoom, cur_room_loc)
                if new_pos != player_pos[cur_player] and reason is not None: # 이동한 경우
                    previous_dice1 = None  # 이전 주사위 결과를 초기화합니다.
                    previous_dice2 = None  # 이전 주사위 결과를 초기화합니다.
                    notMoved = False
                else:  # 플레이어가 이동하지 않은 경우
                    previous_dice1 = dice1  # 이전 주사위 결과를 저장합니다.
                    previous_dice2 = dice2  # 이전 주사위 결과를 저장합니다.
                    notMoved = True
                player_pos[cur_player] = new_pos
                draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, cur_player) # 모든 요소 그리기
            else: # 이동한 경우
                if event.type == pg.QUIT: running = False # 종료 버튼을 누른 경우
                if event.type == pg.MOUSEBUTTONDOWN: 
                    x, y = event.pos  # 클릭한 위치를 가져옵니다.
                    if handle_dice_click(x, y, dice_btn_pos) : # 주사위 굴리기 버튼을 누른 경우
                        main_theme.set_volume(0.12) # 메인 테마 볼륨 설정
                        player_pos, dice1, dice2, previous_dice1, previous_dice2 = do_dice_roll(previous_dice1, previous_dice2, dice1, dice2, player_pos)
                        draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, cur_player) # 모든 요소 그리기
                        other_players_poss = {player[0]: (player[1][0], player[1][1]) 
                                              for player in player_pos.items() if player[0] != cur_player} # 나머지 플레이어들의 좌표를 가져옵니다.    
                        new_pos, reason = move_player(cur_player, player_pos[cur_player], dice1, dice2, other_players_poss, isOutStartRoom, cur_room_loc)
                        if new_pos == player_pos[cur_player] and reason is None: # 이동하지 않은 경우
                            previous_dice1 = dice1 # 이전 주사위 결과를 저장합니다.
                            previous_dice2 = dice2 # 이전 주사위 결과를 저장합니다.
                            notMoved = True       
                        else: # 이동한 경우
                            previous_dice1 = None # 이전 주사위 결과를 초기화합니다.
                            previous_dice2 = None # 이전 주사위 결과를 초기화합니다.     
                            cnt += 1 # 카운트 증가 
                            notMoved = False      
                        player_pos[cur_player] = new_pos  # 플레이어 위치를 새로운 위치로 설정합니다.
                        draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, dice_btn_pos, cur_player) # 모든 요소 그리기
    pg.quit() # pg 종료 

if __name__ == "__main__":
    main() # 메인 함수 실행