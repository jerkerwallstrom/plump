#competitor
import carddeck

class RoundInfo:
  def __init__(self, round, suit, card):
    self.round = round
    self.suit = suit
    self.card = card
    

class Competitor:
  def __init__(self, name):
    self.name = name
    self.cards = []

  def addCard(self, round, suit, card):
    roundinfo = RoundInfo(round, suit, card)
    self.cards.append(roundinfo)

  def haveCardInSuit(self, suit):
    result = False
    for c in self.cards:
      if c.suit == suit:
        result = suit == c.card.suit
    if not result:
      bTest = 1
    return result 

  def haveSuitBeenPlayed(self, suit):
    result = 0
    for c in self.cards:
      if c.suit == suit:
        result += 1
    return result 
  
  def getRecommendedSuit(self):
    suit = None

    #suitCnts = dict((j, i) for i, j in carddeck.suits)
    suitCnts = dict()
    for suit in carddeck.suits:
      suitCnts[suit] = 0
    iCnt = 0
    for c in reversed(self.cards):
      v = suitCnts[c.suit]
      v += 1
      suitCnts[c.suit] = v
      if suit == None:
        suit = c.suit
        iCnt += 1
      elif c.suit == suit:
        iCnt += 1
    vMax = 0    
    for sCnt in suitCnts:
      v = suitCnts[sCnt]
      if v > vMax:
        suit = sCnt
        vMax = v

    rtns = dict()
    rtns[suit] = vMax
    return rtns

    

