'''All Sprites used were created by @LuizMelo from https://luizmelo.itch.io/
and @Ansimuz https://ansimuz.itch.io/  under Creative Commons Zero License

Pixelated Font taken from https://www.dafont.com/craftron-gaming.d6128?text=Octagram
<a target="_blank" href="https://icons8.com/icon/76916/tournament">Tournament</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>'''

# Display resolution of game window is 1280x720 pixels
import tkinter as tk, os, time
import random, json
from typing import Text

main = tk.Tk()

count,countsecond,npccount, npccountsecond = 0,0,0,0

#Initial positions of characters
defaultx_pc, defaulty_pc = 160,450
defaultx_npc, defaulty_npc = 700, 450

#Healthbar dimensions
plx1,ply1,plx2,ply2 = 152,62,353,73
npcx1,npcy1,npcx2,npcy2 = 702,62,899,73

platform = None
npc_health = 300
playerhealth = 150
score, pauseCount, bossCount = 0, 0, 0
events, topscores, datalist = [], [], []
countdownstate = None
label=''
npcmoving = None
countdown = 90

scorelist = [10,20,30,40,50]
backdrops = {1:"graphics/background1.png",2:"graphics/background2.png",3:"graphics/Title.png",4:"graphics/instructions.png",5:"graphics/leaderboardtitle.png"}
gamestate = True

# for animation functions
animate, animatingOnce, npcanimate, npcanimatingOnce= None, None, None, None


# Loads the default values of all characters and widgets from a .json file
def loaddefaults(i):
    global countdown, platform, count,countsecond,npccount, npccountsecond, defaultx_pc, defaulty_pc, defaultx_npc, defaulty_npc
    global plx1,ply1,plx2,ply2, npcx1,npcy1,npcx2,npcy2, npc_health, playerhealth, score
    with open("graphics/defaults.json",encoding="utf-8") as file:
        loaddata = json.load(file)
    count,countsecond,npccount, npccountsecond = loaddata["count"],loaddata["countsecond"],loaddata["npccount"],loaddata["npccountsecond"]
    countdown,  = loaddata["countdown"],
    defaultx_pc, defaulty_pc = loaddata["defaultx_pc"],loaddata["defaulty_pc"]
    defaultx_npc, defaulty_npc = loaddata["defaultx_npc"],loaddata["defaulty_npc"]
    plx1,ply1,plx2,ply2 = loaddata["plx1"],loaddata["ply1"],loaddata["plx2"],loaddata["ply2"]
    npcx1,npcy1,npcx2,npcy2 = loaddata["npcx1"],loaddata["npcy1"],loaddata["npcx2"],loaddata["npcy2"]
    npc_health, playerhealth = loaddata["npc_health"],loaddata["playerhealth"]
    if i == 1:
        score = loaddata["score"]
    else:
        pass

# Adds new values to the leaderboard.txt file
def checkleaderboard():
    global platform, topscores, datalist
    filepath = "graphics/leaderboard.txt"
    if os.path.isfile(filepath) and os.path.getsize(filepath) == 0:
        datalist = []
        for i in topscores:
            datalist.append(f"{i[0]}:{str(i[1])}\n")
        pass
    else:
        file  = open(filepath)
        datalist = file.read().splitlines()
        file.close()
        for i in topscores:
            datalist.append(f"{i[0]}:{str(i[1])}")

    with open(filepath,"w",encoding="utf-8") as datafile:
        for line in datalist:
            datafile.write(line+"\n")

# Reads the data from leaderboard.txt and sorts the scores to display top 5
def readleaderboard():
    global datalist, topscores, sortedtopscores
    filepath = "graphics/leaderboard.txt"
    with open(filepath,encoding="utf-8") as file:
        datalist = file.read().splitlines()
    topscores = []
    for i in datalist:
        topscores.append(list(i.split(":")))
    for i in topscores:
        i[1] = int(i[1])

    sortedtopscores = sorted(topscores,key = lambda x: x[1], reverse=True)[:5]
    return sortedtopscores

# Generates the screen window
def gamescreengenerate():
    main.eval('tk::PlaceWindow . center')  # Tried to center the window
    main.geometry("1280x720")
    main.resizable(False,False)
    posx,posy = int(main.winfo_screenwidth()/2 - 1280/2), 60 #winfo_screenwidth retrieves the screen width in pixels
    main.geometry(f"+{posx}+{posy}")  #Adjusts the window from left and top screen edges
    main.configure(bg='#000000')
    main.title("Octagram")
    main.wm_iconphoto(False,tk.PhotoImage(file="graphics/icon.png"))  #changes the window icon

# Animates .gif files
def animation(count, variable, whichframes,state):
    global animate, platform, pcframes
    next_frame = whichframes[count]
    platform.itemconfig(variable,image=next_frame)

    count += 1
    if count == pcframes[state]:
        count = 0
    animate = platform.after(60, lambda: animation(count, variable, whichframes, state))

