#player
import carddeck
import json
import playeranalyze

class Player:
  def __init__(self, name, pos):
    self.name = name
    self.pos = pos
    self.given = False
    self.cards = []
    self.winner = False
    self.playedCard = ""
    self.playedCardResult = True
    self.sticks = 0
    self.points = 0
    self.virtual = False
    self.bid = 0
    self.lastbid = False
    self.notbid = -1
    self.rankAverage = 0
    self.longsuite = False
    self.totalbids = 0
    self.tmpCards = []
    self.offensive = False
    self.longsuitelen = 0

  def __str__(self):
    return f"{self.name}({str(self.pos)})"
  
  def myPos(self):
    return self.pos
  
  def SetBidSticks(self, value):
    try: 
      if self.lastbid and (int(value) == self.notbid):
        return False 
      else:
        self.bid = int(value)
        self.offensive = self.bid >= (len(self.cards) / 2)
        return True
    except:
      return False 

  def getRankAverage(self, cards):
    if len(cards) <= 0:
      return 0
    rankSum = 0
    for card in cards:
      rankSum = rankSum + card.rankNr
    return rankSum / len(cards)
  
  def checkStrongLongSuites(self, cards):
    longSuiteLen = 0
    if len(cards) <= 0:
      return False
    tmplongsuite = False
    cntLongSuites = dict()
    for suit in carddeck.suits:
      strong = 0
      summa = 0
      for card in cards:
        if card.suit == suit:
          summa = summa + 1
          if card.rankNr > 10:
            strong = strong + 1
      cntLongSuites[suit] = summa if strong >= 2 else 0

    for suit in carddeck.suits:
      if cntLongSuites[suit] > (len(cards) / 2):
        longSuiteLen = cntLongSuites[suit]
        tmplongsuite = True

    return longSuiteLen    

  def SetVirtualBidSticks(self, playorder):
    value = 0
    cards = self.GetCards()
    if len(cards) <= 0:
      return value
    self.rankAverage = self.getRankAverage(cards)
    self.longsuitelen = self.checkStrongLongSuites(cards)
    self.longsuite = self.longsuitelen > 0

    #count royal cards
    royalcards = 0
    for card in cards:
      if card.rankNr > 10:
        royalcards = royalcards + 1

    playerAnalyze = playeranalyze.PlayerAnalyze()
    iData = playerAnalyze.readfile("AIdata.txt")
    if iData > 0:
      bidSuggest = playerAnalyze.analyzeDataFromAverageAndRoyalcards(len(cards), self.rankAverage, royalcards, self.longsuite)
      if playerAnalyze.hit:
        value = bidSuggest
        if self.longsuite and playerAnalyze.longsuite:
          lsValue = playerAnalyze.lsSticks
          if lsValue > value:
            value = lsValue
      else:
        value = royalcards  
    else:
      value = royalcards

    if len(cards) == 1:
      if playorder == 0:
        value = 1
      elif playorder > 0:  
        value = 0

    if value < 0:
      value = 0
    elif value > len(cards):
      value = len(cards)

    if self.lastbid and (value == self.notbid):
      if value == 0:
        value = 1
      elif value == len(cards):
        value = value - 1
      else:
        if self.rankAverage > 8:    
          value = value + 1
        else:  
          value = value - 1  

    self.bid = value
    self.offensive = self.bid >= 2 #(len(self.cards) / 2)
    return value
    
  def isGiven(self):
    return self.given

  def setGiven(self, isGiven):
    self.given = isGiven  
    
  def setWinner(self, isWinner):
    self.winner = isWinner  
    
  def addSticks(self, newSticks):
    self.sticks = self.sticks + newSticks
    return self.sticks

  def setPoints(self):
    if self.sticks == self.bid:
      if self.bid > 0:
        self.points = self.points + (self.sticks * 10)
      else:
        self.points = self.points + 5
  

  def addcard(self, card):  
    self.cards.append(card);
  
  def cardsleft(self):
    return len(self.cards)  
    
  def getPlayedCard(self):
    return self.playedCard  
        
  def getSuit(self):
    aSuit = carddeck.suits[0] 
    if self.cardsleft() > 0:
      tmpCard = self.cards[0]
      for card in self.cards:
        if card.rankint() < tmpCard.rankint():
          tmpCard = card
      aSuit = tmpCard.suit       
    return aSuit
  
  '''
  def playcardX(self):
    szCard = ""
    cardsNr = len(self.cards)
    if cardsNr > 0:
      first = True
      tmpCard = self.cards[0]
      for card in self.cards:
        if card.rankint() > tmpCard.rankint():
          tmpCard = card
        elif card.rankint() == tmpCard.rankint():
          if card.suitint() < tmpCard.suitint():
            tmpCard = card
      szCard = str(tmpCard)
      self.cards.remove(tmpCard)
            
    return szCard
  '''

  '''
  def selectCard(self, fsuit, first):
    select = ""
    cardOK = False
    i = 0
    print(self)
    for card in self.cards:
      i += 1
      print(str(i) + " " + str(card))
      
    while cardOK == False:
      select = -1   
      szSelect = input("Select card!")
      try:
        select = int(szSelect) - 1
      except:
        select = -1
      cardOK = select < len(self.cards) and select >= 0
      if cardOK:
        tmpCard = self.cards[select]
        print(first)
        print(fsuit)
        print(select)
        if tmpCard.suit != fsuit and first == False:
          #check suit
          for card in self.cards:
            if card.suit == fsuit:
              cardOK = False
              break
        
    szCard = tmpCard
    self.cards.remove(tmpCard)
            
    self.playedCard = szCard;        
    return szCard
  '''  
  def playerPlayCard(self, szCard):    
    iRtn = 100
    self.playedCardResult = False
    try:
      for card in self.cards:
        if str(szCard) == str(card):
          tmpCard = card
          self.cards.remove(card)           
          self.playedCard = tmpCard
          iRtn = 200
          self.playedCardResult = True
          break
      return iRtn
    except:         
      return iRtn

  def getAutomaticPlaycard(self, fsuit, fRankInt):
    #szTest = "Test Rank (Int): {}" 
    #print(szTest.format(fRankInt))
    szCard = None
    if len(self.cards) > 0:
      #first = True
      tmpCard = self.cards[0]

      suitCards = []
      for card in self.cards:
        if fsuit == None or card.suit == fsuit:
          suitCards.append(card)

      if (self.offensive or (self.bid-self.sticks == 1)) and fsuit == None and self.sticks < self.bid:    
        #play strongest
        tmpI = 0
        for card in suitCards:
          if card.rankint() > tmpI:
            tmpCard = card
            tmpI = card.rankint()
          
      elif len(suitCards) > 0 and self.sticks < self.bid:
        #Find highest       
        tmpI = 0
        for card in suitCards:
          if card.rankint() > tmpI:
            tmpCard = card
            tmpI = card.rankint()
            
        bFound = False    
        if self.sticks != self.bid:
          for card in suitCards:
            if card.rankint() > fRankInt:
              bFound = True
              if self.offensive or (self.bid-self.sticks == 1):
                if card.rankint() > tmpCard.rankint():
                  tmpCard = card
              else:  
                if card.rankint() < tmpCard.rankint():
                  tmpCard = card
        if not bFound:
          #Find lowest
          tmpI = 15
          for card in suitCards:
            if card.rankint() < tmpI:
              tmpCard = card
              tmpI = card.rankint()
          
      else:      
        if self.sticks < self.bid:
          #waste lowest card if wrong suit
          for card in self.cards:
            if card.rankint() < tmpCard.rankint():
              tmpCard = card
        else:      
          #waste lowest card if you are first to play
          if fsuit == None:
            for card in self.cards:
              if card.rankint() < tmpCard.rankint():
                tmpCard = card          
          else:
            if len(suitCards) <= 0:
              #waste highest card if wrong suit
              for card in self.cards:
                if card.rankint() > tmpCard.rankint():
                  tmpCard = card
              if (tmpCard == None):
                tmpCard = self.cards[0]
            else:      
              #waste highest card lower than rank
              tmpCard = None              
              for card in suitCards:
                if card.rankint() < fRankInt:
                  if (tmpCard == None) or (card.rankint() > tmpCard.rankint()):
                    tmpCard = card
              if (tmpCard == None):
                tmpCard = suitCards[0]
      
      szCard = tmpCard
      #self.cards.remove(tmpCard)
            
    #self.playedCard = szCard;        
    return szCard
  
  def GetCards(self):
    retCards = []
    for card in self.cards:
      retCards.append(card)
    return retCards  
  
  # def UpdateStat(self, fplayer):
  #   self.winner = fplayer.winner
  #   if self.winner:
  #     self.points += 1
  #   self.cards = []        
  #   for card in fplayer.GetCards():
  #     #print("Card (X1):" + str(card))
  #     self.cards.append(card)    
  
  def showcards(self):
    szCards = ""
    for card in self.cards:
      #printinfo
      szCards = szCards + " " + card.printinfo()
      #testGetInfo
      #szCards = szCards + " " + " " + card.printinfo() + card.testGetInfo()
    return szCards
  
  def summerycards(self):
    self.tmpCards = []
    for card in self.cards:
      tmpCard = {}
      tmpCard.update({"suit": card.suit})
      tmpCard.update({"rank": card.rank})
      self.tmpCards.append(tmpCard)


  def summerygame(self):
    rtns = dict()
    #name of player
    rtns["player"] = self.name
    #cards to json
    rtns["cardcount"] = len(self.tmpCards)
    rtns["cards"] = self.tmpCards

    #properties to json
    rtns["sticks"] = self.sticks
    rtns["points"] = self.points
    rtns["virtual"] = "true" if self.virtual else "false"
    rtns["bid"] = self.bid
    rtns["offensive"] = "true" if self.offensive else "false"
    rtns["lastbid"] = "true" if self.lastbid else "false"
    rtns["notbid"] = self.notbid
    rtns["rankAverage"] = self.rankAverage
    rtns["longsuite"] = "true" if self.longsuite else "false"
    rtns["longsuitelen"] = self.longsuitelen
    rtns["totalbids"] = self.totalbids

    return json.dumps(rtns)