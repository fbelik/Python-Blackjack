class Card:
    nums = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
    suits = ['C','S','D','H']
    def __init__(self,num,suit):
        self.num = num
        self.suit = suit
        self.isFaceUp = False
    def name(self):
        return "{} of {}".format(self.num, self.suit)#[self.num,self.suit]
    def getRankAceHigh(self):
        if (self.num == 'J' or self.num =='Q' or self.num == 'K'):
            return 10
        elif (self.num=='A'):
            return 11
        else:
            return self.num
    def getRankAceLow(self):
        if (self.num == 'J' or self.num == 'Q' or self.num == 'K'):
            return 10
        elif (self.num=='A'):
            return 1
        else:
            return self.num
    def flip(self):
        if self.isFaceUp:
            self.isFaceUp = False
        else:
            self.isFaceUp = True
    def isAce(self):
        if (self.num == 'A'):
            return True
        return False

import random

class Deck:
    def __init__(self):
        self.cards = []
    def shuffle(self):
        nums = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
        suits = ['C','S','D','H']
        for suit in suits:
            for num in nums:
                self.cards.append(Card(num,suit))
        self.cards = random.sample(self.cards,52)
    def createHand(self,numCards):
        newHand = Hand(self.cards[0:numCards])
        del self.cards[0:numCards]
        return newHand

class Hand:
    def __init__(self,cards):
        self.cardsInHand = cards
    def hasAce(self):
        for card in self.cards:
            if (card.num=='A'):
                return True
        return False
    def getAceLowValue(self):
        rank = 0
        for card in self.cardsInHand:
            rank += card.getRankAceLow()
        return rank
    def getAceHighValue(self):
        rank = 0
        for card in self.cardsInHand:
            rank += card.getRankAceHigh()
        return rank
    def getValue(self):
        aceHighValue = self.getAceHighValue()
        if (aceHighValue>21):
            return self.getAceLowValue()
        return aceHighValue
    def add(self,card):
        self.cardsInHand.append(card)
    def clear(self):
        self.cardsInHand = []

class Player:
    def __init__(self,name):
        self.name = name
        self.hand = None
        self.splitHand = None
        self.money = 50
    def hit(self):
        resp = input(r'Hit(y/n)   ')
        if (resp=='y'):
            return True
        return False
    def isBust(self):
        if (self.hand.getValue()>21):
            return True
        return False
    def stand(self):
        self.isStand = True
    def addToHand(self,card):
        self.hand.cardsInHand.append(card)
    def displayHand(self):
        for card in self.hand.cardsInHand:
            print(card.name())

class Dealer:
    def __init__(self,deck):
        self.deck = deck
        self.dealersCards = None
    def firstDeal(self,players,AIs):
        for player in players:
            player.hand = self.deck.createHand(2)
        for AI in AIs:
            AI.hand = self.deck.createHand(2)
        self.dealersCards = self.deck.createHand(2)
    def dealCard(self,player):
        player.addToHand(self.deck.cards[0])
        del self.deck.cards[0]
    def playOut(self):
        while (self.dealersCards.getValue()<17):
            self.dealersCards.add(self.deck.cards[0])
            del self.deck.cards[0]
        print("Dealer has")
        self.displayHand(len(self.dealersCards.cardsInHand)+1)
        print('Dealers value is',self.dealersCards.getValue())
        return self.dealersCards.getValue()
    def displayHand(self,num):
        for card in self.dealersCards.cardsInHand[0:num]:
            print(card.name())

class AI:
    def __init__(self,name):
        self.name = name
        self.hand = None
        self.money = 50
    def isBust(self):
        if (self.hand.getValue()>21):
            return True
        return False
    def isHit(self,hand,dealersHand):
        dealersRevealedCard = dealersHand.cardsInHand[0].getRankAceHigh()
        if (dealersRevealedCard>6):
            if (self.hand.getValue()>=17):
                return False
            else:
                return True
        elif (dealersRevealedCard>3):
            if (self.hand.getValue()>=12):
                return False
            else:
                return True
        else:
            if (self.hand.getValue()>=13):
                return False
            else:
                return True
    def addToHand(self,card):
        self.hand.cardsInHand.append(card)
    def displayHand(self):
        for card in self.hand.cardsInHand:
            print(card.name())
            