# Animating the Playable Character
def animationOnce(countsecond, variable, whichframes,state,x):
    global animatingOnce, platform, pcframes
    platform.after_cancel(animate)
    next_frame = whichframes[countsecond]
    platform.itemconfig(variable,image=next_frame)
    countsecond += 1
    if countsecond == pcframes[state]:
        platform.after_cancel(animatingOnce)
        platform.after(60,animation(count,playableChar,player_stance[0],"idle"))
    elif countsecond != pcframes[state]:
        animatingOnce = platform.after(x, lambda: animationOnce(countsecond, variable, whichframes, state,x))

# Anmating npc
def npcanimation(npccount, variable, whichframes,state):
    global npcanimate, platform, pcframes
    next_frame = whichframes[npccount]
    platform.itemconfig(variable,image=next_frame)

    npccount += 1
    if npccount == pcframes[state]:
        npccount = 0
    npcanimate = platform.after(50, lambda: npcanimation(npccount, variable, whichframes, state))

# Animating NPC once
def npcanimationOnce(npccountsecond, variable, whichframes,state,x):
    global npcanimatingOnce, platform, pcframes
    platform.after_cancel(animate)
    next_frame = whichframes[npccountsecond]
    platform.itemconfig(variable,image=next_frame)
    npccountsecond += 1
    if npccountsecond == pcframes[state]:
        platform.after_cancel(npcanimatingOnce)
        platform.after(60,npcanimation(npccount,npc,npc_stance[0],"npcidle"))
    elif npccountsecond != pcframes[state]:
        npcanimatingOnce = platform.after(x, lambda: animationOnce(npccountsecond, variable, whichframes, state,x))

# To stop animation
def stopAnimation():
    global animate, platform
    platform.after_cancel(animate)

# Movement of Playable Character
def movement():
    global gamestate
    if gamestate == True:
        global playableChar, platform, events
        animation(count,playableChar,player_stance[0],"idle")
        def moveleft(event):
            if gamestate == True:
                # global playcharacter, platform
                character_coords = platform.bbox(playableChar)
                if character_coords[0] > 0:
                    platform.move(playableChar, -5,0)
                else:
                    pass

        def moveright(event):
            if gamestate == True:
                # global playcharacter, platform
                # animationOnce(countsecond,playableChar,player_stance[4],"run",100)
                character_coords = platform.bbox(playableChar)
                if character_coords[2] < 955:
                    platform.move(playableChar, +5,0)
                else:
                    pass

        def jump(event):
            if gamestate == True:
                character_coords = platform.bbox(playableChar)

                counter = 0
                i = 593 - character_coords[3]
                if i < 0 and character_coords[1] > 450:
                    platform.move(playableChar,0,i)
                elif i > 0 and character_coords[1] > 445:
                    platform.move(playableChar,0,(-i))
                else:
                    pass

                if character_coords[3] == 593 and counter == 0:

                    diff = character_coords[3]
                    yvelocity = -3
                    counter = 1
                    animationOnce(countsecond,playableChar,player_stance[3],"jump",90)
                    while diff >= character_coords[3] and character_coords[3] <= 593 :
                        platform.move(playableChar,0,yvelocity)
                        platform.update()
                        time.sleep(.01)
                        diff -= yvelocity
                        yvelocity += .098
                    yvelocity = 0
                    if character_coords[3] > 593:
                        platform.move(playableChar,0, (593 - character_coords[3]))
                    counter = 0
                else:
                    pass

        def attack1(event):
            if gamestate == True:
                events.append(str(event.char).lower())
                animationOnce(countsecond,playableChar,player_stance[1],"attack1",30)

        def attack2(event):
            if gamestate == True:
                events.append(str(event.char).lower())
                animationOnce(countsecond,playableChar,player_stance[2],"attack2",30)


        main.bind("<KeyPress-Left>", lambda event: moveleft(event))
        main.bind("<KeyPress-Right>", lambda event: moveright(event))
        main.bind("<KeyPress-Up>", lambda event: jump(event))
        main.bind("<z>", lambda event: attack1(event))
        main.bind("<x>", lambda event: attack2(event))

        # If user wishes to play with other set of KeyPress
        main.bind("<a>", lambda event: moveleft(event))
        main.bind("<d>", lambda event: moveright(event))
        main.bind("<w>", lambda event: jump(event))
        main.bind("<j>", lambda event: attack1(event))
        main.bind("<k>", lambda event: attack2(event))

    else:
        platform.after(50,movement)

# Healthbars for characters
def healthbars():
    global plx1,ply1,plx2,ply2
    global npcx1,npcy1,npcx2,npcy2

    platform.create_text(110,58, text="You", font="Arial 12 bold",fill="white",anchor='nw')
    platform.create_rectangle(150,60,354,74, outline="#e3e3e3", width=0.1, tags="playerhealthoutline")
    platform.create_rectangle(plx1,ply1,plx2,ply2,fill="#eb4034", outline='', tags="playerhealth")

    platform.create_text(637,58, text="Enemy", font="Arial 12 bold",fill="white",anchor='nw')
    platform.create_rectangle(700,60,900,74, outline="#e3e3e3",width=0.1, tags="npchealthoutline")
    platform.create_rectangle(npcx1,npcy1,npcx2,npcy2,fill="#eb4034", outline="", tags="npchealth")

