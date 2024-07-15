import pygame
import sys
import random
# 省略輸入用的
from pygame.locals import *

# 設定顏色區
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
CYAN = (0,255,255)
BLINK = [(224,255,255), (192,240,255), (128,224,255), (64,192,255), (128,224,255), (192,240,255)]

# 載入圖片區
imgTitle = pygame.image.load("img/title.png")
imgWall = pygame.image.load("img/wall.png")
imgWall2 = pygame.image.load("img/wall2.png")
imgDark = pygame.image.load("img/dark.png")
imgPara = pygame.image.load("img/parameter.png")
imgBtlBG = pygame.image.load("img/btlbg.png")
imgEnemy = pygame.image.load("img/enemy1.png")

imgItem = [
    pygame.image.load("img/potion.png"),
    pygame.image.load("img/blaze_gem.png"),
    pygame.image.load("img/spoiled.png"),
    pygame.image.load("img/apple.png"),
    pygame.image.load("img/meat.png")
]

imgFloor = [
    pygame.image.load("img/floor.png"),
    pygame.image.load("img/tbox.png"),
    pygame.image.load("img/cocoon.png"),
    pygame.image.load("img/stairs.png")
]

imgPlayer = [
    pygame.image.load(f"img/mychr{i}.png") for i in range(9)
]

imgEffect = [
    pygame.image.load("img/effect_a.png"),
    pygame.image.load("img/effect_b.png")
]

# 宣告變數區
speed = 1
idx = 0
tmr = 0
floor = 0
fl_max = 1
welcome = 0

pl_x = 0
pl_y = 0
pl_d = 0
pl_a = 0
pl_lifemax = 0
pl_life = 0
pl_str = 0
food = 0
potion = 1
blazegem = 1
treasure = 0

emy_name = ""
emy_lifemax = 0
emy_life = 0
emy_str = 0
emy_x = 0
emy_y = 0
emy_step = 0
emy_blink = 0

dmg_eff = 0
btl_cmd = 0

COMMAND = ["[A]ttack", "[P]otion", "[B]laze gem", "[R]un"]
TRE_NAME = ["Potion", "Blaze gem", "Food spoiled.", "Food +20", "Food +100"]
EMY_NAME = [
    "Green slime", "Red slime", "Axe beast", "Ogre", "Sword man",
    "Death hornet", "Signal slime", "Devil plant", "Twin killer", "Hell"
]

# 迷宮列表
MAZE_W = 11
MAZE_H = 9
maze = []
for y in range(MAZE_H):
        maze.append([0]*MAZE_W)

# 地下城列表
DUNGEON_W = MAZE_W*3
DUNGEON_H = MAZE_H*3
dungeon = []
for y in range(DUNGEON_H):
    dungeon.append([0]*DUNGEON_W)

# 產生地下城
def make_dungeon():
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]

    # 最上排和最下排設為牆壁
    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[MAZE_H-1][x] = 1
    
    # 最左列和最右列設為牆壁
    for y in range(MAZE_H):
        maze[y][0] = 1
        maze[y][MAZE_W-1] = 1

    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            maze[y][x] = 0

    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            maze[y][x] = 1

    for y in range(2, MAZE_H-2, 2):
        for x in range(2, MAZE_W-2, 2):
            d = random.randint(0, 3)
            if x > 2:
                d = random.randint(0, 2)
            maze[y+YP[d]][x+XP[d]] = 1
    
    for y in range(DUNGEON_H):
        for x in range(DUNGEON_W):
            dungeon[y][x] = 9
    
    # 配置房間與通道
    for y in range(1, MAZE_H-1):
        for x in range(1, MAZE_W-1):
            dx = x*3+1
            dy = y*3+1
            if maze[y][x] == 0:

                # 建立房間
                if random.randint(0, 99) < 20:
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy+ry][dx+rx] = 0
                
                # 建立通道
                else:
                    dungeon[dy][dx] = 0
                    if maze[y-1][x] == 0:
                        dungeon[dy-1][dx] = 0

                    if maze[y+1][x] == 0:
                        dungeon[dy+1][dx] = 0

                    if maze[y][x-1] == 0:
                        dungeon[dy][dx-1] = 0

                    if maze[y][x+1] == 0:
                        dungeon[dy][dx+1] = 0

