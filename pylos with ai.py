import pygame
import numpy as np
import pygame_gui
import copy
from sys import exit

#sākuma vērtības
Player = 0
Player1_marbles=7
Player2_marbles=7
game_active = 0

#-------attēli un citi vizuālie elementi --------
pygame.init()
screen = pygame.display.set_mode((1000,1210))
board_img = pygame.image.load('images/Board.png').convert()
pygame.display.set_caption('Pylos')
clock=pygame.time.Clock()

hoverbutton = (255, 160, 113)
button = (255, 136, 77)
screencolor=(229, 122, 69)
textfont = pygame.font.SysFont("Cairo",75)

player1_count = pygame.image.load('images/SmallPlayer_1.png').convert_alpha()
player2_count = pygame.image.load('images/SmallPlayer_2.png').convert_alpha()
player1_set = pygame.image.load('images/Player_1_ver2_b.png').convert_alpha()
player2_set = pygame.image.load('images/Player_2_ver2_b.png').convert_alpha()
player_none = pygame.image.load('images/Player_none.png').convert_alpha()
start_screen = pygame.image.load('images/start_game.png').convert_alpha()
marble_background = pygame.image.load('images/marble_background.png').convert_alpha()
text_playagain=textfont.render('Click Y to play again!', True, 'Beige')
text_winner=0
#koordinātes, kur zīmē spēlētāja atlikušās bumbiņas
koords1 = [80,200,320,440,560,680,800]
koords2 = [800,680,560,440,320,200,80]
#--------------------------------------------------


#spēles lauciņa klase
class Spot:
    def __init__(self, x, y, nr,state):
        self.x = x
        self.y = y
        self.nr = nr
        self.state = state

    #pārbauda, vai izvelētā vieta atbilst kādam laukam
    def checkSpot(ar,ar2,ix,iy): #ar = empty spots, ar2 = taken spots
        for s in ar:
            Rx=s.x+100
            Ry=s.y+100
            if ((ix-Rx)*(ix-Rx)+(iy-Ry)*(iy-Ry)) < 100**2:
                return s
        for j in ar2:
            Rx=j.x+100
            Ry=j.y+100
            if ((ix-Rx)*(ix-Rx)+(iy-Ry)*(iy-Ry)) < 100**2:
                return j
        return 0

    #pārbauda, vai atbilst kādam laukam, gadījumā, kad veic pārnešanu
    def checkSpot_movable(ar,ix,iy): #ar = empty
        #global movable
        for s in ar: #apskatamies vai ir izvēlēts tukšs lauks
            Rx=s.x+100
            Ry=s.y+100
            if ((ix-Rx)*(ix-Rx)+(iy-Ry)*(iy-Ry)) < 100**2:
                print('yes')
                return s
        return 0

    #pārbauda, vai divreiz netiek izvēlēts viens un tas pats lauks.
    def checkIfSelectedTwice(sel,ix,iy):
        Rx=sel.x+100
        Ry=sel.y+100
        if ((ix-Rx)*(ix-Rx)+(iy-Ry)*(iy-Ry)) < 100**2:
                return sel 
        return 0

class movableToSquare():
    def __init__(self, square, possibleNr):
        self.square = square
        self.possibleNr=possibleNr

movableToSquare1 = movableToSquare([Spot(126,231,1,0),Spot(401,231,2,0),Spot(126,506,4,0),Spot(401,506,5,0)],[Spot(676,231,3,0),Spot(676,506,6,0),Spot(126,781,7,0),Spot(401,781,8,0),Spot(676,781,9,0)])
movableToSquare2 = movableToSquare([Spot(401,231,2,0),Spot(676,231,3,0),Spot(401,506,5,0),Spot(676,506,6,0)],[Spot(126,231,1,0),Spot(126,506,4,0),Spot(126,781,7,0),Spot(401,781,8,0),Spot(676,781,9,0)])
movableToSquare3 = movableToSquare([Spot(126,506,4,0),Spot(401,506,5,0),Spot(126,781,7,0),Spot(401,781,8,0)],[Spot(126,231,1,0),Spot(401,231,2,0),Spot(676,231,3,0),Spot(676,506,6,0),Spot(676,781,9,0)])
movableToSquare4 = movableToSquare([Spot(401,506,5,0),Spot(676,506,6,0),Spot(401,781,8,0),Spot(676,781,9,0)],[Spot(126,231,1,0),Spot(401,231,2,0),Spot(676,231,3,0),Spot(126,506,4,0),Spot(126,781,7,0)])


