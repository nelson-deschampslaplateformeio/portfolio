case=["1","2","3",
      "4","5","6",
      "7","8","9"]
symbol="X"
restart=""
def tab(case):
    espace="|         |         |         |"
    ligne="+---------+---------+---------+"
    print(ligne)
    for i in range(0,7,3):
        print(espace)
        print(f"|    {case[i]}    |    {case[i+1]}    |    {case[i+2]}    |")
        print(espace)
        print(ligne)
def check_win(case,symbol):
    raw(case)
    col(case)
    diag(case)
    if raw(case)==True or col(case)==True or diag(case)==True:
        tab(case)
        if symbol=="X":
                symbol="O"
        else:
            symbol="X"
        print("Bravo",symbol)
        return True
def raw(case):
    if case[0]==case[1]==case[2]:
        return True
    elif case[3]==case[4]==case[5]:
        return True
    elif case[6]==case[7]==case[8]:
        return True
def col(case):
    if case[0]==case[3]==case[6]:
        return True
    elif case[1]==case[4]==case[7]:
        return True
    elif case[2]==case[5]==case[8]:
        return True
def diag(case):
    if case[0]==case[4]==case[8]:
        return True
    elif case[2]==case[4]==case[6]:
        return True
def players(symbol):
    select=int(input(f"Joueur {symbol}, choisissez une case sur laquelle jouer :"))
    if select>9 or case[select-1]=="X" or case[select-1]=="O":
            while True:
                if select>9 or case[select-1]=="X" or case[select-1]=="O":
                    select=int(input(f"MAUVAISE CASE !!! Joueur {symbol}, rejouez :"))
                elif symbol=="X":
                    case[select-1]=symbol
                    symbol="O"
                    break
                elif symbol=="O":
                    case[select-1]=symbol
                    symbol="X"
                    break
    elif symbol=="O" and case[select-1]!="X" and case[select-1]!="O":
        case[select-1]=symbol
        symbol="X"
    elif symbol=="X" and case[select-1]!="X" and case[select-1]!="O":
        case[select-1]=symbol
        symbol="O"
    return symbol

while restart!="n" or restart!="N":
    tab(case)
    for i in range(9):
        symbol=players(symbol)
        tab(case)
        if check_win(case,symbol)==True:
            break
        elif i==8:
            print("Match nul !!!")
    restart=input("Continuer ? (O/N) :")
    if restart=="n" or restart=="N":
        break
    elif restart=="o" or restart=="O":
        case=["1","2","3",
              "4","5","6",
              "7","8","9"]
        print("C'est reparti !!!")
        symbol="X"        
    else:
        while restart!="o" or restart!="O" or restart!="n" or restart!="N":
            restart=input("ERREUR !!! Continuer ? (O/N) :")
            if restart=="o" or restart=="O":
                case=["1","2","3",
                      "4","5","6",
                      "7","8","9"]
                print("C'est reparti !!!")
                symbol="X"
                break
            elif restart=="n" or restart=="N":
                break
        if restart=="n" or restart=="N":
            break
        #test