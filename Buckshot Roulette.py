import sys
import time
import random
import threading
def cp(text):
    print(text)
def ci(prompt=""):
    return input(prompt)
def reload():
    global shotgun, lives, blanks
    while True:
        shotgun.clear()
        lives = 0
        blanks = 0
        for i in range(random.randint(3, 8)):
            shell = random.randint(0, 1)
            shotgun.append(shell)
            if shell==1:
                lives += 1
            else:
                blanks += 1
        if not blanks==0 and not lives==0:
            break
    cp(f"{lives} lives, {blanks} blanks.")
    for i in range(2):
        player.append(random.choice(items))
        dealer.append(random.choice(items))
def glass():
    global current, dk, player, dealer
    if shotgun:
        current = bullets[shotgun[0]]
        if turn=="player":
            cp(f"current round is {current}.")
            player.remove("magnifying glass")
        else:
            dk = 1
            dealer.remove("magnifying glass")
    else:
        if turn=="player":
            cp("shotgun is empty.")
def beer():
    global shotgun, current, lives, blanks, player, dealer
    if shotgun:
        current = bullets[shotgun[0]]
        shotgun.pop(0)
        if current == "live":
            lives -= 1
        else:
            blanks -= 1
        cp(f"ejected a {current} round.")
    else:
        cp("No shells left to eject.")
    if turn=="player":
        player.remove("beer")
    else:
        dealer.remove("beer")
def hand():
    global dl, pl, player, dealer
    if turn=="player":
        if dl==0:
            dl = 1
            cp("dealer is handcuffed now.")
            player.remove("handcuffs")
        else:
            cp("dealer is already handcuffed.")
    else:
        if pl==0:
            pl = 1
            cp("you got handcuffed by the dealer.")
            dealer.remove("handcuffs")
def cigar():
    global plives, dlives
    if turn=="player":
        if plives != maxlives:
            plives += 1
            cp(f"you now have {plives} lives.")
            player.remove("cigarettes")
    else:
        if dlives != maxlives:
            dlives += 1
            cp(f"the dealer now has {dlives} lives.")
            dealer.remove("cigarettes")
def shoot():
    global plives, dlives, ntp, ntd, shotgun, current, pd, saw
    if not shotgun:
        cp("No shells left to shoot.")
        return
    current = bullets[shotgun[0]]
    shotgun.pop(0)
    if turn=="player":
        if pd=="y":
            if current=="live":
                plives -= 1
                cp("you shot yourself with a live round, you lost a life.")
            else:
                ntp += 1
                cp("you shot yourself and it was a blank, you get an extra turn.")
        else:
            if current=="live":
                if saw==0:
                    dlives -= 1
                    cp("you shot the dealer with a live round, the dealer lost a life.")
                else:
                    dlives -= 2
                    cp("you shot the dealer with a live round, the dealer lost two lives.")
            else:
                cp("you shot the dealer with a blank round.")
    else:
        if pd=="y":
            if current=="live":
                if saw==0:
                    plives -= 1
                    cp("the dealer shot you with a live round, you lost a life.")
                else:
                    plives -= 2
                    cp("the dealer shot you with a live round, you lost two lives.")
            else:
                cp("the dealer shot you with a blank round.")
        else:
            if current=="live":
                dlives -= 1
                cp("the dealer shot himself with a live round, he lost a life.")
            else:
                ntd += 1
                cp("the dealer shot himself with a blank round.")
    time.sleep(2)
    saw = 0
    cp(f"{name} {plives}, dealer {dlives}.")
def main():
    global to, turn, pl, ntd, dl, ntp, current, end, r, don, m, plives, dlives, player, dealer, donr, ch
    while r < 3:
        while plives > 0 and dlives > 0:
            if not shotgun:
                cp("reloading...")
                time.sleep(1)
                reload()
            time.sleep(2)
            if donr==0 and r==2 and ch==0:
                cp("dealer: now it's me and you dancing on the edge of life and death. no more defibrillators, no more blood transfusions. are you ready?")
                time.sleep(4)
                ch = 1
            to = 0
            if shotgun:
                current = bullets[shotgun[0]]
            if turn=="player":
                if ntd==0:
                    if pl==0:
                        playert()
                    else:
                        to = 1
                        pl = 0.5
                        print(" you are handcuffed, turn skipped.")
                        turn = "dealer"
                        dealert()
                else:
                    turn = "dealer"
                    dealert()
                    ntd -= 1
            else:
                if ntp==0:
                    if dl==0:
                        dealert()
                    else:
                        to = 1
                        dl = 0.5
                        turn = "player"
                        playert()
                else:
                    turn = "player"
                    playert()
                    ntp -= 1
            while to==0:
                time.sleep(0.1)
            time.sleep(2)
            if turn=="player":
                turn = "dealer"
            else:
                turn = "player"
        r += 1
        if dlives<1:
            print("you win this round.")
        if plives<1:
            r = 0
            if ch==0:
                print("you died, you got revived by the doctor.")
                time.sleep(2)
                cp(f"doctor: wake up, {name}.")
            else:
                cp("you died..")
                sys.exit()
        plives = 6
        dlives = 6
        dealer.clear()
        player.clear()
        reload()
    end = 1
    m = round(m)
    if m<10:
        m = 10
    while don not in ["y", "n"]:
        don = ci(f"double or nothing? the current prize is {m}. (y/n)")
        if don not in ["y", "n"]:
            print("invalid input")