# Collision between Characters
def collisionDetection(obj1, obj2):
    global gamestate
    if gamestate == True:
        global npcx1,npcy1,npcx2,npcy2
        global events, score, npc_health, scoreboard, stop, npc_stance
        object_1 = platform.bbox(obj1)
        object_2 = platform.bbox(obj2)
        temp = 300
        if object_2[0] in range(object_1[0], object_1[2]) or object_2[2] in range(object_1[0], object_1[2]):
            if npc_health > 15:
                if events == []:
                    pass

                elif events[0] == "z":
                    events.clear()
                    npcx2 = npcx2 - ((200/temp)*6)
                    main.after(90,platform.delete("npchealth"))
                    if npcx2 == npcx1:
                        platform.create_rectangle(0,npcy1,0,npcy2,fill="#eb4034", outline="", tags="npchealth")
                    elif npcx2>npcx1:
                        platform.create_rectangle(npcx1,npcy1,npcx2,npcy2,fill="#eb4034", outline="", tags="npchealth")
                        score += random.choice(scorelist)
                    platform.itemconfigure(scoreboard, text = f"HIGHSCORE : {score:05d}")
                    npcanimationOnce(npccountsecond,npc,npc_stance[3],"npchit",40)
                    npc_health -= 6

                elif events[0] == "x":
                    events.clear()
                    npcx2 = npcx2 - ((200/temp)*5)
                    main.after(90,platform.delete("npchealth"))
                    if npcx2 == npcx1:
                        platform.create_rectangle(0,npcy1,0,npcy2,fill="#eb4034", outline="", tags="npchealth")
                    elif npcx2>npcx1:
                        platform.create_rectangle(npcx1,npcy1,npcx2,npcy2,fill="#eb4034", outline="", tags="npchealth")
                        score += random.choice(scorelist)
                    platform.itemconfigure(scoreboard, text = f"HIGHSCORE : {score:05d}")
                    npcanimationOnce(npccountsecond,npc,npc_stance[3],"npchit",40)
                    npc_health -= 5
            elif npc_health < 30:
                if events == []:
                    pass
                elif events[0] == "z":
                    events.clear()
                    npcx2 = npcx2 - ((200/temp)*3)
                    main.after(90,platform.delete("npchealth"))
                    if npcx2 == npcx1:
                        platform.create_rectangle(0,npcy1,0,npcy2,fill="#eb4034", outline="", tags="npchealth")
                    elif npcx2>npcx1:
                        platform.create_rectangle(npcx1,npcy1,npcx2,npcy2,fill="#eb4034", outline="", tags="npchealth")
                        score += random.choice(scorelist)
                    platform.itemconfigure(scoreboard, text = f"HIGHSCORE : {score:05d}")
                    npcanimationOnce(npccountsecond,npc,npc_stance[3],"npchit",40)
                    npc_health -= 3

                elif events[0] == "x":
                    events.clear()
                    npcx2 = npcx2 - ((200/temp)*2)
                    main.after(90,platform.delete("npchealth"))
                    if npcx2 == npcx1:
                        platform.create_rectangle(0,npcy1,0,npcy2,fill="#eb4034", outline="", tags="npchealth")
                    elif npcx2>npcx1:
                        platform.create_rectangle(npcx1,npcy1,npcx2,npcy2,fill="#eb4034", outline="", tags="npchealth")
                        score += random.choice(scorelist)
                    platform.itemconfigure(scoreboard, text = f"HIGHSCORE : {score:05d}")
                    npcanimationOnce(npccountsecond,npc,npc_stance[3],"npchit",40)
                    npc_health -= 2
            elif npc_health < 0:
                npc_health = 0



        main.after(100, lambda: collisionDetection(obj1, obj2))
    else:
        platform.after(50, lambda: collisionDetection(obj1, obj2))

# hides the initial FIght Title
def changestate_rounds(txt,arg):
    global platform
    if arg == 0:
        platform.itemconfigure(txt,state="hidden")
    elif arg == 1:
        platform.itemconfigure(txt,state="normal")
    else:
        pass

# Timer for the Fight
def countdowntimer():
    global gamestate
    if gamestate == True:
        global timer, countdownstate, countdown
        if countdown > -1:
            minutes,seconds = divmod(countdown,60)
            platform.itemconfigure(timer, text=f"{minutes:02d}:{seconds:02d}")
            if countdown == 0:
                platform.itemconfigure(timer, text=f"{0:02d}:{0:02d}")
                platform.after_cancel(countdownstate)


        countdown -= 1
        countdownstate = platform.after(1000,countdowntimer)
    else:
        platform.after(50,countdowntimer)

