#playeranalyze
import carddeck
import json

class PlayerAnalyze:
  def __init__(self):
    self.file = ""
    self.jsonobjects = []
    self.rankAverage = 0
    self.longsuite = False
    self.hit = False
    self.lsSticks = 0

  def __str__(self):
    return ""
  
  def readfile(self, afile):
    empty = 0
    f = open("AIdata.txt", "r")
    for line in f:
      if len(line ) > 0:
        szline = line.rstrip(line[-1])
        if len(szline) > 0:
          jsondata = json.loads(szline)
          try:
            player = jsondata["player"]
            if len(player) > 0:
              self.jsonobjects.append(jsondata)
          except:
            empty =+ 1    

    f.close()

    return len(self.jsonobjects)
  
  def analyzeDataFromBid(self, cardcount, bid):
    self.rankAverage = 0
    averagecntr = 0
    averagesum = 0
    longsuitetrue = 0
    for jsondata in self.jsonobjects:
      if jsondata["catdcount"] == cardcount:
        if jsondata["bid"] == bid and jsondata["bid"] == jsondata["sticks"]:
          rankAverage = jsondata["rankAverage"]
          averagecntr = averagecntr + 1
          averagesum = averagesum + rankAverage
          if jsondata["longsuite"] == "true":
            longsuitetrue = longsuitetrue + 1
    if averagecntr > 0:
      self.rankAverage = averagesum / averagecntr
      self.longsuite = longsuitetrue*2 > averagecntr
    
  def analyzeDataFromAverage(self, cardcount, average, onlybidokay):
    averagecntr = 0
    stickssum = 0
    longsuitetrue = 0

    self.sticks = 0
    self.longsuite = False

    for jsondata in self.jsonobjects:
      if jsondata["cardcount"] == cardcount:
        if not onlybidokay or jsondata["bid"] == jsondata["sticks"]:
          if jsondata["rankAverage"] > (average - 1.5) and jsondata["rankAverage"] < average + 1.5:
            sticks = jsondata["sticks"]
            averagecntr = averagecntr + 1
            stickssum = stickssum + sticks
          if jsondata["longsuite"] == "true":
            averagecntr = longsuitetrue + 1
    if averagecntr > 0:
      self.sticks = stickssum / averagecntr
      self.longsuite = longsuitetrue*2 > averagecntr
    return round(self.sticks)

  def countRoyalCards(self, cards):
    royals = 0
    for card in cards:
      rankint = carddeck.getRankInt(card["rank"])
      if rankint > 10:
        royals += 1
    return royals    
  
  def countCardsInterval(self, incards, minV, maxV):
    outcards = 0
    for card in incards:
      rankint = carddeck.getRankInt(card["rank"])
      if rankint >= minV and rankint <= maxV:
        outcards += 1
    return outcards    
      
  def analyzeDataFromAverageAndRoyalcards(self, cardcount, average, royalCards, longsuite):
    sticks = 0
    averagecntr = 0
    longsuitecntr = 0
    stickssum = 0
    longsuitessticks = 0

    for jsondata in self.jsonobjects:
      if jsondata["cardcount"] == cardcount:
        tmprankAverage = jsondata["rankAverage"]
        if (tmprankAverage > (average - 1)) and (tmprankAverage < (average + 1)):
            tmpRoyalCards = self.countRoyalCards(jsondata["cards"])
            if tmpRoyalCards == royalCards:
              tmpsticks = jsondata["sticks"]
              averagecntr = averagecntr + 1
              stickssum = stickssum + tmpsticks
              if jsondata["longsuite"] == "true":
                longsuitecntr += 1
                longsuitessticks = longsuitessticks + tmpsticks
            # if jsondata["longsuite"] == "true":
            #   averagecntr = longsuitetrue + 1
    self.hit = averagecntr > 0
    self.longsuite = longsuitecntr  > 0

    self.lsSticks = 0
    if longsuitecntr > 0:
      self.lsSticks = round(longsuitessticks / longsuitecntr)

    if averagecntr > 0: 
      sticks = round(stickssum / averagecntr)
    
    return sticks

  def analyzeDataFromCountingCards(self, cardcount, royalCards, middleCards, lowCards, longsuite):
    sticks = 0
    averagecntr = 0
    longsuitecntr = 0
    stickssum = 0
    longsuitessticks = 0

    for jsondata in self.jsonobjects:
      if jsondata["cardcount"] == cardcount:
        tmpRoyalCards = self.countRoyalCards(jsondata["cards"])
        tmpmiddleCards = self.countCardsInterval(jsondata["cards"], 7, 10)
        tmplowCards = self.countCardsInterval(jsondata["cards"], 2, 6)
        if tmpRoyalCards == royalCards and tmpmiddleCards == middleCards and tmplowCards == lowCards:
          tmpsticks = jsondata["sticks"]
          averagecntr = averagecntr + 1
          stickssum = stickssum + tmpsticks
          if jsondata["longsuite"] == "true":
            longsuitecntr += 1
            longsuitessticks = longsuitessticks + tmpsticks
    self.hit = averagecntr > 0
    self.longsuite = longsuitecntr  > 0

    self.lsSticks = 0
    if longsuitecntr > 0:
      self.lsSticks = round(longsuitessticks / longsuitecntr)

    if averagecntr > 0: 
      sticks = round(stickssum / averagecntr)
    
    return sticks