def draw_dungeon(bg, fnt):
    bg.fill(BLACK)
    for y in range(-4, 6):
        for x in range(-5, 6):
            X = (x+5)*80
            Y = (y+4)*80
            dx = pl_x + x
            dy = pl_y + y

            if 0 <= dx < DUNGEON_W and 0 <= dy < DUNGEON_H:
                if dungeon[dy][dx] <= 3:
                    bg.blit(imgFloor[dungeon[dy][dx]], [X, Y])

                if dungeon[dy][dx] == 9:
                    bg.blit(imgWall, [X, Y-40])

                    if dy >= 1 and dungeon[dy-1][dx] == 9:
                        bg.blit(imgWall2, [X, Y-80])
            
            # 顯示主角
            if x == 0 and y == 0:
                bg.blit(imgPlayer[pl_a], [X, Y-40])
    
    # 黑色四角框框
    bg.blit(imgDark, [0, 0])
    draw_para(bg, fnt)

# 在地板配置道具
def put_event():
    global pl_x, pl_y, pl_d, pl_a

    # 配置樓梯
    while True:
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)

        if dungeon[y][x] == 0:
            for ry in range(-1, 2):
                for rx in range(-1, 2):
                    dungeon[y+ry][x+rx] = 0
            dungeon[y][x] = 3
            break
    
    # 配置寶箱跟繭
    for i in range(60):
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)

        if dungeon[y][x] == 0:
            dungeon[y][x] = random.choice([1, 2, 2, 2, 2])
    
    # 玩家初始位置
    while True:
        pl_x = random.randint(3, DUNGEON_W-4)
        pl_y = random.randint(3, DUNGEON_H-4)
        if dungeon[pl_y][pl_x] == 0:
            break
    
    pl_d = 1
    pl_a = 2

# 移動主角
def move_player(key):
    global idx, tmr, pl_x, pl_y, pl_d, pl_a, pl_life, food, potion, blazegem, treasure

    # 玩家跟寶箱重疊
    if dungeon[pl_y][pl_x] == 1:
        dungeon[pl_y][pl_x] = 0
        treasure = random.choice([0, 0, 0, 1, 1, 1, 1, 1, 1, 2])

        if treasure == 0:
            potion += 1
        if treasure == 1:
            blazegem += 1
        if treasure == 2:
            food = int(food/2)
        
        idx = 3
        tmr = 0
        return

    # 玩家跟繭重疊
    if dungeon[pl_y][pl_x] == 2:
        dungeon[pl_y][pl_x] = 0
        r = random.randint(0, 99)
        
        # 食物
        if r < 40:
            treasure = random.choice([3, 3, 3, 4])
            if treasure == 3:
                food += 20
            if treasure == 4:
                food += 100
            idx = 3
            tmr = 0

        else:
            # 開始戰鬥
            idx = 10
            tmr = 0
        return
    
    if dungeon[pl_y][pl_x] == 3:
        # 切換畫面
        idx = 2
        tmr = 0
        return
    
    x = pl_x
    y = pl_y
    
    if key[K_UP]:
        pl_d = 0
        if dungeon[pl_y-1][pl_x] != 9:
            pl_y -= 1
    
    if key[K_DOWN]:
        pl_d = 1
        if dungeon[pl_y+1][pl_x] != 9:
            pl_y += 1

    if key[K_LEFT]:
        pl_d = 2
        if dungeon[pl_y][pl_x-1] != 9:
            pl_x -= 1
    
    if key[K_RIGHT]:
        pl_d = 3
        if dungeon[pl_y][pl_x+1] != 9:
            pl_x += 1
    
    # 控制食物存量與生命值的關係
    pl_a = pl_d * 2
    if pl_x != x or pl_y != y:
        pl_a += tmr % 2

        if food > 0:
            food -= 1
            if pl_life < pl_lifemax:
                pl_life += 1
        
        else:
            pl_life -= 5
            if pl_life <= 0:
                pl_life = 0
                pygame.mixer.music.stop()
                idx = 9
                tmr = 0

# 套用陰影效果的文字
def draw_text(bg, txt, x, y, fnt, col):
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])
    