#masīvi ar spēles informāciju
arraySpots = [Spot(126,231,1,0),Spot(401,231,2,0),Spot(676,231,3,0),
Spot(126,506,4,0),Spot(401,506,5,0),Spot(676,506,6,0),
Spot(126,781,7,0),Spot(401,781,8,0),Spot(676,781,9,0)]
arrayTaken=[]


#pārbauda cik gājieni palikuši
def checkMarbles():
    global Player1_marbles
    global Player2_marbles
    screen.blit(marble_background,(0,0))
    screen.blit(marble_background,(0,1105))
    for x in koords2[:Player1_marbles]:
        screen.blit(player1_count,(x,0))
    for x in koords1[:Player2_marbles]:
        screen.blit(player2_count,(x,1110))
    

#veic gājienu gan vizuāli, gan noņem uzlikto marble no kopējā skaita
def place_marble(pl,x,y):
    global Player1_marbles
    global Player2_marbles
    if pl == 1:
        screen.blit(player1_set,(x,y))
        Player1_marbles=Player1_marbles-1
    if pl == 2:
        screen.blit(player2_set,(x,y))
        Player2_marbles=Player2_marbles-1
#pārnešanas gadījumā, noņem uz lauka esošo lodīti, nodrošina atlikušo lodišu skaita nemainīgumu
def take_marble(pl,spot):
    global Player
    global Player1_marbles
    global Player2_marbles
    if pl == 1:
        screen.blit(player_none,(spot.x,spot.y))
        Player1_marbles=Player1_marbles+1
    if pl == 2:
        screen.blit(player_none,(spot.x,spot.y))
        Player2_marbles=Player2_marbles+1

#padod nākamajam spēletājam gājienu ja vinam ir atlikusi marbles, ja nav, tad gājiens paliek pie tā paša spēlētaja
def next_move(pl):
    global Player
    global Player1_marbles
    global Player2_marbles
    if Player == 1:
        #place_marble(1, x, y)
        if Player2_marbles != 0:
            pl = Player % 2 + 1
        elif Player2_marbles == 0 and Player1_marbles > 0:
            pl = Player 
            print('PLAYER 1 TURN AGAIN') 
    elif Player == 2:
        #if Player1_marbles != 0:
        if Player1_marbles != 0:
            pl = Player % 2 + 1
        elif Player1_marbles == 0 and Player2_marbles > 0:
            pl = Player
            print('PLAYER 2 TURN AGAIN') 
    #pl = Player % 2 + 1
    return pl

def next_move_AI(pl):
    global Player
    global Player1_marbles
    global Player2_marbles
    #ja tikko gāja spēlētājs un viņš ir pirmais, kas iet, tad pārbauda, vai datoram ir gājieni
    if pl == 1 and Player == 1:
        if Player2_marbles != 0:
            pl = 'AI'
        elif Player2_marbles == 0 and Player1_marbles > 0:
            pl = 1 
            print('PLAYER 1 TURN AGAIN')
    elif pl == 2 and Player == 2:
        if Player1_marbles != 0:
            pl = 'AI'
    elif Player1_marbles == 0 and Player2_marbles > 0:
            pl = 2
    elif pl == 1 and Player == 2:
        if Player2_marbles != 0:
            pl = 1
    elif Player2_marbles == 0 and Player1_marbles > 0:
            pl = 'AI' 
            print('PLAYER 1 TURN AGAIN')
    elif pl == 2 and Player == 1:
        if Player1_marbles != 0:
            pl = 1
    elif Player1_marbles == 0 and Player2_marbles > 0:
            pl = 'AI' 
            print('PLAYER 1 TURN AGAIN')
    return pl  

