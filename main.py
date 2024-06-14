import pygame as pg # 파이게임 라이브러리 불러오기
import os # 운영체제 라이브러리 불러오기
import time

pg.init() # pygame 초기화
from package.setting import * # setting.py 파일에서 모든 변수 및 함수 불러오기
from package.functions import * # functions.py 파일에서 모든 함수 불러오기
os.system('cls') # 콘솔 화면 지우기

def main(): # 메인 함수
    pg.init() # pg 초기화
    pg.display.set_caption("CLUE - board game") # 창 제목 설정
    window.fill(bg_color) # 창 배경색으로 채우기
    
    dice1 = 0  # 주사위 초기값 설정
    dice2 = 0  # 주사위 초기값 설정
    cnt = 0  # 카운트 초기값 설정
    grid = set() # 그리드 설정
    font = pg.font.SysFont('malgungothic', square_size * 2 // 3) # 폰트 설정
    case_envelope, player_cards, last_cards = shuffle_and_distribute_cards() # 사건 봉투, 플레이어 카드, 마지막 카드를 섞고 분배합니다.
    add_rooms_to_grid(grid) # 방을 그리드에 추가
    dice_btn_pos = wall_pos[0] + 26 * square_size, wall_pos[1] + 17 * square_size, 4 * square_size, 2 * square_size # 버튼 위치 설정

    player_pos = { # 각 플레이어의 초기 위치를 설정합니다.
        list(suspects.keys())[0] : (8, 10), list(suspects.keys())[1] : (11, 10),
        list(suspects.keys())[2] : (8, 12), list(suspects.keys())[3] : (11, 12) }
    isOutStartRoom = { # 시작점 방을 나갔는지 여부
        list(suspects.keys())[0]: False, list(suspects.keys())[1]: False,
        list(suspects.keys())[2]: False, list(suspects.keys())[3]: False }
    cur_room_loc = { # 현재 플레이어의 방 위치
        list(suspects.keys())[0]: room_names[rooms.index(rooms[12])], list(suspects.keys())[1]: room_names[rooms.index(rooms[12])],
        list(suspects.keys())[2]: room_names[rooms.index(rooms[12])], list(suspects.keys())[3]: room_names[rooms.index(rooms[12])] }
    
    draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, 
             dice_btn_pos, None, case_envelope, player_cards) # 모든 요소 그리기
    pg.display.flip() # 창 업데이트
    
    running = True # 게임 실행 여부
    previous_dice1 = None  # 이전 주사위 결과를 저장하는 변수
    previous_dice2 = None  # 이전 주사위 결과를 저장하는 변수
    notMoved = False # 이동하지 않은 경우
                     
    while running: # 게임이 실행 중인 동안
        global isLosed # 패배 여부
        main_theme.set_volume(0.25) # 메인 테마 볼륨 설정
        if main_theme.get_num_channels() == 0: main_theme.play(-1) # 메인 테마 소리 재생 (재생 중이 아닌 경우)
        for event in pg.event.get(): # 이벤트 리스트 반복
            cur_player = list(player_pos.keys())[cnt % PLAYER] # 현재 플레이어
            if all(isLosed.values()): # 모든 플레이어가 패배한 경우
                main_theme.stop() # 메인 테마 정지
                if lose_sound.get_num_channels() == 0: lose_sound.play(-1) # 패배 사운드 재생 (재생 중이 아닌 경우)
                print("모든 플레이어가 패배함")
                show_message("알림", "모든 플레이어가 패배하여 게임이 종료되었습니다.\n사건 봉투를 공개합니다.")
                end_screen(True, case_envelope, cur_player) # 게임 종료 화면
            if isLosed[cur_player] is True: # 해당 플레이어가 패배한 경우
                print() # 줄바꿈
                print(cur_player, "이/가 이미 패배함. 다음 차례로 넘어감")
                show_message("알림", f"{cur_player}님, 이미 패배하셨습니다.\n다음 차례로 넘어갑니다.")
                cnt += 1
                continue
            if event.type == pg.MOUSEBUTTONDOWN: # 마우스 버튼을 누른 경우
                x, y = event.pos  # 마우스 위치를 가져옵니다
                if (gmrule_btn_pos[0] <= x <= gmrule_btn_pos[0] + gmrule_btn_pos[2] 
                and gmrule_btn_pos[1] <= y <= gmrule_btn_pos[1] + gmrule_btn_pos[3]): # 게임 규칙 버튼을 누른 경우
                    show_game_rules() # 게임 규칙 표시
            if notMoved: # 이동하지 않은 경우
                player_pos, dice1, dice2, previous_dice1, previous_dice2 = do_dice_roll(previous_dice1, previous_dice2, 
                                                                                        dice1, dice2, player_pos) # 주사위 굴리기
                draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, 
                         dice_btn_pos, cur_player, case_envelope, player_cards) # 모든 요소 그리기
                other_players_poss = {player[0]: (player[1][0], player[1][1]) 
                                      for player in player_pos.items() if player[0] != cur_player} # 나머지 플레이어들의 좌표를 가져옵니다
                new_pos, reason = move_player(cur_player, player_pos[cur_player], dice1, dice2, 
                                              other_players_poss, isOutStartRoom, cur_room_loc, case_envelope, player_cards) # 플레이어 이동
                if new_pos != player_pos[cur_player] and reason is not None: # 이동한 경우
                    previous_dice1 = None  # 이전 주사위 결과를 초기화합니다.
                    previous_dice2 = None  # 이전 주사위 결과를 초기화합니다.
                    notMoved = False
                else:  # 플레이어가 이동하지 않은 경우
                    previous_dice1 = dice1  # 이전 주사위 결과를 저장합니다.
                    previous_dice2 = dice2  # 이전 주사위 결과를 저장합니다.
                    notMoved = True
                player_pos[cur_player] = new_pos
                draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, 
                         dice_btn_pos, cur_player, case_envelope, player_cards) # 모든 요소 그리기
            else: # 이동한 경우
                if event.type == pg.QUIT: running = False # 종료 버튼을 누른 경우
                if event.type == pg.MOUSEBUTTONDOWN: 
                    x, y = event.pos  # 클릭한 위치를 가져옵니다.
                    if (gmrule_btn_pos[0] + 3 * square_size <= x <= gmrule_btn_pos[0] + gmrule_btn_pos[2] + 3 * square_size
                        and gmrule_btn_pos[1] <= y <= gmrule_btn_pos[1] + gmrule_btn_pos[3]): # 옆에 있는 노트 버튼을 누른 경우
                        cur_player = list(player_pos.keys())[cnt - 1 % PLAYER] # 현재 플레이어 (주사위 전)
                        show_clue_notes(cur_player) # 노트 표시
                        cur_player = list(player_pos.keys())[cnt % PLAYER] # 현재 플레이어 (다시 복구)
                    if handle_dice_click(x, y, dice_btn_pos) : # 주사위 굴리기 버튼을 누른 경우
                        player_pos, dice1, dice2, previous_dice1, previous_dice2 = do_dice_roll(previous_dice1, previous_dice2, 
                                                                                                dice1, dice2, player_pos) # 주사위 굴리기
                        draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, 
                                 dice_btn_pos, cur_player, case_envelope, player_cards) # 모든 요소 그리기
                        other_players_poss = {player[0]: (player[1][0], player[1][1]) 
                                              for player in player_pos.items() if player[0] != cur_player} # 나머지 플레이어들의 좌표를 가져옵니다.    
                        new_pos, reason = move_player(cur_player, player_pos[cur_player], dice1, dice2, 
                                                      other_players_poss, isOutStartRoom, cur_room_loc, case_envelope, player_cards) # 플레이어 이동
                        if new_pos == player_pos[cur_player] and reason is None: # 이동하지 않은 경우
                            previous_dice1 = dice1 # 이전 주사위 결과를 저장합니다.
                            previous_dice2 = dice2 # 이전 주사위 결과를 저장합니다.
                            notMoved = True
                            if cur_room_loc[cur_player] != "복도": # 현재 플레이어의 방안에서, 방을 나가려고 시도했는데 막혀서 이동하지 못한 경우
                                print("방을 나가려고 시도했으나, 막혀서 이동하지 못함") # 콘솔에 출력
                                previous_dice1 = None # 이전 주사위 결과를 초기화합니다.
                                previous_dice2 = None # 이전 주사위 결과를 초기화합니다.
                                cnt += 1 # 카운트 증가
                                notMoved = False
                        else: # 이동한 경우
                            previous_dice1 = None # 이전 주사위 결과를 초기화합니다.
                            previous_dice2 = None # 이전 주사위 결과를 초기화합니다.     
                            cnt += 1 # 카운트 증가 
                            notMoved = False      
                        player_pos[cur_player] = new_pos  # 플레이어 위치를 새로운 위치로 설정합니다.
                        draw_all(font, grid, room_walls, thickness, player_pos, dice1, dice2, 
                                 dice_btn_pos, cur_player, case_envelope, player_cards) # 모든 요소 그리기
    pg.quit() # pg 종료 