class Blackjack:
    def __init__(self,playerNames,AIs = []):
        self.deck = Deck()
        self.players = {}
        self.AIPlayers = {}
        #self.AllAIs = {}
        self.playerBets = {}
        self.dealer = Dealer(self.deck)
        self.round = 0
        for name in playerNames:
            self.players[name] = Player(name)
        for ai in AIs:
            newAI = AI(ai)
            self.AIPlayers[ai] = newAI
            #self.AllAIs[ai] = newAI
    def playRound(self):
        try:
            for name,player in self.players.items():
                player.hand.clear()
            for name,ai in self.AIPlayers.items():
                ai.hand.clear()
        except:
            pass
        self.deck.shuffle()
        self.dealer.firstDeal(self.players.values(),self.AIPlayers.values())
        for name,ai in self.AIPlayers.items():
            if (ai.money<=0):
                try:
                    self.AIPlayers.pop(name)
                except:
                    pass
        print('Dealer has')
        self.dealer.displayHand(1)
        playerValues = {}
        for name,player in self.players.items():
            self.playerBets[name] = 10
            rnum = 1
            while True:
                print(name)
                player.displayHand()
                if (player.isBust()):
                    print(name,'is bust')
                    playerValues[name] = player.hand.getValue()
                    break
                resp = ''
                while not isValid(resp):
                    resp = input('%s, hit or stand?:   ' % name)
                if (resp == 'hit'):
                    self.dealer.dealCard(player)
                elif (resp == 'double down' and rnum == 1):
                    print('players bet is now $20')
                    self.playerBets[name] = 20
                else:
                    playerValues[name] = player.hand.getValue()
                    print(name,'had',player.hand.getValue())
                    break
                rnum += 1
        for name,ai in self.AIPlayers.items():
            self.playerBets[name] = 10
            while (ai.isHit(ai.hand,self.dealer.dealersCards)):
                self.dealer.dealCard(ai)
            playerValues[name] = ai.hand.getValue()
            print(name)
            ai.displayHand()
            print('AI',name,'had',ai.hand.getValue())
        dealerValue = self.dealer.playOut()
        for name,key in playerValues.items():
            if ((key>dealerValue and key<=21) or (dealerValue>21 and key<=21)):
                print(name,'wins')
                try:
                    self.players[name].money += self.playerBets[name]
                    print(name,'has',self.players[name].money,'dollars')
                except:
                    self.AIPlayers[name].money += self.playerBets[name]
                    print(name,'has',self.AIPlayers[name].money,'dollars')
            elif(key<dealerValue or key>21):
                try:
                    self.players[name].money -= self.playerBets[name]
                    print(name,'has',self.players[name].money,'dollars')
                except:
                    self.AIPlayers[name].money -= self.playerBets[name]
                    print(name,'has',self.AIPlayers[name].money,'dollars')
            else:
                try:
                    print(name,'has',self.players[name].money,'dollars')
                except:
                    print(name,'has',self.AIPlayers[name].money,'dollars')
    def playGame(self, num_rounds):
        for round in range(num_rounds):
            self.playRound()
        print("\nRESULTS:")
        for name,player in self.players.items():
            print("{:8s}: ${:3d}".format(name, player.money))
        for name,AI in self.AIPlayers.items():
            print("{:8s}: ${:3d}".format(name, AI.money))


def isValid(resp):
    if (resp=='hit' or resp=='stand' or resp=='double down'):
        return True
    return False

if __name__ == "__main__":
    players = input("Enter names of human players, separated by spaces: ").split()
    AIs = input("Enter names of AI players, separated by spaces: ").split()
    num_rounds = input("How many rounds to play: ")
    while True:
        try:
            if int(num_rounds) >= 0:
                num_rounds = int(num_rounds)
                break
        except:
            num_rounds = input("Invalid entry, how many rounds to play:  ")
    game = Blackjack(players, AIs=AIs)
    game.playGame(num_rounds)