# Setting Direction for NPC
def npcmove(arg):
    global platform, npc
    if arg == 0:
        # step = random.randrange(5,15)
        platform.move(npc,10,0)
    elif arg == 1:
        # step = random.randrange(5,15)
        platform.move(npc,(-10),0)

# Movement of NPC on Conditionals
def npcmovement():
    global gamestate
    if gamestate == True:
        global npc, playableChar, platform, npcmoving, stop, npc_stance, chance, playerhealth
        global plx1,ply1,plx2,ply2
        co_ords = platform.bbox(playableChar)
        npccoords = platform.bbox(npc)
        playHealth = 150
        initialHealth = npc_health
        if npc_health > 0 and playerhealth > 0:
            if npccoords[0] in range(co_ords[0], co_ords[2]) or npccoords[2] in range(co_ords[0],co_ords[2]):
                if playerhealth > 40:
                    chance = random.choice((0,1,2))
                    if chance == 0:
                        pass
                    elif chance == 1:
                        npcanimationOnce(npccountsecond,npc,npc_stance[1],"npcattack1",90)
                        plx2 = plx2 - ((200/playHealth)*4)
                        playerhealth -= 4
                        animationOnce(countsecond,playableChar,player_stance[4],"hit",30)
                        main.after(130,npcmove(0))
                        if plx2 == plx1:
                            platform.coords("playerhealth",0,ply1,0,ply2)
                        elif plx2>plx1:
                            platform.coords("playerhealth",plx1,ply1,plx2,ply2)
                    elif chance == 2:
                        npcanimationOnce(npccountsecond,npc,npc_stance[2],"npcattack2",90)
                        plx2 = plx2 - ((200/playHealth)*3)
                        playerhealth -= 3
                        npcmove(0)
                        animationOnce(countsecond,playableChar,player_stance[4],"hit",30)
                        main.after(130,npcmove(0))
                        if plx2 == plx1:
                            platform.coords("playerhealth",0,ply1,0,ply2)
                        elif plx2>plx1:
                            platform.coords("playerhealth",plx1,ply1,plx2,ply2)
                elif playerhealth < 40:
                    chance = random.choice((0,1,2))
                    if chance == 0:
                        pass
                    elif chance == 1:
                        npcanimationOnce(npccountsecond,npc,npc_stance[1],"npcattack1",90)
                        plx2 = plx2 - ((200/playHealth)*2)
                        playerhealth -= 2
                        animationOnce(countsecond,playableChar,player_stance[4],"hit",30)
                        main.after(130,npcmove(0))
                        if plx2 == plx1:
                            platform.coords("playerhealth",0,ply1,0,ply2)
                        elif plx2>plx1:
                            platform.coords("playerhealth",plx1,ply1,plx2,ply2)
                    elif chance == 2:
                        npcanimationOnce(npccountsecond,npc,npc_stance[2],"npcattack2",90)
                        plx2 = plx2 - ((200/playHealth)*1)
                        playerhealth -= 1
                        animationOnce(countsecond,playableChar,player_stance[4],"hit",30)
                        main.after(130,npcmove(0))
                        if plx2 == plx1:
                            platform.coords("playerhealth",0,ply1,0,ply2)
                        elif plx2>plx1:
                            platform.coords("playerhealth",plx1,ply1,plx2,ply2)
                elif playerhealth < 0:
                    playerhealth = 0
                    platform.coords("playerhealth",0,ply1,0,ply2)
                    stop_npc()

            elif npccoords[0] > co_ords[2] and npccoords[0] > co_ords[0] and npccoords[0] > 0:
                main.after(50,npcmove(1))

            elif co_ords[0] > npccoords[2] or co_ords[2] > npccoords[2] and npccoords[2] < 955:
                main.after(50,npcmove(0))

            if npc_health <  initialHealth:
                main.after(240,npcmove(0))
        elif npc_health == 0:
            platform.coords("npchealth",0,npcy1,0,npcy2)
            stop_npc()
            pass
        npcmoving = platform.after(random.randint(70,500),npcmovement)
    else:
        platform.after(100,npcmovement)

# Stop npc
def stop_npc():
    global npcmoving, stop
    platform.after_cancel(npcmoving)
    platform.after_cancel(stop)

# Saves the progress of game
def savestate():
    global filepath, data, score, countdown, platform, playableChar, npc, npc_health, playerhealth
    filepath = "graphics/save_state.json"
    playercoords = platform.coords(playableChar)
    npccoords = platform.coords(npc)
    npchealth = platform.coords("npchealth")
    playerh = platform.coords("playerhealth")
    data = {"score":score,"time":countdown,"player":playercoords,"npc":npccoords,"playhealth":playerhealth, "npchealth":npc_health,"npcbar":npchealth,"playbar":playerh}
    with open(filepath,"w",encoding="utf-8",) as file:
        json.dump(data,file)