class Board:
    #paņem iepriekš izveidotos arrays
    global arraySpots
    global arrayTaken
    def __init__(self):
        self.spots=arraySpots
        self.empty_spots = self.spots
        self.taken_spots = arrayTaken
    
    #pārbauda, vai uz izvēlētais lauks ir pieejams uz spēles laukuma
    def checkBoard(self, nr):
        global Player
        skaitlis = 0
        for n in self.empty_spots:
            if n.nr == nr:
                if n.state == 0:
                    skaitlis = 1
        for m in self.taken_spots:
            if m.nr == nr and m.state == Player:
                skaitlis = 2
        return skaitlis

    #pārbauda, vai izvēlētais lauks ir pieejams uz spēles laukuma AI gājiena gadījumā
    def checkBoardForAI(self, ai, AI_board_empty, AI_board_taken, numurs):
        global Player
        skaitlis = 0
        for n in AI_board_empty:
            if n.nr == numurs:
                if n.state == 0:
                    skaitlis = 1
            if n.nr == numurs and numurs == 14:
                if n.state == 0:
                    skaitlis = 3
        # for m in AI_board_taken:
        #     if m.nr == numurs and m.state == ai.player:
        #         print('hey')
        #         skaitlis = 2
        return skaitlis

    #pārnešanas gadījumā ar šo metodi pārbauda, vai ir iespējams tur pārlikt lodīti
    def checkBoardForMove(self,empty_spots,new_select_spot):
        for n in empty_spots:
            if n.nr == new_select_spot.nr:
                return 1
        return 0

    #pievieno lauciņu kā aizņemtu
    def addTaken(self,spot):
        self.taken_spots.append(spot)

    #lauciņa atbrīvošanas gadījumā pieliek atpakaļ pie brīvajiem lauciņiems
    def addToEmpty(self,spot):
        spot.state=0
        self.empty_spots.append(spot)
        if spot in self.empty_spots:
            print(spot.nr,'HAS BEEN ADDED BACK TO LIST OF EMPTY')

    #pārbauda, vai ir veidojies kvadrāts uz lauka pirmā līmeņa, ja ir, tad pievieno kā iespējamu gājiena lauciņu tā vidū esošo lauciņu. 
    def checkPossibleLevels(self):
        arrayNr=[]
        arrayNr_empty=[]
        #global game_active
        for n in self.taken_spots:
            arrayNr.append(n.nr)
        for m in self.empty_spots:
            arrayNr_empty.append(m.nr)
        if (1 in arrayNr and 2 in arrayNr and 4 in arrayNr and 5 in arrayNr) and 10 not in arrayNr:
            if 10 not in arrayNr_empty:
                nr10=Spot(263.5,368.5,10,0)
                print(';;nocheckpossible levels pieliek 10')
                self.empty_spots.append(nr10)
        if 2 in arrayNr and 3 in arrayNr and 5 in arrayNr and 6 in arrayNr and 11 not in arrayNr:
            if 11 not in arrayNr_empty:  
                nr11=Spot(538.5,368.5,11,0)
                self.empty_spots.append(nr11)
        if 4 in arrayNr and 5 in arrayNr and 7 in arrayNr and 8 in arrayNr and 12 not in arrayNr:
            if 12 not in arrayNr_empty: 
                nr12=Spot(263.5,643.5,12,0)
                self.empty_spots.append(nr12)
        if 5 in arrayNr and 6 in arrayNr and 8 in arrayNr and 9 in arrayNr and 13 not in arrayNr:
            if 13 not in arrayNr_empty: 
                nr13=Spot(538.5,643.5,13,0)
                self.empty_spots.append(nr13)
        if 10 in arrayNr and 11 in arrayNr and 12 in arrayNr and 13 in arrayNr and 14 not in arrayNr:
            top=Spot(401,506,14,0)
            self.empty_spots.append(top)

    #pārbauda vai pēc pārnešanas veikšanas nav atbrīvojies kāds pirmā līmeņa kvadrāts.Ja ir, tad tā virsotni izņem no iespējamo gājienu saraksta.
    def checkPossibleToDeleteLevel(self):
        arrayNr_takenSpots=[]
        arrayNr_emptySpots=[]
        for n in self.taken_spots:
            arrayNr_takenSpots.append(n.nr)
        for m in self.empty_spots:
            arrayNr_emptySpots.append(m.nr)
        if (1 not in arrayNr_takenSpots or 2 not in arrayNr_takenSpots or 4 not in arrayNr_takenSpots or not 5 in arrayNr_takenSpots):
            if 10 in arrayNr_emptySpots:
                nr10=Spot(263.5,368.5,10,0)
                idx=self.empty_spots.index(nr10)
                print('SPOT NR 10 SHOULD BE UNAVAILABLE AGAIN NOW')
                self.empty_spots.pop(idx)
        if (2 not in arrayNr_takenSpots or 3 not in arrayNr_takenSpots or 5 not in arrayNr_takenSpots or 6 not in arrayNr_takenSpots):
            if 11 in arrayNr_emptySpots:
                nr11=Spot(538.5,368.5,11,0)
                idx=self.empty_spots.index(nr11)
                self.empty_spots.pop(idx)
        if (4 not in arrayNr_takenSpots or 5 not in arrayNr_takenSpots or 7 not in arrayNr_takenSpots or 8 not in arrayNr_takenSpots):
            if 12 in arrayNr_emptySpots:
                nr12=Spot(263.5,643.5,12,0)
                idx=self.empty_spots.index(nr12)
                self.empty_spots.pop(idx)
        if (5 not in arrayNr_takenSpots or 6 not in arrayNr_takenSpots or 8 not in arrayNr_takenSpots or 9 not in arrayNr_takenSpots):
            if 13 in arrayNr_emptySpots:
                nr13=Spot(538.5,643.5,13,0)
                idx=self.empty_spots.index(nr13)
                self.empty_spots.pop(idx)


    #pāŗbauda, vai ir sasniegta uzvara
    def checkWin(self):
        arrayNr=[]
        global text_winner
        for n in self.taken_spots:
            arrayNr.append(n.nr)
        if 14 in arrayNr:
            for m in self.taken_spots:
                if m.nr == 14:
                    string_winner = str(m.state)
            winner = 'Player ' + string_winner + ' wins!!'
            text_winner=textfont.render(winner, True, 'Beige')
            return 7
        return False

    #pārbauda izvēlētās pārnešanai lodītes pacelšanas lauciņus
    def checkWhereToMoveSpot(self,spot):
        numbersForSpots = [] #jaunais empty array ko es izmantosu updateosanai kamer kaulins ir selected
        for m in movableToSquare1.possibleNr:
            if spot.nr == m.nr:
                nr10=Spot(263.5,368.5,10,0)
                numbersForSpots.append(nr10)
        for m in movableToSquare2.possibleNr:
            if spot.nr == m.nr:
                nr11=Spot(538.5,368.5,11,0)
                numbersForSpots.append(nr11)
        for m in movableToSquare3.possibleNr:
            if spot.nr == m.nr:
                nr12=Spot(263.5,643.5,12,0)
                numbersForSpots.append(nr12)
        for m in movableToSquare4.possibleNr:
            if spot.nr == m.nr:
                nr13=Spot(538.5,643.5,13,0)
                numbersForSpots.append(nr13)
        return numbersForSpots #jaunais "empty" spot array

    #maina spēles lauka stāvokli, gadījumā, kad notiek pacelšana
    def updateStateWithMove(self,selectedSpot, newEmpty, spot):
        global Player
        # global game_active
        thisMove = Player
        for n in newEmpty:
            if spot.nr == n.nr: #ja parliksanai izveletais spots ir jaunajaa empty spot masiivaa
                
                for empties in self.empty_spots:
                    if n.nr == empties.nr:
                        print('IN NEW EMPTY ARRAY WE HAVE NR',n.nr)
                        idx=self.empty_spots.index(empties)
                        n.state=Player
                        #aizņem jauno lauciņu masīvā ar player krāsu
                        self.addTaken(n)
                        self.addToEmpty(selectedSpot)
                        self.empty_spots.pop(idx)
                        take_marble(Player,selectedSpot)
                        place_marble(Player,spot.x,spot.y)
                        pl = next_move_AI(Player)
                        checkMarbles()
                        newEmpty=[]
                        self.checkPossibleToDeleteLevel()
                        return pl  
        return
    

    def updateState(self, spot, AI):
        global Player
        if AI == False:
            gajiens = copy.deepcopy(Player)
        elif AI ==True:
            gajiens = copy.deepcopy(Player % 2 + 1) 
        global game_active
        for n in self.empty_spots:
            if n.nr == spot.nr:
                idx=self.empty_spots.index(n)
                n.state = gajiens
                self.addTaken(n) #pievieno aiznemto lauku aiznemto lauku sarakstam
                self.empty_spots.pop(idx)
        if self.checkWin():
            place_marble(gajiens,spot.x,spot.y)#uzliek kauliņu pēdejo un beidz darbību
            pl = next_move_AI(gajiens)
            game_active = 3
            return
        place_marble(gajiens,spot.x,spot.y)#move == nākamā spēlētāja kārta!
        gajiens = copy.deepcopy(gajiens)
        #---------------------------
        pl = copy.deepcopy(next_move_AI(gajiens))
        #---------------------------
        checkMarbles()
        #ja var tad pievieno nākamā līmeņa empty spots
        self.checkPossibleLevels()
        return pl


