import random
import time
from collections import deque
from pynput import keyboard
from os import system


SYMBOLS = ["【𝕏】", "【𝔹】", "【ℚ】", "【𝕂】", "【𝔸】", "【7】", "【$】"]


VALUES = {
    "【𝕏】" : 0.5,
    "【𝔹】" : 0.5,
    "【ℚ】" : 2,
    "【𝕂】" : 2,
    "【𝔸】" : 5,
    "【7】" : 10,
    "【$】" : 20
}
LOGO = "₮ Ⱨ Ɇ ~҉~҉~ ₲ ₳ ₥ ฿ Ⱡ Ɇ Ɽ"
HEIGHT = 8
WIDTH = 30
screenLines = deque(deque([],WIDTH), HEIGHT)
money = 1000
bet = 100

WINLOW = bet * 2
WINHIGH = bet * 10
JACKPOT = bet * 100
BONUS = bet * 2
ROWS, WHEELS = (3, 3)
LINEMULTIPLIER = 10

result = []
wheelCount = 3
current = []
canPressKey = False
pressedSpace = False
hasWon = False
didQuit = False
lastWin = 0
fps = 1/60

wheelDisplay = []

## function to control keys-pressed

def on_release(key):
    global didQuit
    global pressedSpace
    global canPressKey

    if canPressKey and key == keyboard.Key.space:
        pressedSpace = True
        canPressKey = False
    
    if canPressKey and key == key == keyboard.Key.esc:
        didQuit = True

def screenRenderer(wheelDisplay):
    system('clear')
    print("\t" + str(LOGO))
    print("▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
    print("▒                                      ▒")
    for w in range(WHEELS):
        for r in range(ROWS):
            print("\t" + wheelDisplay[r][w], end=" ")
        print("")    
    print("▒                                      ▒")
    print("▒Money: " + str(money) + "      Last win: ", str(lastWin)+ "        ▒")
    print("▒Bet: " + str(bet) + "   SPIN  BET  AUTO            ▒")
    print("▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")

def calculateActualSpinResult():
    ## the actual spin result is calculated once,
    ## the rest is just for show

    ##creating structur of the queue
    spinResult = deque(deque([], ROWS) for i in range(WHEELS))
    ## creating a pool of symbols to fill
    inflatedSymbolPool = createSymbolPool(SYMBOLS)
    # Populate the sublists with unique elements
    for wheel in spinResult:
        while len(wheel) < ROWS:
            uniqueSymbol = random.choice(inflatedSymbolPool)
            if uniqueSymbol not in wheel:
                wheel.appendleft(uniqueSymbol)
    return spinResult
## function to show a spin animation

def wheelSpinAnimation(wheelDisplay):
    global SYMBOLS
    wheelsStopped = 0
    
    ## the actual spin result is calculated once,
    ## the rest is just for show

    ##creating structur of the queue
    spinResult = calculateActualSpinResult()

    ## creating a pool of symbols to fill

    while wheelsStopped < WHEELS:
        x = 0
        while x < random.randrange(10, 50):
            for w in range(WHEELS - wheelsStopped):
                    w += wheelsStopped
                    wheelDisplay[w].appendleft(random.choice(SYMBOLS))
            time.sleep(0.05)
            x += 1
            if wheelsStopped == 1:
                    wheelDisplay[0] = spinResult[0]
            if wheelsStopped == 2:
                    wheelDisplay[1] = spinResult[1]
            if wheelsStopped == 3:
                    wheelDisplay[2] = spinResult[2]
            screenRenderer(wheelDisplay)

        wheelsStopped += 1

# Function to show a win or lose animation after each spin
def endScreenAnimation(wheelDisplay):
    global hasWon
    global money
    global lastWin
    winAmount = calculateWin(winDetector(wheelDisplay))
    lastWin = winAmount
    moneyOld = money

    if hasWon:
        x = 0
        storage = []
        while x < 5:

            for w in range(WHEELS):
                storage.append(wheelDisplay[w][1])
                lastWin = "       "
                wheelDisplay[w][1] = "- -"

            screenRenderer(wheelDisplay)
            time.sleep(fps)

            for w in range(WHEELS):
                storage.append(wheelDisplay[w][1])
                lastWin = winAmount
                wheelDisplay[w][1] = " - "


            screenRenderer(wheelDisplay)
            time.sleep(fps)

            for w in range(WHEELS):
                storage.append(wheelDisplay[w][1])
                wheelDisplay[w][1] = " | "
                lastWin = "       "

            screenRenderer(wheelDisplay)
            time.sleep(fps)            

            for w in range(WHEELS):
                wheelDisplay[w][1] = storage[w]
            lastWin = winAmount

            screenRenderer(wheelDisplay)
            time.sleep(fps*10)

            x += 1
        for w in range(WHEELS):
            wheelDisplay[w][1] = storage[w]

        while money < moneyOld + winAmount:
            money += 10
            time.sleep(fps/10)
            screenRenderer(wheelDisplay)

## function to inflate the symbol pool
def createSymbolPool(symbolPool):
    x = 0
    while x < 1:
        symbolSource = SYMBOLS
        symbolSource.reverse()
        symbolPool = []
        
        for symbol in symbolSource:
            position = symbolSource.index(symbol) + 1

            for counter in range(position):
                symbolPool.append(symbol)
        x += 1
    return symbolPool

## function to calculate the result of the spin
def calculateWin(win):
    global hasWon
    winAmount = 0
    if win[0] > 0:
        win[1] = VALUES[win[1]]
        if win[0] == 3:
            winAmount = bet * (win[1] * LINEMULTIPLIER)
            hasWon = True
            return winAmount
        
        elif win[0] == 2:
            winAmount = bet * win[1]
            hasWon = True
            return winAmount

## function to check for symbols in one line
def winDetector(result):
    global money
    lineResult = []

    collector = []

    # create a list of the symbols from all wheels
    # on the second row.
    for w in range(WHEELS):
        collector.append(result[w][1])
    

    if collector[0] == collector[1] and collector[1] == collector[2]:
        lineResult.append(collector.count(collector[0]))    
        lineResult.append(collector[0])
    elif collector[0] == collector[1]:
        lineResult.append(collector.count(collector[0]))    
        lineResult.append(collector[0])
    else:
         lineResult.append(0)
         lineResult.append(0)
    return lineResult

#######################################
################ START ################
#######################################

listener = keyboard.Listener(on_release = on_release)
listener.start()

## filling wheels with symbols, 
## using 2 dimensional list and deque
for i in range(WHEELS):
    wheelDisplay.append(deque([random.choice(SYMBOLS) for i in range(WHEELS)], 3))

system('clear')
while not didQuit:
    screenRenderer(wheelDisplay)
    canPressKey = True
    if pressedSpace:
        canPressKey = False
        money -= bet
        wheelSpinAnimation(wheelDisplay)
        endScreenAnimation(wheelDisplay)
        pressedSpace = False
        hasWon = False
    
        

    time.sleep(0.1)
quit()