# Loads the Saved State of Game
def loadstate():
    global filepath, score, platform, playableChar, npc, npc_health, playerhealth, loaddata, backdrops, player_stance,scoreboard,timer,npcx1,npcy1,npcx2,npcy2
    global stop, gamestate, count, countsecond, npccount, pcframes, co_ords, npccoords, countdown, npc_stance, backdrop, plx1,ply1,plx2,ply2

    main.after(100,platform.pack_forget())

    filepath = "graphics/save_state.json"
    with open(filepath,encoding="utf-8") as file:
        loaddata = json.load(file)
    score = loaddata["score"]
    countdown = loaddata["time"]
    co_ords = loaddata["player"]
    npccoords = loaddata["npc"]
    playerhealth = loaddata["playhealth"]
    npc_health = loaddata["npchealth"]
    npcbar = loaddata["npcbar"]
    playbar = loaddata["playbar"]

    plx1,ply1,plx2,ply2 = playbar[0],playbar[1],playbar[2],playbar[3]
    npcx1,npcy1,npcx2,npcy2 = npcbar[0],npcbar[1],npcbar[2],npcbar[3]

    gamestate = True
    # Canvas i.e. Main Game screen setup in 4:3 ratio
    platform = tk.Canvas(main, height=720, width=960, bg="black",bd=-2)
    platform.pack()

    #Added a background image
    backdrop = tk.PhotoImage(file=backdrops[1])
    platform.create_image(0,0,image=backdrop,anchor="nw")

    # Loading .gif files and declaring frames
    playablecharacter = {"idle":"graphics/playerIdle.gif","attack1":"graphics/playerAttack1.gif","attack2":"graphics/playerAttack2.gif","jump":"graphics/playerJump.gif","hit":"graphics/playerHit.gif"}
    pcframes = {"idle":8,"attack1":6,"attack2":6,"jump":12,"run":8,"hit":4,"npcidle":10,"npcattack1":6,"npcattack2":7,"npchit":3}

    npcframes = {"idle":"graphics/npcIdle.gif","attack1":"graphics/npcattack1.gif","attack2":"graphics/npcattack2.gif","hit":"graphics/npchit.gif"}

    # Stores all the frames in a list to iterate in animation function
    player_stance = [
        [tk.PhotoImage(file=playablecharacter["idle"], format=f"gif -index {i}") for i in range(pcframes["idle"])],
        [tk.PhotoImage(file=playablecharacter["attack1"], format=f"gif -index {i}") for i in range(pcframes["attack1"])],
        [tk.PhotoImage(file=playablecharacter["attack2"], format=f"gif -index {i}") for i in range(pcframes["attack2"])],
        [tk.PhotoImage(file=playablecharacter["jump"], format=f"gif -index {i}") for i in range(pcframes["jump"])],
        [tk.PhotoImage(file=playablecharacter["hit"], format=f"gif -index {i}") for i in range(pcframes["hit"])]
        ]

    npc_stance = [
        [tk.PhotoImage(file=npcframes["idle"], format=f"gif -index {i}") for i in range(pcframes["npcidle"])],
        [tk.PhotoImage(file=npcframes["attack1"], format=f"gif -index {i}") for i in range(pcframes["npcattack1"])],
        [tk.PhotoImage(file=npcframes["attack2"], format=f"gif -index {i}") for i in range(pcframes["npcattack2"])],
        [tk.PhotoImage(file=npcframes["hit"], format=f"gif -index {i}") for i in range(pcframes["npchit"])]
        ]

    # Loading rectangle for test
    npc = platform.create_image(npccoords[0],npccoords[1],image="",anchor="nw")

    #Playable Character
    playableChar = platform.create_image(co_ords[0],co_ords[1], image="",anchor='nw')

    #Scoreboard
    scoreboard = platform.create_text(45,10, text=f"HIGHSCORE : {score:05d}", font="Arial 18 bold",fill="#bb86fc", anchor='nw')

    #Countdown Timer
    timer = platform.create_text(480,40,text="{0:02d}:{0:02d}", font="Arial 22",fill="white", anchor='center')


    platform.create_text(110,58, text="You", font="Arial 12 bold",fill="white",anchor='nw')
    platform.create_rectangle(150,60,354,74, outline="#e3e3e3", width=0.1, tags="playerhealthoutline")
    platform.create_rectangle(plx1,ply1,plx2,ply2,fill="#eb4034", outline='', tags="playerhealth")

    platform.create_text(637,58, text="Enemy", font="Arial 12 bold",fill="white",anchor='nw')
    platform.create_rectangle(700,60,900,74, outline="#e3e3e3",width=0.1, tags="npchealthoutline")
    platform.create_rectangle(npcx1,npcy1,npcx2,npcy2,fill="#eb4034", outline="", tags="npchealth")

    stop = npcanimation(npccount,npc,npc_stance[0],"npcidle")

    movement()
    npcmovement()
    countdowntimer()
    collisionDetection(playableChar,npc)
    additionalBinds()
    endgame()


