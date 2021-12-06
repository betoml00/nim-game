import pygame
import array
import random
pygame.init()

boardColor = (0, 200, 0)
selectedColor = (200, 0, 0)
overColor = (0, 255, 0)
overSelectedColor = (255, 0, 0)
bgColor = (255, 255, 255)

win = pygame.display.set_mode((700, 500))
win.fill(bgColor)
simpleBoard = {}
areSelected = {}
isOver = {}
tienenAnimacion = {}

class button():
    def __init__(self, color, x, y, width, height, text='', textColor = (0, 0, 0)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColor = textColor

    def draw(self, win, outline = None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('centurygothic', 20)
            text = font.render(self.text, 1, self.textColor)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2) ) )

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

addElementsBtn = button((255, 255, 255), (350 + 25/2), 325, 25, 50, '+')
substractElementsBtn = button((255, 255, 255), (350 - 25/2 - 25), 325, 25, 50, '-')
playBtn = button((90, 90, 90), (350 - 75), (250 - 25), 150, 50, 'Play', (255, 255, 255))

startGame = False
cantidadDeMontones = 3

delFont = pygame.font.SysFont('centurygothic', 20)
montonesText = delFont.render('Seleccione la cantidad de niveles:', 1, (0, 0, 0))
win.blit(montonesText, (350 - 25/2 - montonesText.get_width()/2, 300 ))
while startGame == False:
    addElementsBtn.draw(win)
    substractElementsBtn.draw(win)
    playBtn.draw(win)
    pygame.draw.rect(win, (255, 255, 255), (350 - 25/2, 325, 25, 50), 0)    
    delText = delFont.render(str(cantidadDeMontones), 1, (0,0,0))
    win.blit(delText, (350 - 25/2 + (25/2 - delText.get_width()/2), 325 + (50/2 - delText.get_height()/2) ))
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
                    
        if event.type == pygame.QUIT:                    
            okay = True
            gameIsGoingOn = False
                        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if addElementsBtn.isOver(pos) and cantidadDeMontones < 6:
                cantidadDeMontones += 1
            if substractElementsBtn.isOver(pos) and cantidadDeMontones > 3:
                cantidadDeMontones -= 1
            if playBtn.isOver(pos):
                startGame = True
                            
        if event.type == pygame.MOUSEMOTION:
            if addElementsBtn.isOver(pos):
                addElementsBtn.color = (211, 211, 211)
            else:
                addElementsBtn.color = (255, 255, 255)
            if substractElementsBtn.isOver(pos):
                substractElementsBtn.color = (211, 211, 211)
            else:
                substractElementsBtn.color = (255, 255, 255)
            if playBtn.isOver(pos):
                playBtn.color = (190, 190, 190)
            else:
                playBtn.color = (90, 90, 90)  

#win.get_width()
finishMove = button((90, 90, 90), (525), 5, 150, 50, 'Terminar turno', (255, 255, 255))
restart = button((235, 20, 20), (525), 65, 150, 50, 'Restart', (255, 255, 255))

class board():
    def __init__(self, rows):
        self.rows = rows
        for i in range(self.rows):
            for j in range((self.rows * 2) + 1):
                simpleBoard[i, j] = 0
                areSelected[i, j] = 0
                isOver[i, j] = 0

    def drawGameBoard(self, win, cantidadDeMontones, animationColor):
        xTempo = 5
        yTempo = 5
        for i in range(cantidadDeMontones):
            xTempo = 5
            for j in range((cantidadDeMontones * 2) + 1):
                if tienenAnimacion[i, j] == 1:
                    pygame.draw.rect(win, animationColor, (xTempo, yTempo, 25, 50),0)                    
                else:
                    if simpleBoard[i, j] == 0:
                        pygame.draw.rect(win, bgColor, (xTempo, yTempo, 25, 50),0)
                    else:                       
                        if areSelected[i, j] == 1:
                            if isOver[i, j] == 1:
                                pygame.draw.rect(win, overSelectedColor, (xTempo, yTempo, 25, 50),0)
                            else:
                                pygame.draw.rect(win, selectedColor, (xTempo, yTempo, 25, 50),0)
                        else:
                            if isOver[i, j] == 1:
                                pygame.draw.rect(win, overColor, (xTempo, yTempo, 25, 50),0)
                            else:
                                pygame.draw.rect(win, boardColor, (xTempo, yTempo, 25, 50),0)
                xTempo += 30
            yTempo += 55

