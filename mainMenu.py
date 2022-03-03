import pygame, sys
from playsound import playsound
pygame.init()

oknoX,oknoY = 600,500
win = pygame.display.set_mode((oknoX,oknoY))
tile = pygame.image.load("C:/Users/fifah/OneDrive/Plocha/arabárna/programko/python/projekty/tile.jpg")
#herní pole, které se vytvoří podle různých znaků vepsaných do str

texture = """##########
#TTTTTT  #
#KKKMMM O#
#   UU LO#
#HH jG LDF
#XLLjG LD#
#X   G AA#
#XPPP II #
##########"""

botTexture = """##########
#   IIII #
#        #
#    kp  #
#HH  kp  F 
#    kpO #
#  LLLLO #
#      O #
##########"""
#potřebné proměnné na vytvoření menu
font = pygame.font.SysFont('Arial', 45)
rect1 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*1 - 85,250,150),2) 
rect2 = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*2 - 70,250,150),2) 

####################################################################################

#class pro vytvoření rects v metodě readMap_createObj, leva/prava/hore/dole - bool pro pohyb v botovi
class Obdelnik(pygame.Rect):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)   
        self.x = x*50
        self.y = y*50
        self.width = width*50
        self.height = height*50
        
        if self.height > self.width:
            self.stoji = True
            self.hore = True
            self.dole = True
            self.prava = False
            self.leva = False

        elif self.height < self.width:
            self.stoji = False
            self.prava = True
            self.leva = True
            self.hore = False
            self.dole = False
            