def playert():
    global pd, to, saw, dl, rng, plives
    while True:
        while True:
            for i in range(len(player)):
                print(f"{i} - {player[i]}")
            puse = ci(f"what item to use? (enter the number, leave blank if you dont want to use anything). ")
            if int(puse) < len(player) or puse == len(player):
                if player[int(puse)]=="magnifying glass":
                    glass()
                elif player[int(puse)]=="beer":
                    beer()
                elif player[int(puse)]=="handcuffs":
                    if dl==0:
                        hand()
                    elif dl==1:
                        cp("handcuffs don't stack.")
                    else:
                        cp("dealer is already handcuffed")
                elif player[int(puse)]=="cigarettes":
                    cigar()
                elif player[int(puse)]=="saw":
                    if saw==0:
                        saw = 1
                        player.pop(player.index("saw"))
                        cp("next shot does 2 damage if it is live.")
                    else:
                        cp("saw damage doesn't stack.")
                elif player[int(puse)]=="inverter":
                    invert()
                elif player[int(puse)]=="expired medicine":
                    rng = random.randint(0, 1)
                    if rng==1:
                        plives += 2
                        if plives>maxlives:
                            plives = maxlives
                        cp("you gained 2 lives.")
                    else:
                        plives -= 1
                        cp("you lost 1 life.")
                time.sleep(2)
                mi = ci("do you want to use more items? (y/n) ")
                if mi=="n":
                    break
                elif mi!="y":
                    cp("invalid input.")
            else:
                cp("invalid input.")
        break
    while True:
        pd = ci("shoot the dealer or yourself? (d/y) ")
        if pd=="d" or pd=="y":
            break
        else:
            cp("invalid input.")
    shoot()
    if dl==0.5:
        dl = 0
    to = 1
def dealert():
    global pl, to, pd, current, lives, blanks, saw, rng, dlives, mode
    time.sleep(1)
    cp("dealer's turn")
    if shotgun:
        current = bullets[shotgun[0]]
    time.sleep(2)
    if not mode=="e":
        if "cigarettes" in dealer and dlives < maxlives:
            cigar()
        if "beer" in dealer and lives==blanks:
            beer()
        if "handcuffs" in dealer:
            if dl==0:
                hand()
        if "magnifying glass" in dealer and lives+blanks<3:
            glass()
        if "saw" in dealer and (lives>blanks or dk==1):
            if dk==1:
                if current=="live":
                    saw = 1
                    dealer.remove("saw")
            elif lives>blanks:
                saw = 1
                dealer.remove("saw")
        if "inverter" in dealer and blanks>lives:
            invert()
        if "expired medicine" in dealer and lives>1 and lives<maxlives-2:
            dealer.remove("expired medicine")
            rng = random.randint(0, 1)
            if rng==1:
                dlives += 2
                cp("the dealer gained 2 lives.")
            else:
                dlives -= 1
                cp("the dealer lost 1 life.")
        time.sleep(1.5)
    if shotgun:
        current = bullets[shotgun[0]]
    if mode=="e":
        rng = random.randint(0, 1)
        if rng==1:
            pd = "y"
            shoot()
        else:
            pd = "d"
            shoot()
    elif mode=="n":
        rng = random.randint(0, 1)
        if rng==1:
            if dk==1:
                if current=="live":
                    pd = "y"
                    shoot()
                else:
                    pd = "d"
                    shoot()
            else:
                if dlives < 3:
                    pd = "y"
                    shoot()
                else:
                    if lives < blanks:
                        pd = "d"
                        shoot()
                    elif lives==blanks:
                        pd = "y"
                        shoot()
                    else:
                        pd = "y"
                        shoot()
        else:
            rng = random.randint(0, 1)
            if rng==1:
                pd = "y"
                shoot()
            else:
                pd = "d"
                shoot()
    else:
        if dk==1:
            if current=="live":
                pd = "y"
                shoot()
            else:
                pd = "d"
                shoot()
        else:
            if dlives < 3:
                pd = "y"
                shoot()
            else:
                if lives < blanks:
                    pd = "d"
                    shoot()
                elif lives==blanks:
                    pd = "y"
                    shoot()
                else:
                    pd = "y"
                    shoot()
    time.sleep(2)
    if pl==0.5:
        pl = 0
    to = 1
def timer():
    global end, m
    while end==0:
        time.sleep(1)
        m -= 66.67
def invert():
    global shotgun, lives, blanks, current
    if shotgun:
        if shotgun[0] == 0:
            shotgun[0] = 1
            blanks -= 1
            lives += 1
        else:
            shotgun[0] = 0
            lives -= 1
            blanks += 1
        current = bullets[shotgun[0]]
    else:
        cp("no round to invert.")
    if turn == "player":
        player.remove("inverter")
    else:
        dealer.remove("inverter")
player = []
dealer = []
plives = 6
dlives = 6
maxlives = 6
dk=0
ntp = 0
ntd = 0
pl = 0
dl = 0
end = 0
m = 70000
don = ""
r = 0
ch = 0
saw = 0
donr = 0
rng = 0
shotgun = []
bullets = ["blank", "live"]
items = ["magnifying glass", "beer", "handcuffs", "cigarettes", "saw", "inverter", "expired medicine"]
turn="player"
pd=""
cp("welcome to buckshot roulette!")
cp("")
while True:
    mode = ci("easy, normal, or hard? (e/n/h)")
    if mode=="e" or mode=="n" or mode=="h":
        break
cp("dealer: please, sign this waiver.")
name = ci("enter your name. ")
ee = threading.Thread(target=timer, name="ee")
ee.start()
main()
while don=="y":
    donr = 1
    end = 0
    m *= 2
    r = 0
    plives = 6
    dlives = 6
    dealer.clear()
    player.clear()
    main()
    don = ""
    while end==0:
        time.sleep(0.1)
print("")
print(f"you win, you got {m}$.")