# Game Over screen widgets
def endgamemenu():
    global platform, playerhealth, gameend, gamestate, topscores, score, initialstext, initials, gettext, countdown
    gamestate = False
    platform.create_text(480,300,text="Game Over",tags="Gameover",anchor="center",fill="#ff3b3b",font="Arial 80 bold")
    initials = tk.Entry(platform, width=30,bd=-2,relief="flat")
    initials.insert(0,"Enter your initials")
    initials.focus()
    initials.pack()
    initials.bind("<Button-1>",initials.delete(0,"end"))
    platform.create_window(480, 400, window=initials,anchor="center",height=30)
    initialsbutton = tk.Button(platform,text="Enter Your Initials", font="Arial 12",activebackground="#32a852",activeforeground="white",disabledforeground="white",bg="#e81d45",fg="white",bd=-2,relief="flat",command=endgametolb)
    platform.create_window(650,400,window=initialsbutton,anchor='center',height=30)

# Game OVer Screen
def endgame():
    global platform2, playerhealth, gameend, gamestate, topscores, score, initialstext, initials, gettext, countdown
    if playerhealth == 0 or playerhealth < 0:
        endgamemenu()

    elif countdown == 0:
        endgamemenu()
    else:
        main.after(1000,endgame)
        pass

# Directs to leaderboard after Gameover
def endgametolb():
    global topscores, initialstext, score, initials, gettext
    gettext = initials.get()
    text = gettext[:3]
    topscores.append([text,score])
    checkleaderboard()
    try:
        main.after_cancel(lambda event: maincanvas(event))
    except:
        main.after_cancel(loadstate)

    platform.destroy()
    platform.forget()
    leaderboardcanvas()

# Increase time by 50 seconds
def cheats1(event):
    if gamestate == True:
        global countdown
        countdown += 50
    else:
        pass

# Infinite Health
def cheats2(event):
    if gamestate == True:
        global playerhealth,platform
        playerhealth += 150
        platform.coords("playerhealth",152,62,353,73)

def pause(event):
    global gamestate, pauseCount, events
    pausemenu()
    pauseCount += 1
    if gamestate == True and pauseCount == 1:
        gamestate = False
        platform.itemconfigure("pauseText",state="normal")
        platform.itemconfigure("BacktoMenu",state="normal")
        platform.itemconfigure("SaveState",state="normal")
        events.append(str(event.char).lower())
    elif gamestate == False and pauseCount == 2:
        gamestate = True
        platform.itemconfigure("pauseText",state="hidden")
        platform.itemconfigure("BacktoMenu",state="hidden")
        platform.itemconfigure("SaveState",state="hidden")
        pauseCount = 0
        events.clear()
    main.after(100,additionalBinds)

def pausemenu():
    pausetext = platform.create_text(480,250,text="Press P to Resume", font="Arial 16",fill="white", state="hidden",tags="pauseText")

    backtomenu = tk.Button(platform,text="Quit Game", font="Arial 12",activebackground="#32a852",activeforeground="white",bg="#e81d45",fg="white",bd=-2,relief="flat",command=quitgame)
    savegame = tk.Button(platform, text="Save Game",font="Arial 12",activebackground="#32a852",activeforeground="white",bg="#e81d45",fg="white",bd=-2,relief="flat",command=savestate)

    backtomenuButton = platform.create_window(400, 300,window=backtomenu,tags="BacktoMenu",anchor='center',state="hidden",width=90,height=30)
    savegameButton = platform.create_window(560,300,window=savegame,tags="SaveState",anchor='center',state="hidden",width=90,height=30)

# Some Additional keybinds
def additionalBinds():
    main.bind("<p>", lambda event: pause(event))
    main.bind("<b>", lambda event: bosskey(event))
    main.bind("<i>", lambda event: cheats2(event))
    main.bind("<o>", lambda event: cheats1(event))

# # Complexity in Game
def round2():
    global gamestate, coundown, npc_health
    if gamestate == True:
        if npc_health == 0 and countdown != 0:
            global platform, npcframes, npc, playableChar, scoreboard, timer, player_stance, pcframes, backdrop, stop, npc_stance, score
            main.after(1000,platform.pack_forget())
            loaddefaults(0)
            countdown = 300
            npc_health = 500
            scorelist = [100,50,60,70,80]
            npc = platform.create_image(defaultx_npc,defaulty_npc,image="",anchor="nw")

            #Playable Character
            playableChar = platform.create_image(defaultx_pc,defaulty_pc, image="",anchor='nw')

            #Scoreboard
            scoreboard = platform.create_text(45,10, text=f"HIGHSCORE : {score:05d}", font="Arial 18 bold",fill="#bb86fc", anchor='nw')

            #Countdown Timer
            timer = platform.create_text(480,40,text="{0:02d}:{0:02d}", font="Arial 22",fill="white", anchor='center')

            stop = npcanimation(npccount,npc,npc_stance[0],"npcidle")
            healthbars()
            countdowntimer()
            movement()
            npcmovement()
            collisionDetection(playableChar,npc)
            endgame()
            roundtext = platform.create_text(480,340, text=f"Fight", font="Arial 60 bold",fill="#f7ffe8", justify="center",state="hidden",anchor="center")
            platform.after(1000, lambda: changestate_rounds(roundtext,1))
            platform.after(3000, lambda: changestate_rounds(roundtext,0))
            additionalBinds()
        else:
            pass
        main.after(100,round2)