gameBoard = board(cantidadDeMontones)

def redrawWindow(win, animationColor):
    win.fill(bgColor)
    gameBoard.drawGameBoard(win, cantidadDeMontones, animationColor)

    finishMove.draw(win)
    restart.draw(win)

def mouseOverBoard(pos):
    if pos[1] >= 5 and pos[1] <= (cantidadDeMontones * 55):
        if pos[0] >= 5 and pos[0] <= ((cantidadDeMontones * 2) + 2)*30:
            return True
        else:
            return False
    else:
        return False

def whichIsItOver(pos):
    mouseIsOver = [0, 0]
    tempoi = 0
    for i in range(5, ((cantidadDeMontones * 2) + 1)*30, 30):
        tempoj = 0
        for j in range(5, cantidadDeMontones * 55, 55):
            if pos[0] >= i and pos[0] < (i + 30):
                if pos[1] >= j and pos[1] < (j + 55):
                    mouseIsOver[1] = tempoi
                    mouseIsOver[0] = tempoj
            tempoj += 1
        tempoi += 1

    return mouseIsOver

def intToBin(a):
    b = [0, 0, 0, 0, 0]
    count = [1, 1, 1, 1, 1]
    tempoSum = 0
    index = 0

    while a != tempoSum:
        tempoSum = 0
        for i in range(5):
            index = 4 - i
            if count[index] == (2**i):
                count[index] = 1
                if b[index] == 0:
                    b[index] = 1
                else:
                    b[index] = 0
            else:
                count[index] = count[index] + 1

        for i in range(5):
            index = 4 - i
            tempoSum += (2**i)*b[index]


    return b
#__________________________________________________________________________
def sumaNIM(elementosMontonBin, cantidadDeMontones):
    aSum = [0, 0, 0, 0, 0]
    normalSum = 0

    for i in range(5):
        for j in range(cantidadDeMontones):
            normalSum += elementosMontonBin[j][i]
        aSum[i] = normalSum % 2
        normalSum = 0

    return aSum

