# Default configuration
from othello_configuration_editable import *

PLAYERNAME = {"player1": "player1", "player2": "player2"}
MATCHNUMBER = 3
TIMELIMIT = {"player1": 60000, "player2": 60000}
DISPLAY = ""
HANDICAP = {"player1": "", "player2": ""}

# TODO: ****_editable.pyを検査して、妥当な値のみを通す
# そうでない場合は規定値を使う(か修正して利用する)

# playerの表示名
if "PLAYERNAME_EDITABLE" in globals():
    try:
        name1 = PLAYERNAME_EDITABLE["player1"]
        name2 = PLAYERNAME_EDITABLE["player2"]
        if type(name1) == str and type(name2) == str:
            PLAYERNAME["player1"] = name1[:10]
            PLAYERNAME["player2"] = name2[:10]
    except:
        pass

# 対戦数
if "MATCHNUMBER_EDITABLE" in globals():
    try:
        number = MATCHNUMBER_EDITABLE
        if type(number) == int:
            if number > 0 and number <= 100:
                MATCHNUMBER = number
    except:
        pass

# 制限時間
if "TIMELIMIT_EDITABLE" in globals():
    try:
        time1 = TIMELIMIT_EDITABLE["player1"]
        time2 = TIMELIMIT_EDITABLE["player2"]
        if type(time1) == int and type(time2) == int:
            time1 = max(time1, 1000)
            time2 = max(time2, 1000)
            TIMELIMIT["player1"] = time1
            TIMELIMIT["player2"] = time2
    except:
        pass

# 表示方法
# TODO: 表示方法を考える
if "DISPLAY_EDITABLE" in globals():
    try:
        way = DISPLAY_EDITABLE
        if type(way) == str:
            if way == "":
                pass
            elif way == "":
                pass
            elif way == "":
                pass
            else:
                pass
    except:
        pass


# ハンデ
# TODO: ハンデの種類を考える
if "HANDICAP_EDITABLE" in globals():
    try:
        way = HANDICAP_EDITABLE
        if type(way) == str:
            if way == "":
                pass
            elif way == "":
                pass
            elif way == "":
                pass
            else:
                pass
    except:
        pass