# Return to main menu
def quitgame():
    global platform, animate
    main.after_cancel(lambda event: maincanvas(event))
    platform.destroy()
    platform.forget()
    menucanvas()

# Text animation
def blinkingtext():
    platform.itemconfigure("LoadText",state="normal")
    platform.after(1000,blinkingtextsecond)

def blinkingtextsecond():
    platform.itemconfigure("LoadText",state="hidden")
    platform.after(1000,blinkingtext)

# bosskey
def bosskey(event):
    global platform, bossCount, gamestate, bosskey_image, boss_canvas, label, events
    bossCount += 1
    if bossCount == 1:
        gamestate = False
        bosskey_image = tk.PhotoImage(file="graphics/bosskey2.png")
        label = tk.Label(platform,image=bosskey_image,anchor='nw')
        label.pack()
        main.wm_iconphoto(False,tk.PhotoImage(file="graphics/icon2.png"))
        main.title("Week 09 (starting Nov 22) – COMP16321 Introduction to ...")

    elif bossCount == 2 and "p" in events:
        bossCount = 0
        label.pack_forget()
        platform.config(width=960,height=720,bd=-2,bg="black")
        platform.pack()
        main.title("Octagram")
        main.wm_iconphoto(False,tk.PhotoImage(file="graphics/icon.png"))

    elif bossCount == 2:
        bossCount = 0
        gamestate = True
        label.pack_forget()
        platform.config(width=960,height=720,bd=-2,bg="black")
        platform.pack()
        main.title("Octagram")
        main.wm_iconphoto(False,tk.PhotoImage(file="graphics/icon.png"))

# menu
def menucanvas():
    global platform, backdrop, titletext
    if platform != None:
        platform.forget()
    else:
        pass
    platform = tk.Canvas(main, height=720, width=960, bg="black",bd=-2)
    platform.pack()

    backdrop = tk.PhotoImage(file=backdrops[2])
    platform.create_image(0,0,image=backdrop,anchor='nw')

    titletext = tk.PhotoImage(file=backdrops[3])
    platform.create_image(480,230,image=titletext,anchor="center")

    startgame = tk.Button(platform,text="New Game", font="Arial 20",activebackground="#720551",activeforeground="white",bg="#e81d45",fg="white",bd=-2,relief="flat",command=loadscreencanvas)
    startgameButton = platform.create_window(480, 360, window=startgame,tags="MenuButton",anchor="center",width=157,height=40)

    loadgame = tk.Button(platform,text="Load Game", font="Arial 20",activebackground="#720551",activeforeground="white",bg="#e81d45",fg="white",bd=-2,relief="flat",command=loadstate)
    loadgameButton = platform.create_window(480, 420, window=loadgame,tags="MenuButton",anchor="center",width=157,height=40)

    leaderboard = tk.Button(platform,text="Leaderboard", font="Arial 20",activebackground="#720551",activeforeground="white",bg="#e81d45",fg="white",bd=-2,relief="flat",command=leaderboardcanvas)
    leaderboardButton = platform.create_window(480, 480, window=leaderboard,tags="MenuButton",anchor="center",width=157,height=40)

# loadingscreen
def loadscreencanvas():
    global platform, instruction, backdrops
    platform.pack_forget()

    platform = tk.Canvas(main, height=720, width=960, bg="black",bd=-2)
    platform.pack()

    platform.create_rectangle(280,160,680,400,width=4,fill="#00031a",outline="#e81d45",tags="LoadScreen")

    instruction = tk.PhotoImage(file=backdrops[4])
    platform.create_image(480,280, image=instruction, anchor='center', tags="LoadScreen")

    platform.create_text(480,680,text="Press Enter to Start",fill="white",font="20",tags=("LoadScreen","LoadText"),state="hidden")
    platform.after(2500,blinkingtext)

    backtomenu = tk.Button(platform,text="Back", font="Arial 18",activebackground="#fc563a",activeforeground="white",bg="#e78b3c",fg="white",bd=-2,relief="flat",command=menucanvas)
    backtomainmenuButton = platform.create_window(100, 70, window=backtomenu,tags="ScoreScreen",anchor="center",width=80,height=25)

    main.bind("<Return>",lambda event: maincanvas(event))

