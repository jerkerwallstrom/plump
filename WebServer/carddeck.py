from numpy import random

suits = tuple(("heart", "spade", "diamond", "club"))
ranks = {
   "ace": 14, 
   "2": 2, 
   "3": 3, 
   "4": 4, 
   "5": 5, 
   "6": 6, 
   "7": 7, 
   "8": 8, 
   "9": 9, 
   "10": 10, 
   "jack": 11, 
   "queen": 12, 
   "king": 13
}

def getSuitInt(suit):
  return suits.index(suit)

def getRankInt(rank):
  return ranks[rank]

class Card:
  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank
    self.suitNr = getSuitInt(suit)
    self.rankNr = getRankInt(rank)
    if self.rankNr == 1:
      self.rankNr = 14
      
  def __str__(self):
    return f"{self.suit}({self.rank})" 
    
  def printinfo(self):
    return f"{self.suit}({self.rank})"

  def testGetInfo(self):
    return "Suit: " + str(self.suitNr) + " " + "Rank: " + str(self.rankNr) + "(" +  str(ranks[self.rank]) +  ");"
    
  def rankint(self):
    return self.rankNr;

  def suitint(self):
    return self.suitNr;
  
class CardDeck: 
  def __init__(self):
    self.cards = []
    self.createDeck()

  def createDeck(self):
    self.cards = []
    for s in suits:
      for r in ranks: 
        self.cards.append(Card(s, r))
    
  def shuffle(self):    
    shufflecards = []
    i = 0
    while i < 52:
      i += 1
      #from numpy import random
      s = 52 - i
      x = 0;
      if s > 0:
        x = random.randint(s)

      #print("X = " +  str(x))
      l = len(self.cards)
      #print("len = " + str(l))
      if x >= l:
        print("Error X")
      else:  
        card = self.cards[x]
        shufflecards.append(card)
        self.cards.remove(card)
      
    self.cards = shufflecards;  

  def cardleft(self):
    l = len(self.cards)
    return l > 0
    
    
  def getcard(self):
    l = len(self.cards)
    x = random.randint(l)
    card = self.cards[x]
    self.cards.remove(card)
      
 
    return card 
        
#carddeck = CardDeck();
    
#test
#print(len(carddeck.cards))
#for c in carddeck.cards:
#  print(c)

#carddeck.shuffle() 
  
#print(len(carddeck.cards))
#for c in carddeck.cards:
#  print(c)
  
#print("Get card")  
#if carddeck.cardleft:
#  card = carddeck.getcard()
#  print(card)
  