# 顯示主角的能力
# 寫在draw_dungeon裡面 
def draw_para(bg, fnt):
    X = 30
    Y = 600
    bg.blit(imgPara, [X, Y])
    col = WHITE

    if pl_life < 10 and tmr % 2 == 0:
        col = RED
    
    draw_text(bg, f"{pl_life}/{pl_lifemax}", X+128, Y+6, fnt, col)
    draw_text(bg, f"{pl_str}", X+128, Y+33, fnt, WHITE)
    col = WHITE
    if food == 0 and tmr%2 == 0:
        col = RED
    
    draw_text(bg, str(food), X+128, Y+60, fnt, col)
    draw_text(bg, str(potion), X+266, Y+6, fnt, WHITE)
    draw_text(bg, str(blazegem), X+266, Y+33, fnt, WHITE)

# 準備進入戰鬥
def init_battle():
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_str, emy_x, emy_y
    typ = random.randint(0, floor)

    if floor >= 10:
        typ = random.randint(0, 9)
    
    lev = random.randint(1, floor)
    imgEnemy = pygame.image.load(f"img/enemy{typ}.png")
    
    emy_name = f"{EMY_NAME[typ]} LV{lev}"
    emy_lifemax = 60*(typ+1) + (lev-1)*10
    emy_life = emy_lifemax
    emy_str = int(emy_lifemax/8)

    emy_x = 440-imgEnemy.get_width()/2
    emy_y = 560-imgEnemy.get_height()