# 인트로 화면
def intro_screen(): 
    screen = pg.display.set_mode(window_size)
    pg.display.set_caption("인트로")

    font = pg.font.SysFont("malgungothic", 23)
    screen.fill(WHITE) 
    screen.blit(cluedo_logo, ((window_size[0] - cluedo_logo.get_width()) // 2, (window_size[1] - cluedo_logo.get_height()) // 2))  # 이미지를 화면 중앙에 배치

    text = font.render("게임을 시작하려면 아무 키를 입력하세요...", True, BLACK)
    text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] - 50))
    screen.blit(text, text_rect)

    pg.display.flip()

    wait = True # 아무 키나 누를 때까지 대기
    while wait:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                wait = False

def fade_out(): # 페이드 아웃 함수
    alpha = 0  # 최초 알파값
    screen = pg.display.set_mode(window_size) # 화면 설정

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.fill(BLACK)  

        fade_surface = pg.Surface(window_size)
        fade_surface.fill(BLACK)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pg.display.flip()

        alpha += 2
        if alpha > 255: alpha = 255 # 알파값이 255보다 크면 255로 설정
        if alpha >= 255: return # 알파값이 255보다 크거나 같으면 반환
        clock.tick(FPS) # FPS 설정

if __name__ == "__main__":
    intro_screen() # 인트로 화면
    fade_out() # 페이드 아웃
    show_game_rules() # 게임 규칙 표시
    main() # 메인 함수 실행