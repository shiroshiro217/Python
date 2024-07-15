import math

# 計算傷害
def cal_damage(attack, defence, power, bonus):
    return math.floor((110 / 250 * (attack / defence) * power + 2) * bonus)

# 計算攻擊力
def cal_attack(damage, defence, power, bonus):
    return (damage / bonus - 2) / power / (110 / 250) * defence

# 計算防禦力
def cal_defence(damage, attack, power, bonus):
    return attack / ((damage / bonus - 2) / power / (110 / 250))

# 計算努力值
def cal_basepoint(iv, basepoints, species_strength, status, lv):

    for i in range(6):

        # HP計算公式
        if i == 0:
            basepoints.append((math.ceil(((status[i] - lv - 10) * 100) / lv) - species_strength[i] * 2 - iv[i]) * 4)

        # 判斷是否有性格加成 1.1 0.9 1
        elif i == 2:
            basepoints.append(((math.ceil(status[i] / 1.1) - 5) * 100 / lv - species_strength[i] * 2 - iv[i]) * 4)
        
        elif i == 3:
            basepoints.append(((math.ceil(status[i] / 0.9) - 5) * 100 / lv - species_strength[i] * 2 - iv[i]) * 4)

        else:
            basepoints.append(((status[i] - 5) * 100 / lv - species_strength[i] * 2 - iv[i]) * 4)

    return basepoints

# 計算能力值
def cal_status(iv, basepoints, species_strength, status, lv):
    for i in range(6):
        if i == 0:
            status.append((math.floor((species_strength[i] * 2 + iv[i] + basepoints[i] / 4)) * lv) / 100 + 10 + lv)
        
        # 性格修正 2 = 防禦
        elif i == 2:
            status.append(((math.floor((species_strength[i] * 2 + iv[i] + basepoints[i] / 4)) * lv) / 100 + 5) * 1.1)
        
        elif i == 3:
            status.append(((math.floor((species_strength[i] * 2 + iv[i] + basepoints[i] / 4)) * lv) / 100 + 5) * 0.9)

        # 性格修正*1
        else:
            status.append((math.floor((species_strength[i] * 2 + iv[i] + basepoints[i] / 4)) * lv) / 100 + 5)
    
    # 回傳能力值列表
    return status

while True:
    mode = input("請輸入模式(A=計算傷害 B=推算攻擊 C=推算防禦 D=推算努力值 E=計算能力值 Q=退出):").upper()

    if mode == "A":
        print("選擇了計算傷害功能")
        attack = int(input("輸入攻擊方攻擊力:"))
        defence = int(input("輸入防禦方防禦力:"))
        power = int(input("輸入招式威力:"))
        bonus = float(input("輸入加成:"))
        damage = cal_damage(attack, defence, power, bonus)

        print(f"造成傷害為:{damage}")

    elif mode == "B":
        print("選擇了推算攻擊功能")
        damage = int(input("輸入造成傷害:"))
        defence = int(input("輸入防禦方防禦力:")) 
        power = int(input("輸入招式威力:"))
        bonus = float(input("輸入加成:"))
        attack = cal_attack(damage, defence, power, bonus)
        
        print(f"攻擊力為:{attack}")

    elif mode == "C":
        print("選擇了推算防禦功能")
        damage = int(input("輸入造成傷害:"))
        attack = int(input("輸入攻擊方攻擊力:"))
        power = int(input("輸入招式威力:"))
        bonus = float(input("輸入加成:"))
        defence = cal_defence(damage, attack, power, bonus)

        print(f"防禦力為:{defence}")
    
    # 提供計算努力值所需參數
    elif mode == "D":
        iv = []
        basepoints = []
        species_strength = []
        status = []
        status_string = ["HP", "攻擊", "防禦", "特攻", "特防", "速度"]
        pokemon_name = input("請輸入名字:")

        print("選擇了推算努力值功能")

        for i in range(6):
            iv.append(int(input(f"請輸入{status_string[i]}的個體值:")))
        print("個體值輸入完畢\n")

        for i in range(6):
            species_strength.append(int(input(f"請輸入{status_string[i]}的種族值:")))
        print("種族值輸入完畢\n")

        for i in range(6):
            status.append(int(input(f"請輸入{status_string[i]}的能力值:")))
        print("能力值輸入完畢\n")

        lv = int(input("請輸入等級:"))

        bp = cal_basepoint(iv, basepoints, species_strength, status, lv)
        for i in range(6):
            print(f"{pokemon_name}的{status_string[i]}努力值是{bp[i]}")

    elif mode == "E":
        iv = []
        species_strength = []
        status = []
        # 預設努力值
        # basepoints = [212, 4, 116, 0, 68, 108]
        basepoints = [252, 252, 252, 252, 252, 252]
        status_string = ["HP", "攻擊", "防禦", "特攻", "特防", "速度"]
        pokemon_name = input("請輸入名字:")

        print("選擇了計算能力值功能")

        for i in range(6):
            iv.append(int(input(f"請輸入{status_string[i]}的個體值:")))
        print("個體值輸入完畢\n")

        for i in range(6):
            species_strength.append(int(input(f"請輸入{status_string[i]}的種族值:")))
        print("種族值輸入完畢\n")

        lv = int(input("請輸入等級:"))
        status = cal_status(iv, basepoints, species_strength, status, lv)
        
        for i in range(6):
            print(f"{pokemon_name}的{status_string[i]}能力值是{status[i]}")

    elif mode == "Q":
        break

    else:
        print("輸入無效")