# 繪製敵人體力條
def draw_bar(bg, x, y, w, h, val, max):
    pygame.draw.rect(bg, WHITE, [x-2, y-2, w+4, h+4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    
    if val > 0:
        pygame.draw.rect(bg, (0,128,255), [x, y, w*val/max, h])

# 繪製戰鬥畫面
def draw_battle(bg, fnt):
    global emy_blink, dmg_eff
    bx = 0
    by = 0
    if dmg_eff > 0:
        dmg_eff -= 1

        # 背景晃動
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    
    bg.blit(imgBtlBG, [bx, by])
    
    if emy_life > 0 and emy_blink%2 == 0:
        bg.blit(imgEnemy, [emy_x, emy_y+emy_step])

    draw_bar(bg, 340, 580, 200, 10, emy_life, emy_lifemax)

    if emy_blink > 0:
        emy_blink -= 1
    
    # 顯示戰鬥訊息
    for i in range(10):
        draw_text(bg, message[i], 600, 100+i*50, fnt, WHITE)
    
    draw_para(bg, fnt)

# 輸入與顯示戰鬥指令
def battle_command(bg, fnt, key):
    global btl_cmd
    ent = False

    # a鍵攻擊
    if key[K_a]:
        btl_cmd = 0
        ent = True
    
    # p鍵藥水
    if key[K_p]:
        btl_cmd = 1
        ent = True

    # b鍵火焰石
    if key[K_b]:
        btl_cmd = 2
        ent = True
    
    # r鍵逃跑
    if key[K_r]:
        btl_cmd = 3
        ent = True

    if key[K_UP] and btl_cmd > 0:
        btl_cmd -= 1
    
    if key[K_DOWN] and btl_cmd < 3:
        btl_cmd += 1
    
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    
    for i in range(4):
        c = WHITE
        if btl_cmd == i:
            c = BLINK[tmr%6]

        draw_text(bg, COMMAND[i], 20, 360+i*60, fnt, c)

    return ent

# 訊息處理
message = [""]*10
def init_message():
    for i in range(10):
        message[i] = ""

# 依序設置訊息
def set_message(msg):
    for i in range(10):
        if message[i] == "":
            message[i] = msg
            return
        
    for i in range(9):
        message[i] = message[i+1]
    message[9] = msg

def main():
    global speed, idx, tmr, floor, fl_max, welcome
    global pl_a, pl_lifemax, pl_life, pl_str, food, potion, blazegem
    global emy_life, emy_step, emy_blink, dmg_eff
    dmg = 0
    lif_p = 0

    # strong
    str_p = 0

    pygame.init()
    pygame.display.set_caption("一小時地下城")
    
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    fontS = pygame.font.Font(None, 30)

    # 音效
    se = [
        pygame.mixer.Sound("sound/ohd_se_attack.ogg"),
        pygame.mixer.Sound("sound/ohd_se_blaze.ogg"),
        pygame.mixer.Sound("sound/ohd_se_potion.ogg"),
        pygame.mixer.Sound("sound/ohd_jin_gameover.ogg"),
        pygame.mixer.Sound("sound/ohd_jin_levup.ogg"),
        pygame.mixer.Sound("sound/ohd_jin_win.ogg")
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == K_s:
                    speed += 1

                    if speed == 4:
                        speed = 1

        tmr += 1
        key = pygame.key.get_pressed()

        # 標題畫面
        if idx == 0:
            if tmr == 1:

                # 載入背景音樂
                pygame.mixer.music.load("sound/ohd_bgm_title.ogg")

                # -1表示無限循環
                pygame.mixer.music.play(-1)
                # 調整音量倍率
                pygame.mixer.music.set_volume(0.1)
            
            screen.fill(BLACK)
            screen.blit(imgTitle, [40, 60])

            if fl_max >= 2:
                draw_text(screen, f"You reached floor{fl_max}.", 300, 460, font, CYAN)
            
            draw_text(screen, "Press space key", 320, 560, font, BLINK[tmr%6])
            
            # 按下空白鍵
            if key[K_SPACE]:
                make_dungeon()
                put_event()
                floor = 1
                welcome = 15
                pl_lifemax = 30
                pl_life = pl_lifemax
                pl_str = 100
                food = 300
                potion = 1
                blazegem = 1
                idx = 1
                pygame.mixer.music.load("sound/ohd_bgm_field.ogg")
                pygame.mixer.music.play(-1)
        
        # 玩家移動
        elif idx == 1:
            move_player(key)
            draw_dungeon(screen, fontS)
            draw_text(screen, f"floor{floor}({pl_x},{pl_y})", 60, 40, fontS, WHITE)

            if welcome > 0:
                welcome -= 3
                draw_text(screen, f"Welcome to floor{floor}.", 300, 180, font, CYAN)
        
        # 切換畫面
        elif idx == 2:
            draw_dungeon(screen, fontS)
            if 1 <= tmr <= 5:
                h = 80*tmr
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            
            if tmr == 5:
                floor += 1
                if floor > fl_max:
                    fl_max = floor
                
                welcome = 15
                make_dungeon()
                put_event()
            
            if 6 <= tmr <= 9:
                h = 80*(10-tmr)
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
            
            if tmr == 10:
                idx = 1
        
        # 拿到道具或踩到陷阱
        elif idx == 3:
            draw_dungeon(screen, fontS)
            screen.blit(imgItem[treasure], [320, 220])
            draw_text(screen, TRE_NAME[treasure], 380, 240, font, WHITE)

            if tmr == 4:
                idx = 1
        
        # 遊戲結束
        elif idx == 9:
            if tmr <= 15:
                PL_TURN = [2, 4, 0, 6]
                pl_a = PL_TURN[tmr%4]

                if tmr == 15:
                    pl_a = 8
                draw_dungeon(screen, fontS)
            
            elif tmr == 16:
                se[3].play()
                se[3].set_volume(0.1)
                draw_text(screen, "You Died!", 380, 240, font, RED)
                draw_text(screen, "GAME OVER", 360, 380, font, RED)

            elif tmr == 40:

                # 暫停音樂
                se[3].stop()
                idx = 0
                tmr = 0
        
        # 戰鬥開始
        elif idx == 10:
            if tmr == 1:
                pygame.mixer.music.load("sound/ohd_bgm_battle.ogg")
                pygame.mixer.music.play(-1)
                init_battle()
                init_message()
            
            elif tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(imgBtlBG, [bx, by])
                draw_text(screen, "Encounter!!", 350, 200, font, WHITE)
            
            elif tmr <= 10:
                draw_battle(screen, fontS)
                draw_text(screen, f"{emy_name} appear!", 280, 200, font, WHITE)
            
            else:
                idx = 11
                tmr = 0
        
        # 輪到玩家輸入指令
        elif idx == 11:
            draw_battle(screen, fontS)

            if tmr == 1:
                set_message("Your turn.")
            
            if battle_command(screen, font, key) == True:
                if btl_cmd == 0:
                    idx = 12
                    tmr = 0
                
                if btl_cmd == 1 and potion > 0:
                    idx = 20
                    tmr = 0

                if btl_cmd == 2 and blazegem > 0:
                    idx = 21
                    tmr = 0

                if btl_cmd == 3:
                    idx = 14
                    tmr = 0

        elif idx == 12:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("You Attack!")
                se[0].play()
                se[0].set_volume(0.2)
                dmg = pl_str + random.randint(0, 9)

            if 2 <= tmr <= 4:
                screen.blit(imgEffect[0], [700-tmr*120, -100+tmr*120])           

            if tmr == 5:
                emy_blink = 5
                set_message(f"{dmg}pts of damage!")
            
            if tmr == 11:
                emy_life -= dmg
                if emy_life <= 0:
                    emy_life = 0
                    idx = 16
                    tmr = 0
            
            if tmr == 16:
                idx = 13
                tmr = 0
        
        # 敵人攻擊
        elif idx == 13:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Enemy turn.")
            
            if tmr == 5:
                set_message(f"{emy_name} attack!")
                se[0].play()
                se[0].set_volume(0.2)
                emy_step = 30
            
            if tmr == 9:
                dmg = emy_str + random.randint(0, 9)
                set_message(f"{dmg}pts of damage!")
                dmg_eff = 5
                emy_step = 0
            
            if tmr == 15:
                pl_life -= dmg
                if pl_life < 0:
                    pl_life = 0
                    idx = 15
                    tmr = 0

            if tmr == 20:
                idx = 11
                tmr = 0
        
        # 逃跑判定
        elif idx == 14:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("...")
            if tmr == 2:
                set_message("......")
            if tmr == 3:
                set_message(".........")
            if tmr == 4:
                set_message("............")
            if tmr == 5:
                if random.randint(0, 99) < 60:
                    idx = 22
                
                else:
                    set_message("You failed to flee")
            
            if tmr == 10:
                idx = 13
                tmr = 0

        # 戰鬥失敗
        elif idx == 15:
            draw_battle(screen, fontS)
            if tmr == 1:
                pygame.mixer.music.stop()
                set_message("You lose.")
            
            if tmr == 8:
                idx = 9
                tmr = 14
        
        # 打敗敵人
        elif idx == 16:

            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("You win!")
                pygame.mixer.music.stop()
                se[5].play()
                se[5].set_volume(0.1)

            if tmr == 16:
                idx = 22

                if random.randint(0, emy_lifemax) > random.randint(0, pl_lifemax):
                    
                    # 升等
                    idx = 17
                    tmr = 0

        # 升級
        elif idx == 17:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Level UP!")
                se[4].play()
                se[4].set_volume(0.1)
                lif_p = random.randint(10, 20)
                str_p = random.randint(5, 10)
            
            if tmr == 21:
                set_message(f"Max life + {lif_p}")
                pl_lifemax += lif_p
            
            if tmr == 26:
                set_message(f"Str + {str_p}")
                pl_str += str_p
            
            if tmr == 40:
                idx = 22
        
        # 使用藥水
        elif idx == 20:
            draw_battle(screen, fontS)
            if tmr == 1:
                set_message("Use Potion!")
                se[2].play()
                se[2].set_volume(0.5)
            
            if tmr == 6:
                pl_life = pl_lifemax
                potion -= 1
            
            if tmr == 11:
                idx = 13
                tmr = 0
        
        # 使用火焰石
        elif idx == 21:
            draw_battle(screen, fontS)
            img_rz = pygame.transform.rotozoom(imgEffect[1], 30*tmr, (12-tmr)/8)
            X = 440 - img_rz.get_width()/2
            Y = 360 - img_rz.get_height()/2
            screen.blit(img_rz, [X, Y])

            if tmr == 1:
                set_message("Use Blaze gem!")
                se[1].play()
                se[1].set_volume(0.2)
            
            if tmr == 6:
                blazegem -= 1
            
            if tmr == 11:
                dmg = 1000

                # 回到發動攻擊的tmr4
                idx = 12
                tmr = 4

        # 戰鬥結束
        elif idx == 22:
            pygame.mixer.music.load("sound/ohd_bgm_field.ogg")
            pygame.mixer.music.play(-1)
            idx = 1

        draw_text(screen, f"[S]peed{speed}", 740, 40, fontS, WHITE)

        pygame.display.update()
        clock.tick(4+2*speed)

if __name__ == "__main__":
    main()