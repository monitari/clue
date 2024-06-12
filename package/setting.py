import pygame as pg

# 색상 설정
BLACK = (0, 0, 0, 255) # 검은색
WHITE = (255, 255, 255, 255) # 흰색
BLUE = (0, 0, 220, 255) # 파란색
PURPLE = (128, 0, 128, 255) # 보라색
RED = (220, 0, 0, 255) # 빨간색
YELLOW = (220, 220, 0, 255) # 노란색
GREEN = (0, 128, 0, 255) # 초록색
GRAY = (220, 220, 220, 255) # 회색
LIGHT_GRAY = (240, 240, 240, 255) # 밝은 회색
DARK_GRAY = (100, 100, 100, 255) # 짙은 회색

# 게임 설정
PLAYER = 4 # 플레이어 수 설정
FPS = 300   # FPS 오를수록 빨라짐
clock = pg.time.Clock()
square_size = 32  # 기본 사각형 크기 설정
window_size = (square_size * 40, square_size * 24) # 창 크기 설정
window = pg.display.set_mode(window_size, pg.RESIZABLE)
bg_color = WHITE # 배경색 설정
wall_color = BLACK # 벽의 색상 설정
wall_pos = pg.Rect(window_size[0] / 2 - square_size * 19, window_size [1] / 2 - square_size * 10, 20 * square_size, 20 * square_size) # 벽의 위치 설정
grid_color = GRAY  # 그리드 색상
thickness = square_size // 10 # 선 두께 설정

# 이미지 및 소리 불러오기
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
final_reasoning_sound.set_volume(0.5) # 최종 추리하는 소리 볼륨 설정
win_sound = pg.mixer.Sound("sounds/win.mp3") # 승리하는 소리 불러오기
win_sound.set_volume(0.6) # 승리하는 소리 볼륨 설정
lose_sound = pg.mixer.Sound("sounds/lose.mp3") # 패배하는 소리 불러오기
lose_sound.set_volume(0.6) # 패배하는 소리 볼륨 설정

# 카드 설정
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
# bonus_cards = { # 보너스카드
#         "차례를 한 번 더 진행합니다." : "지금 사용하거나 필요할 때 사용합니다.",
#         "원하는 장소로 이동합니다." : "지금 사용합니다.",
#         "카드 엿보기" : "누군가 다른 사람에게 추리 카드를 보여줄 때 그 카드를 볼 수 있습니다. 필요할 때 사용합니다.",
#         "나온 주사위에 6을 더할 수 있습니다." : "지금 사용하거나 필요할 때 사용합니다.",
#         "다른 사람의 카드 한 장을 공개합니다." : "한 사람을 정해 이 카드를 보여주면, 그 사람은 자기 카드 중 한 장을 모두에게 보여주어야 합니다. 지금 사용합니다.",
#         "한 번 더 추리합니다." : "자기 말이나 다른 사람의 말 또는 토큰을 이용하지 않고 원하는 장소, 사람, 도구를 정해 추리할 수 있습니다. 지금 사용합니다."
# }
# bonus_cards_list = [card for card in bonus_cards for _ in range(2)] # 각 카드를 원하는 수만큼 복제합니다.
# bonus_cards_list.extend(["원하는 장소로 이동합니다."]) # 보너스카드 목록에 추가

# 방 설정
room_names = list(locs.keys()).copy() # 방 이름
room_names.insert(1, "") # 이름 빈 방
room_names.insert(8, "") # 이름 빈 방
room_names.insert(9, "") # 이름 빈 방
room_names.insert(12, "시작점") # 시작점 방

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
#grid_bonus_pos = ((8, 5), (10, 6), (9, 13), (12, 12), (11, 15)) # 보너스카드 위치 설정
#grid_bonus = [(wall_pos[0] + x * square_size, wall_pos[1] + y * square_size) for x, y in grid_bonus_pos] #`grid_bonus_pos` 위치에 보너스카드 추가

# 카드 설정
card_pos = wall_pos[0] + wall_pos[2] + 1 * square_size, wall_pos[1] # 카드 위치 설정
card_width = square_size * 2 # 카드 너비
card_height = square_size # 카드 높이
card_font = pg.font.SysFont('malgungothic', square_size) # 카드 폰트

# 기타 설정
border_color = wall_color # 테두리 색상
border_thickness = thickness # 테두리 두께
player_size = square_size / 3 # 플레이어 크기
gmrule_btn_pos = wall_pos[0] + 31 * square_size, wall_pos[1] + 17 * square_size, 2 * square_size, 2 * square_size # 게임 규칙 버튼 위치 설정
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