#__________________________________________________________________________
def escoger(elementosMontonBin, elementosMonton, cantidadDeMontones):
    borrar = [0, 0]
    count = 0
    nimSumIsZero = True
    nimSum = sumaNIM(elementosMontonBin, cantidadDeMontones)

    for i in range(cantidadDeMontones):
        if elementosMonton[i] != 0:
            count += 1

    for i in range(5):
        if nimSum[i] != 0:
            nimSumIsZero = False

    if count > 2:
        if nimSumIsZero == False:
            columnaTempo = 0

            for i in range(4, -1, -1):
                if nimSum[i] == 1:
                    columnaTempo = i

            for i in range(cantidadDeMontones):
                if elementosMontonBin[i][columnaTempo] == 1:
                    borrar[0] = i + 1

            filaMod = array.array('i', [0, 0, 0, 0, 0])
            filaMod = elementosMontonBin[borrar[0] - 1]

            for i in range(5):
                if nimSum[i] == 1:
                    if filaMod[i] == 0:
                        filaMod[i] = 1
                    else:
                        filaMod[i] = 0

            index = 0
            suma = 0
            for i in range(5):
                index = 4 - i
                suma += (2**i)*filaMod[index]

            borrar[1] = elementosMonton[borrar[0] - 1] - suma
        else:
            validRow = False
            randomRow = 0
            randomQuantity = 0

            while validRow == False:
                randomRow = random.randint(0, cantidadDeMontones - 1)                
                if elementosMonton[randomRow] != 0:
                    if elementosMonton[randomRow] == 1:
                        randomQuantity = 1
                    else:
                        randomQuantity = random.randint(1, elementosMonton[randomRow])

                    validRow = True
            borrar[0] = randomRow + 1
            borrar[1] = randomQuantity

    elif count == 1:
        for i in range(cantidadDeMontones):
            if elementosMonton[i] > 1:
                borrar[0] = i + 1
                borrar[1] = elementosMonton[i] - 1
            elif elementosMonton[i] == 1:
                borrar[0] = i + 1
                borrar[1] = 1

    else:
        if nimSumIsZero:
            for i in range(cantidadDeMontones):
                if elementosMonton[i] != 0:
                    borrar[0] = i + 1
            borrar[1] = 1
        else:
            thereIsOne = False
            for i in range(cantidadDeMontones):
                if elementosMonton[i] == 1:
                    thereIsOne = True

            if thereIsOne:
                for i in range(cantidadDeMontones):
                    if elementosMonton[i] > 1:
                        borrar[0] = i + 1
                        borrar[1] = elementosMonton[i]
            else:
                rowOneSize = 0
                rowTwoSize = 0
                rowOneIndex = 0
                rowTwoIndex = 0

                for i in range(cantidadDeMontones):
                    if elementosMonton[i] != 0:
                        if rowOneSize == 0:
                            rowOneSize = elementosMonton[i]
                            rowOneIndex = i
                        else:
                            rowTwoSize = elementosMonton[i]
                            rowTwoIndex = i

                if rowOneSize > rowTwoSize:
                    borrar[0] = rowOneIndex + 1
                    borrar[1] = rowOneSize - rowTwoSize
                else:
                    borrar[0] = rowTwoIndex + 1
                    borrar[1] = rowTwoSize - rowOneSize

    filasConUno = 0
    filasConMas = 0
    filaQueTieneMas = 0

    for i in range(cantidadDeMontones):
        if elementosMonton[i] == 1:
            filasConUno += 1

        if elementosMonton[i] > 1:
            filasConMas += 1
            filaQueTieneMas = i

    if filasConUno >= 1 and filasConMas == 1:
        if count % 2 == 0:
            borrar[1] = elementosMonton[filaQueTieneMas]
            borrar[0] = filaQueTieneMas + 1
        else:
            borrar[1] = elementosMonton[filaQueTieneMas] - 1
            borrar[0] = filaQueTieneMas + 1

    return borrar