class AI:
    def __init__(self, player):
        self.player = copy.deepcopy(player)

    def minimax(self, board_empty, board_taken):
        all_selectable_coords=[]
        all_selectable_nrs=[]
        empty_for_AI = copy.deepcopy(board_empty)
        for n in empty_for_AI:
            all_selectable_coords.append((n.x,n.y))
            all_selectable_nrs.append((n.nr))
        taken_for_AI = copy.deepcopy(board_taken)  
        for m in taken_for_AI:
            if m.state == self.player and m.nr < 10:
                all_selectable_coords.append((m.x,m.y))
                all_selectable_nrs.append((m.nr))
        #checkBoard - 1 ir ok, 2 ir riktigi labi
        spot_ratings=[]
        for spots in all_selectable_nrs:
            print(spots)
            selected_spot_eval = Board.checkBoardForAI(Board,ai, empty_for_AI, taken_for_AI, spots)
            if selected_spot_eval == 1:
                spot_ratings.append((spots,1))
            elif selected_spot_eval == 2:
                spot_ratings.append((spots,2))
            elif selected_spot_eval == 3:
                spot_ratings.append((spots,3))
        #iegūstam masīvu ar visu iespējamo move novērtejumu - kauliņa nr un tā novērtejums
        best_moves=spot_ratings[0]
        #k ir viens typle ar NR un EVAL
        for k in spot_ratings:
            if k[1] > best_moves[1]:
                #saglabā labāko move!
                best_moves=copy.deepcopy(k)
        print(best_moves) #(vietas nr, funkcijas vērtība)
        if best_moves[1] == 1:
            for l in empty_for_AI:
                if l.nr == best_moves[0]:
                    board.updateState(l, True)
                    #best_moves = 0
        elif best_moves[1] == 3:
            board.updateState(Spot(401,506,14,0), True)
            #best_moves = 0
        #pašlaik pārbauda, via 
        #elif best_moves[1] == 2:

            return 

        
            

        