# leaderboardscreen
def leaderboardcanvas():
    global platform, backdrops, leaderboard, sortedtopscores
    platform.pack_forget()

    platform = tk.Canvas(main, height=720, width=960, bg="black",bd=-2)
    platform.pack()
    sortedtopscores = readleaderboard()

    leaderboard = tk.PhotoImage(file=backdrops[5])
    platform.create_image(440,50, image=leaderboard, anchor='center', tags="ScoreScreen")
    platform.create_text(300,200, text=f"1        {sortedtopscores[0][0].upper()}        {sortedtopscores[0][1]:05d}",font="Arial 20 ",fill="white",anchor="nw")
    platform.create_text(300,250, text=f"2        {sortedtopscores[1][0].upper()}        {sortedtopscores[1][1]:05d}",font="Arial 20 ",fill="white",anchor="nw")
    platform.create_text(300,300, text=f"3        {sortedtopscores[2][0].upper()}        {sortedtopscores[2][1]:05d}",font="Arial 20 ",fill="white",anchor="nw")
    platform.create_text(300,350, text=f"4        {sortedtopscores[3][0].upper()}        {sortedtopscores[3][1]:05d}",font="Arial 20 ",fill="white",anchor="nw")
    platform.create_text(300,400, text=f"5        {sortedtopscores[4][0].upper()}        {sortedtopscores[4][1]:05d}",font="Arial 20 ",fill="white",anchor="nw")

    backtomenu = tk.Button(platform,text="Back", font="Arial 18",activebackground="#fc563a",activeforeground="white",bg="#e78b3c",fg="white",bd=-2,relief="flat",command=menucanvas)
    backtomainmenuButton = platform.create_window(100, 650, window=backtomenu,tags="ScoreScreen",anchor="center",width=80,height=25)

# maingame screen
def maincanvas(event):
    global platform, npcframes, npc, playableChar, scoreboard, timer, player_stance, pcframes, backdrop, stop, countdown, gamestate, npc_stance
    main.after(1000,platform.pack_forget())
    main.unbind("<Return>")
    countdown = 90
    gamestate = True
    # Canvas i.e. Main Game screen setup in 4:3 ratio
    platform = tk.Canvas(main, height=720, width=960, bg="black",bd=-2)
    platform.pack()

    #Added a background image
    backdrop = tk.PhotoImage(file=backdrops[1])
    platform.create_image(0,0,image=backdrop,anchor="nw")

    # Loading .gif files and declaring frames
    playablecharacter = {"idle":"graphics/playerIdle.gif","attack1":"graphics/playerAttack1.gif","attack2":"graphics/playerAttack2.gif","jump":"graphics/playerJump.gif","hit":"graphics/playerHit.gif"}
    pcframes = {"idle":8,"attack1":6,"attack2":6,"jump":12,"run":8,"hit":4,"npcidle":10,"npcattack1":6,"npcattack2":7,"npchit":3}

    npcframes = {"idle":"graphics/npcIdle.gif","attack1":"graphics/npcattack1.gif","attack2":"graphics/npcattack2.gif","hit":"graphics/npchit.gif"}

    # Stores all the frames in a list to iterate in animation function
    player_stance = [
        [tk.PhotoImage(file=playablecharacter["idle"], format=f"gif -index {i}") for i in range(pcframes["idle"])],
        [tk.PhotoImage(file=playablecharacter["attack1"], format=f"gif -index {i}") for i in range(pcframes["attack1"])],
        [tk.PhotoImage(file=playablecharacter["attack2"], format=f"gif -index {i}") for i in range(pcframes["attack2"])],
        [tk.PhotoImage(file=playablecharacter["jump"], format=f"gif -index {i}") for i in range(pcframes["jump"])],
        [tk.PhotoImage(file=playablecharacter["hit"], format=f"gif -index {i}") for i in range(pcframes["hit"])]
        ]

    npc_stance = [
        [tk.PhotoImage(file=npcframes["idle"], format=f"gif -index {i}") for i in range(pcframes["npcidle"])],
        [tk.PhotoImage(file=npcframes["attack1"], format=f"gif -index {i}") for i in range(pcframes["npcattack1"])],
        [tk.PhotoImage(file=npcframes["attack2"], format=f"gif -index {i}") for i in range(pcframes["npcattack2"])],
        [tk.PhotoImage(file=npcframes["hit"], format=f"gif -index {i}") for i in range(pcframes["npchit"])]
        ]

    # Loading rectangle for test
    npc = platform.create_image(defaultx_npc,defaulty_npc,image="",anchor="nw")

    #Playable Character
    playableChar = platform.create_image(defaultx_pc,defaulty_pc, image="",anchor='nw')

    #Scoreboard
    scoreboard = platform.create_text(45,10, text=f"HIGHSCORE : {score:05d}", font="Arial 18 bold",fill="#bb86fc", anchor='nw')

    #Countdown Timer
    timer = platform.create_text(480,40,text="{0:02d}:{0:02d}", font="Arial 22",fill="white", anchor='center')

    stop = npcanimation(npccount,npc,npc_stance[0],"npcidle")
    loaddefaults(1)
    healthbars()
    countdowntimer()
    movement()
    npcmovement()
    collisionDetection(playableChar,npc)
    endgame()
    roundtext = platform.create_text(480,340, text=f"Fight", font="Arial 60 bold",fill="#f7ffe8", justify="center",state="hidden",anchor="center")
    platform.after(1000, lambda: changestate_rounds(roundtext,1))
    platform.after(3000, lambda: changestate_rounds(roundtext,0))
    additionalBinds()



gamescreengenerate()
menucanvas()

main.mainloop()
