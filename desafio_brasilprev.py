import random
from random import shuffle


class Game:
    def __init__(self,numPlayersO,playerMoneyListO,propertiesOwnedListO,posListO,masterPropertiesOwnedListO):
        self.j = 0
        self.numPlayersO = numPlayersO
        self.playerMoneyListO = playerMoneyListO
        self.propertiesOwnedListO = propertiesOwnedListO
        self.posListO = posListO
        self.masterPropertiesOwnedListO = masterPropertiesOwnedListO
        self.boxValues = [0]*20
        self.ultimateBoxValues = [0]*20
        self.propertyPriceList = [None,50,60,70,80,90,100,105,110,115,120,125,130,135,140,150,160,170,180,190]

        self.monopolies = [(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)]
        self.propertyRentList = [None,20,22,24,26,30,33,35,38,40,42,44,46,48,51,300,400,450,460,475]

        self.numPlayers = self.numPlayersO
        self.wins = [0]*self.numPlayers
        self.losses = [0]*self.numPlayers
        self.ties = [0]*self.numPlayers

        self.winningProperties = [0]*20
        self.losingProperties = [0]*20
        self.propertyLostOn = [0]*20

        self.averageTurns = 0
        self.maxTurns = 0

        self.gameState = []
        self.gamesWon = [[],[],[],[]]

        self.minValueToBuyProperty = 50


    def simulate(self):
        '''
            Simulador do desafio
        '''

        self.playerMoneyList = self.playerMoneyListO.copy()
        self.propertiesOwnedList = [[],[],[],[],[]]
        for n in range(len(self.propertiesOwnedListO)):
            self.propertiesOwnedList[n] = self.propertiesOwnedListO[n].copy()
        self.posList = self.posListO.copy()
        self.masterPropertiesOwnedList = self.masterPropertiesOwnedListO.copy()
        self.turnsPlayed = 0
        self.players = list(range(self.numPlayers))
        random.shuffle(self.players)

        won = False

        while not won:
            for p in self.players:
                done = False
                rollCounter = 0

                while not done:
                    self.die = random.randrange(1,7)
                    done = True
                    self.posList[p] += self.die

                    if self.posList[p] >= 20:
                        self.posList[p] -= 20
                        self.playerMoneyList[p] += 100

                    if isinstance(self.propertyPriceList[self.posList[p]],int) and (self.posList[p] not in self.masterPropertiesOwnedList):
                        if self.propertyPriceList[self.posList[p]] < self.playerMoneyList[p]  and (p != 0 or self.playerMoneyList[p]-self.propertyPriceList[self.posList[p]] > self.minValueToBuyProperty):
                            if p == 0:
                                self.masterPropertiesOwnedList.append(self.posList[p])
                                self.propertiesOwnedList[p].append(self.posList[p])
                                self.playerMoneyList[p] -= self.propertyPriceList[self.posList[p]]                            
                            if p == 1 and self.propertyRentList[self.posList[p]] > 50:
                                self.masterPropertiesOwnedList.append(self.posList[p])
                                self.propertiesOwnedList[p].append(self.posList[p])
                                self.playerMoneyList[p] -= self.propertyPriceList[self.posList[p]]
                            if p == 2 and self.propertyPriceList[self.posList[p]] <= self.playerMoneyList[p]+80:
                                self.propertiesOwnedList[p].append(self.posList[p])
                                self.playerMoneyList[p] -= self.propertyPriceList[self.posList[p]]
                            if p == 3 and random.randrange(1,2) == 1:
                                self.propertiesOwnedList[p].append(self.posList[p])
                                self.playerMoneyList[p] -= self.propertyPriceList[self.posList[p]]

                    if self.posList[p] in self.masterPropertiesOwnedList and self.posList[p] not in self.propertiesOwnedList[p]:
                        for player in range(len(self.propertiesOwnedList)):
                            if self.posList[p] in self.propertiesOwnedList[player]:
                                self.playerMoneyList[p] -= self.propertyRentList[self.posList[p]]
                                self.playerMoneyList[player] += self.propertyRentList[self.posList[p]]

                    if self.playerMoneyList[p] <= 0:
                        for property in self.propertiesOwnedList[p]:
                            if len(self.players) > 2:
                                if property in self.masterPropertiesOwnedList:
                                    self.masterPropertiesOwnedList.remove(property)

                        if len(self.players) > 2:
                            self.propertiesOwnedList[p].clear()

                        self.losses[p] += 1
                        self.propertyLostOn[self.posList[p]] += 1
                        for property in self.propertiesOwnedList[p]:
                            self.losingProperties[property] += 1
                        try:
                            self.players.remove(p)
                        except ValueError:
                            print(self.j)
                        done = True

                    if len(self.players) == 1:
                        won = True
                        done = True
                        for player in self.players:
                            self.wins[player] += 1
                            self.gamesWon[player].append(self.j+1)

                        self.averageTurns += self.turnsPlayed
                        if self.turnsPlayed > self.maxTurns:
                            self.maxTurns = self.turnsPlayed

                    elif self.turnsPlayed >= 1000:
                        won = True
                        done = True                        
                        for player in self.players:
                            if max(self.playerMoneyList) == self.playerMoneyList[player]:
                                self.wins[player] += 1
                                self.gamesWon[player].append(self.j+1)                            
                            self.ties[player] += 1
                        self.players = []

                self.turnsPlayed += 1
                self.boxValues[self.posList[p]] += 1

        for v in range(len(self.boxValues)):
            self.boxValues[v] = (self.boxValues[v]/self.turnsPlayed)
            self.ultimateBoxValues[v] += self.boxValues[v]

        #Saving end game state
        self.gameState.append(self.__dict__.copy())

    def simulateMany(self,num):
        '''
            Simulador da quatidade de jogos informada
            args: num (int) - The number of games to simulate
        '''
        for self.j in range(num):
            self.simulate()


    def display(self):
        '''
            Saida com as informacoes solicitadas
        '''

        self.numWins = 0
        self.numLosses = 0
        self.numTies = 0

        for i in range(len(self.wins)):
            self.numWins += self.wins[i]
            self.wins[i] = self.wins[i]/(self.j+1)

        print('Quantidade de partidas que terminaram por time out(1000 rodadas):')
        print(max(self.ties))
        print('Quantidade de turnos em media que demora uma partida:')
        print(self.averageTurns/300)
        print('Porcentagem de vitoria do jogador impulsivo:')
        print(self.wins[0])
        print('Porcentagem de vitoria do jogador exigente:')
        print(self.wins[1])
        print('Porcentagem de vitoria do jogador cauteloso:')
        print(self.wins[2])
        print('Porcentagem de vitoria do jogador aleatorio:')
        print(self.wins[3])
        print('Comportamento mais vencedor é:')
        if max(self.wins) == self.wins[0]:
            print('Impulsivo')
        elif max(self.wins) == self.wins[1]:
            print('Exigente')
        elif max(self.wins) == self.wins[2]:
            print('Cauteloso')
        elif max(self.wins) == self.wins[3]:
            print('Aleatorio')
            
def main():

    numPlayers = 4
    playerMoneyList = [300,300,300,300]
    propertiesOwnedList = [[],[],[],[]]
    posList = [0,0,0,0]    
    masterPropertiesOwnedList = []

    game1 = Game(numPlayers,playerMoneyList,propertiesOwnedList,posList,masterPropertiesOwnedList)
    game1.simulateMany(300)
    game1.display()

main()