selectedd = 0
while True:
    board = Board()
    if game_active == 1:
        pl_mr1=Player1_marbles
        pl_mr2=Player2_marbles
        mouse = pygame.mouse.get_pos()
        #uzzīmē spēlētaju sākuma lodītes
        for x in koords2[:Player1_marbles]:
            screen.blit(player1_count,(x,0))
        for x in koords1[:Player2_marbles]:
            screen.blit(player2_count,(x,1110))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pozx, pozy = pygame.mouse.get_pos()
                #pārbauda, vai uzspiestais punkts atbilst kādam spēles lauciņam
                place_valid = Spot.checkSpot(board.spots,board.taken_spots, pozx, pozy)

                #!= 0 nozīme, ka atbilst
                if place_valid != 0:
                    #pārbauda, vai un kāda veida gājiens ir iespējams
                    place_free = board.checkBoard(place_valid.nr)

                    #1 nozīmē parasts gājiens, kur novieto jaunu lodīti uz tukšu laukumu
                    if place_free == 1:
                        #
                        possible_moves = board.updateState(place_valid, False)
                        if possible_moves == 'AI':
                            go = ai.minimax(board.empty_spots, board.taken_spots)
                            #if go == 1:
                             #  reutn     
                    elif place_free == 2:
                        #vajag lai shis butu tikai tad, kad "selected lodīte" ir tavas krāsas
                        print('MARBLE HAS BEEN SELECTED')
                        #-----------#
                        selectedd = place_valid
                        game_active = 2
                        #-----------#

    if game_active == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print('YOU HAVE SELECTED', selectedd.nr)
                pozx2, pozy2 = pygame.mouse.get_pos()
                #pārbauda vai ir "deselected"
                second_selection = Spot.checkIfSelectedTwice(selectedd,pozx2,pozy2)
                if second_selection != 0:
                    print('MARBLE HAS BEEN DESELECTED')
                    game_active = 1
                else:
                    new_empty = board.checkWhereToMoveSpot(selectedd)
                    place_valid = Spot.checkSpot_movable(new_empty, pozx2, pozy2)

                    #PLACE_VALID atgriež vai nu ja iespējams pārlikt to lauku, vai arī 0
                    if place_valid != 0:
                        place_free = board.checkBoardForMove(new_empty,place_valid)
                        #place_free atgriež 1 ja izvēlētā vieta ir pie jaunā brīvo spotu saraksta, 0, ja nav
                        if place_free == 1:
                            #selectedd ir tas KURU mēs pārliekam, place_valid ir tas KUR mēs pārliekam
                            possible_moves = board.updateStateWithMove(selectedd, new_empty, place_valid)
                            if possible_moves == 'AI':
                                go = ai.minimax(board.empty_spots, board.taken_spots)
                                
                            #board.checkPossibleToDeleteLevel()
                            game_active=1                   


    if game_active == 3: #spēle ir uzvarēta
        screen.fill((229, 122, 69))
        screen.blit(text_winner,(300,400))
        screen.blit(text_playagain,(250,800))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    arraySpots = [Spot(126,231,1,0),Spot(401,231,2,0),Spot(676,231,3,0),
                    Spot(126,506,4,0),Spot(401,506,5,0),Spot(676,506,6,0),
                    Spot(126,781,7,0),Spot(401,781,8,0),Spot(676,781,9,0)]
                    arrayTaken = []
                    Player1_marbles=7
                    Player2_marbles=7
                    game_active = 0


    if game_active == 0:
        screen.blit(start_screen,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    Player=1
                    ai = AI(2)
                    screen.fill((248, 231, 209))
                    screen.blit(board_img,(0,105))
                    game_active = 1
                if event.key == pygame.K_2:
                    Player=2
                    ai = AI(1)
                    screen.fill((248, 231, 209))
                    screen.blit(board_img,(0,105))
                    game_active = 1
    pygame.display.update()
    clock.tick(60)



                       