#_____________________________________________________________________________________________________
elementosMontonBin = [[], [], [], [], [], []]
elementosMonton = []
def main():
    gameIsGoingOn = True
    while gameIsGoingOn:        
        
        gameEnded = False
        for i in range(cantidadDeMontones):
            for j in range((cantidadDeMontones * 2) + 1):
                simpleBoard[i, j] = 0
                areSelected[i, j] = 0
                isOver[i, j] = 0
                tienenAnimacion[i, j] = 0

        variableRandom = 3
        yPos = 0
        for i in range(cantidadDeMontones):
            xIndexTempo = cantidadDeMontones - (1 + i)
            for j in range(variableRandom):
                simpleBoard[yPos, xIndexTempo] = 1
                xIndexTempo += 1
            variableRandom += 2
            yPos += 1

        run = True
        rowSelected = [False, 0]

        computersTurn = False #preguntar al usuario
        animacion = False
        animationColor = (255, 0, 0)
        colorAnimacion = 0
        while run:
            elementosMonton = []
            for i in range(cantidadDeMontones):
                activeCount = 0
                for j in range((cantidadDeMontones * 2) + 1):
                    if simpleBoard[i, j] == 1:
                        activeCount += 1
                elementosMonton.append(activeCount)
                elementosMontonBin[i] = intToBin(elementosMonton[i])

            redrawWindow(win, animationColor)
            pygame.display.update()

            if animacion:
                if colorAnimacion < 254:
                    #if computersTurn == False:
                        #pygame.time.delay(1)
                    colorAnimacion += 2
                    animationColor = (255, colorAnimacion, colorAnimacion)
                    pygame.time.delay(1)
                else:
                    for i in range(cantidadDeMontones):
                        for j in range((cantidadDeMontones * 2) + 1):                        
                            tienenAnimacion[i, j] = 0
                            areSelected[i, j] = 0
                    animacion = False
                    colorAnimacion = 0
            
            if computersTurn and animacion == False:
                #pygame.time.delay(500)
                decision = escoger(elementosMontonBin, elementosMonton, cantidadDeMontones)                
                xt = 0                
                for j in range((cantidadDeMontones * 2) + 1):
                    if simpleBoard[decision[0] - 1 , j] == 1 and xt < decision[1]:
                        simpleBoard[decision[0] - 1 , j] = 0
                        tienenAnimacion[decision[0] - 1, j] = 1                        
                        xt += 1
                animacion = True
                computersTurn = False
            
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                    gameIsGoingOn = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouseOverBoard(pos):
                        selectedItem = whichIsItOver(pos)
                        if simpleBoard[selectedItem[0], selectedItem[1]] == 1:
                            if rowSelected[0] == False:
                                if areSelected[selectedItem[0], selectedItem[1]] == 0:
                                    areSelected[selectedItem[0], selectedItem[1]] = 1
                                else:
                                    areSelected[selectedItem[0], selectedItem[1]] = 0                                
                                rowSelected[0] = True
                                rowSelected[1] = selectedItem[0]
                            elif rowSelected[1] == selectedItem[0]:
                                if areSelected[selectedItem[0], selectedItem[1]] == 0:
                                    areSelected[selectedItem[0], selectedItem[1]] = 1
                                else:
                                    areSelected[selectedItem[0], selectedItem[1]] = 0

                                selectedSum = 0
                                for i in range((cantidadDeMontones * 2) + 1):
                                    selectedSum += areSelected[selectedItem[0], i]
                                if selectedSum == 0:
                                    rowSelected = [False, 0]                                

                    selectedSum = 0
                    if finishMove.isOver(pos):
                        for i in range(cantidadDeMontones):
                            for j in range((cantidadDeMontones * 2) + 1):                                
                                if areSelected[i, j] == 1:
                                    simpleBoard[i, j] = 0
                                    selectedSum += 1
                                    tienenAnimacion[i, j] = 1                                    
                        if selectedSum > 0:
                            computersTurn = True
                            animacion = True
                            rowSelected = [False, 0]

                    if restart.isOver(pos):
                        run = False


                if event.type == pygame.MOUSEMOTION:
                    for i in range(cantidadDeMontones):
                        for j in range((cantidadDeMontones * 2) + 1):
                            isOver[i, j] = 0
                    if mouseOverBoard(pos):
                        overItem = whichIsItOver(pos)
                        isOver[overItem[0], overItem[1]] = 1

                    if finishMove.isOver(pos):
                        finishMove.color = (190, 190, 190)
                    else:
                        finishMove.color = (90, 90, 90)

                    if restart.isOver(pos):
                        restart.color = (255, 130, 130)
                    else:
                        restart.color = (235, 20, 20)

            sumaMontones = 0
            for i in range(cantidadDeMontones):
                for j in range((cantidadDeMontones * 2) + 1):
                    sumaMontones += simpleBoard[i, j]

            if sumaMontones == 0:
                run = False
                gameEnded = True

        if gameEnded:
            okay = False
            if computersTurn == True:
                text = '¡Gana Betito! Mejor suerte para la próxima.'
            else:
                text = '¡Felicidades! ¡Ganaste!'
                
            resultBtn = button((90, 90, 90), 25, 165, (win.get_width() - 50), 50, text, (255, 255, 255))
            playAgainBtn = button((235, 20, 20), 250, 225, 200, 50, 'Jugar de nuevo', (255, 255, 255))
            while okay == False:                        
                win.fill((255, 255, 255))
                resultBtn.draw(win)
                playAgainBtn.draw(win)
                pygame.display.update()

                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                            
                    if event.type == pygame.QUIT:                    
                        okay = True
                        gameIsGoingOn = False
                        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if playAgainBtn.isOver(pos):
                            okay = True
                            
                    if event.type == pygame.MOUSEMOTION:
                        if playAgainBtn.isOver(pos):
                            playAgainBtn.color = (255, 130, 130)
                        else:
                            playAgainBtn.color = (235, 20, 20)

main()
pygame.display.quit()
pygame.quit()