class Game():
    def __init__(self):
        self.gamemode = "Main"
        self.radioactive = None
        self.mapa, self.obdelniky = [], []
        self.frajer = None
        self.index = 0
        self.zasobnik = []

    def push(self,rect):
        self.zasobnik.append(rect)
        self.index += 1

    def popOut(self):
        self.index -= 1
        return self.zasobnik.remove((self.index) + 1)

    def getIndex(self):
        if len(self.zasobnik) == 0:
            return len(self.zasobnik)
        else:
            return len(self.zasobnik) - 1
        #1x rect -> poslední je na indexu 0, 0x rect -> index posledního je stále 0, proto tento if 
    
    #všechny col... metody kontrolují srážky s rects před nimi(směr pohybu) a pokud narazí na jiný rect, vratí se z5 a předají impuls 
    def colPosX(self):  
        for rect in self.obdelniky:
            if rect.colliderect(self.radioactive) and rect != self.radioactive:
                self.radioactive.x -= 50
                self.radioactive = rect
                self.push(rect)

    def colNegX(self):
        for rect in self.obdelniky:
            if rect.colliderect(self.radioactive) and rect != self.radioactive:
                self.radioactive.x += 50
                self.radioactive = rect
                self.push(rect)

    def colPosY(self):
        for rect in self.obdelniky:
            if rect.colliderect(self.radioactive) and rect != self.radioactive:
                self.radioactive.y -= 50
                self.radioactive = rect
                self.push(rect)

    def colNegY(self):
        for rect in self.obdelniky:
            if rect.colliderect(self.radioactive) and rect != self.radioactive:
                self.radioactive.y += 50
                self.radioactive = rect
                self.push(rect)

    def readMap_createObj(self,s):
        radek = []
        for x in s:                                           
            if x == "\n":
                if len(radek) != 0:
                    self.mapa.append(radek)
                    radek = []
            else: radek.append(x)
        self.mapa.append(radek)

        for y in range(len(self.mapa)):
            for x in range(len(radek)):
                if self.mapa[y][x] != " " and self.mapa[y][x] != "#" and self.mapa[y][x] != "F":
                    
                    if self.mapa[y][x] == self.mapa[y][x+1]: # sirokej
                        i = 2
                        while True:
                            if self.mapa[y][x] == self.mapa[y][x+i]:
                                i += 1
                            else: 
                                self.obdelniky.append(Obdelnik(x,y,i,1))
                                for sirka in range(i):
                                    self.mapa[y][x + sirka] = " "
                                break
                            
                    elif self.mapa[y][x] ==  self.mapa[y+1][x]: # vysokej
                        i = 2
                        while True:
                            if self.mapa[y][x] == self.mapa[y+i][x]:
                                i += 1
                                
                            else: 
                                self.obdelniky.append(Obdelnik(x,y,1,i))
                                for vyska in range(i):
                                    self.mapa[y + vyska][x] = " "
                                break
        #zjištění bloku, který je hlavní
        for i in self.obdelniky:
            if i.x == 50 and i.y == 200:
                self.frajer = i
                self.radioactive = self.frajer
                
    #metoda pro pohyb(podle inputu z klávesnice) 
    def podminka(self,eventy):
        if self.gamemode == "Game": # or gamemode =="Bot":  #pokud chci manipulovat v bot
            for event in eventy:

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_UP and self.radioactive.stoji:
                        if self.mapa[self.radioactive.y//50 - 1][self.radioactive.x//50] != "#":
                            self.radioactive.y -= 50
                            for tvojemama in self.obdelniky:
                                if tvojemama.colliderect(self.radioactive) and tvojemama != self.radioactive:
                                    self.radioactive.y += 50
                                        #byl tady break idk why

                    elif event.key == pygame.K_DOWN and self.radioactive.stoji:
                        if self.mapa[self.radioactive.y//50 + self.radioactive.height//50][self.radioactive.x//50] != "#":
                            self.radioactive.y += 50
                            for tvojemama in self.obdelniky:
                                if tvojemama.colliderect(self.radioactive) and tvojemama != self.radioactive:
                                    self.radioactive.y -= 50
                                    

                    elif event.key == pygame.K_RIGHT and not self.radioactive.stoji: 
                        if self.mapa[self.radioactive.y//50][self.radioactive.x//50 + self.radioactive.width//50] != "#":
                            self.radioactive.x += 50
                            if self.radioactive == self.frajer and self.mapa[self.radioactive.y // 50][self.radioactive.x//50 + self.radioactive.width//50 - 1] == "F":
                                #playsound("C:/Users/fifah/Desktop/burgir.MP3")
                                print("Konec hry")
                                self.gamemode = "End"
                            for tvojemama in self.obdelniky:
                                if tvojemama.colliderect(self.radioactive) and tvojemama != self.radioactive:
                                    self.radioactive.x -= 50
                                    
                    
                    elif event.key == pygame.K_LEFT and not self.radioactive.stoji:
                        if self.mapa[self.radioactive.y//50][self.radioactive.x//50 - 1] != "#":
                            self.radioactive.x -= 50
                            for tvojemama in self.obdelniky:
                                if tvojemama.colliderect(self.radioactive) and tvojemama != self.radioactive:
                                    self.radioactive.x += 50
                                    
        elif self.gamemode == "Bot":
            self.podminkaBot()
    
    #metoda, ve které vše potřebné, aby se bot pohyboval
    def podminkaBot(self):
        if self.getIndex() == 0:
            self.push(self.frajer)
        
        if self.radioactive == self.frajer:
            if self.mapa[self.radioactive.y // 50][self.radioactive.x//50 + self.radioactive.width//50 - 1] == "F": #F = výhra
                print("vi von")
                self.gamemode = "Main"
            self.radioactive.x += 50
            self.colPosX()
        
        elif self.radioactive != self.frajer and self.radioactive.stoji:
            #up
            if self.radioactive.hore and self.mapa[self.radioactive.y//50 - 1][self.radioactive.x//50] != "#":
                self.radioactive.y -= 50
                self.colNegY()

            elif self.radioactive.hore and self.mapa[self.radioactive.y//50 - 1][self.radioactive.x//50] == "#":
                self.radioactive.hore = False
                self.zasobnik.pop()
                self.radioactive = self.zasobnik[self.getIndex() - 1]

            #down
            elif not self.radioactive.hore and self.mapa[self.radioactive.y//50 + self.radioactive.height//50][self.radioactive.x//50] != "#":
                self.radioactive.y += 50
                self.colPosY()
            
            elif self.radioactive.dole and self.mapa[self.radioactive.y//50 + self.radioactive.height//50][self.radioactive.x//50] == "#":
                self.radioactive.dole = False
                self.zasobnik.pop()
                self.radioactive = self.zasobnik[self.getIndex() - 1]

            #oboje
            elif not self.radioactive.hore and not self.radioactive.dole:
                self.zasobnik.pop()
                self.radioactive = self.zasobnik[self.getIndex() - 1]


        elif self.radioactive != self.frajer and not self.radioactive.stoji:
            #right
            if self.mapa[self.radioactive.y//50][self.radioactive.x//50 + self.radioactive.width//50] != "#": # not in "#F"
                self.radioactive.x += 50
                self.colPosX()

            elif self.mapa[self.radioactive.y//50][self.radioactive.x//50 + self.radioactive.width//50] == "#":
                self.radioactive.prava = False
                self.zasobnik.pop()
                self.radioactive = self.zasobnik[self.getIndex() - 1]

            #left
            elif not self.radioactive.prava and [self.radioactive.y//50][self.radioactive.x//50 - 1] != "#":
                self.radioactive.x -= 50
                self.colNegX()
            
            elif self.radioactive.prava and self.mapa[self.radioactive.y//50][self.radioactive.x//50 - 1] == "#":
                self.radioactive.dole = False
                self.zasobnik.pop()
                self.radioactive = self.zasobnik[self.getIndex() - 1]

            #oboje
            elif not self.radioactive.prava and not self.radioactive.leva:
                self.zasobnik.pop()
                self.radioactive = self.zasobnik[self.getIndex() - 1]

        pygame.time.delay(300)
                
        

#třída, ve které jsou vščechny potřebné metody na vykreslování rects atd   
class Draw():
    def __init__(self,game):
        self.game = game

    def drawEnd(self):
        text3 = font.render("You win", True,(255,255,255))
        text4 = font.render("Main menu", True,(255,255,255))
        win.fill((0,0,0))
        pygame.draw.rect(win, (255,255,255), pygame.Rect(rect1), 2)
        pygame.draw.rect(win, (255,255,255), pygame.Rect(rect2), 2)
        win.blit(text3,(oknoX//2 - 65,oknoY//3*2 - 200))
        win.blit(text4,(oknoX//2 - 95,oknoY//3*1 + 145))
        pygame.display.update()

    def drawMain(self):
        win.fill((0,0,0))
        text1 = font.render("SinglePlayer", True,(255,255,255))
        text2 = font.render("Bottares", True,(255,255,255))
        pygame.draw.rect(win, (100,0,0), pygame.Rect(rect1), 2)
        pygame.draw.rect(win, (100,0,0), pygame.Rect(rect2), 2)
        win.blit(text1,(oknoX//2 - 100,oknoY//3*2 - 200))
        win.blit(text2,(oknoX//2 - 70,oknoY//3*1 + 145))
        pygame.display.update()

    def draw(self):
        color,selectColor,frajerColor,frajerSelectColor = (100,0,0),(0,100,0),(0,0,255),(255, 0, 255)
        
        if self.game.gamemode == "Game" or self.game.gamemode == "Bot":
            win.fill((0,0,0))
            for y in range(len(self.game.mapa)):
                for x in range(len(self.game.mapa[0])):
                    if self.game.mapa[y][x] == "#":
                        win.blit(tile,(x * 50,y * 50))

            #barva se mění podle toho, jaký rect je zvolený
            for obdelnik in self.game.obdelniky:
                if obdelnik == self.game.radioactive:
                    if self.game.frajer == self.game.radioactive:
                        pygame.draw.rect(win, frajerSelectColor, (obdelnik.x+5 , obdelnik.y+5, obdelnik.width-10, obdelnik.height-10))
                    else:
                        pygame.draw.rect(win, selectColor, (obdelnik.x+5 , obdelnik.y+5, obdelnik.width-10, obdelnik.height-10))
                elif obdelnik == self.game.frajer:
                    pygame.draw.rect(win, frajerColor, (obdelnik.x+5 , obdelnik.y+5, obdelnik.width-10, obdelnik.height-10))
                else: 
                    pygame.draw.rect(win, color, (obdelnik.x+5 , obdelnik.y+5, obdelnik.width-10, obdelnik.height-10))
            
            pygame.display.update()
            

        elif self.game.gamemode == "Main":
            self.drawMain()

        elif self.game.gamemode == "End":
            self.drawEnd()

#metoda, která obstarává všechny menu a obsahuje metodu pro překlikávání mezi rects
class Select():
    def __init__(self,game):
        self.game = game

    def mainSelect(self):
        if rect1.collidepoint(pygame.mouse.get_pos()) and self.game.gamemode == "Main":
            self.game.readMap_createObj(botTexture)
            print("Zapnutí SinglePlayeru")
            self.game.gamemode = "Game"

        elif rect2.collidepoint(pygame.mouse.get_pos()) and self.game.gamemode == "Main":
            self.game.readMap_createObj(texture)
            print("Zapnutí bota")
            self.game.gamemode = "Bot"

    def endSelect(self):
        endRect = pygame.draw.rect(win, (100,0,0), pygame.Rect(oknoX//2 - 125,oknoY//3*2 - 70,250,150),2)
        if endRect.collidepoint(pygame.mouse.get_pos()) and self.game.gamemode == "End":
            self.game.gamemode = "Main"

    def select(self):
        if self.game.gamemode == "Main":
            self.mainSelect()
        elif self.game.gamemode == "Game": # or gamemode == "Bot": #pokud chci manipulovat v bot
            for tvojemama in self.game.obdelniky:
                if tvojemama.collidepoint(pygame.mouse.get_pos()):
                    self.game.radioactive = tvojemama
                    
        elif self.game.gamemode == "Bot":
            print("select = None")
        elif self.game.gamemode == "End":
            self.endSelect()   

