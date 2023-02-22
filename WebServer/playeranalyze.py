#playeranalyze
import carddeck
import json

def analyzePlayingCards(playingCards, round):
    res = len(playingCards) > 0
    sumRank = 0
    sumCnt = 0
    for thisplayingCards in playingCards:
      cnt = 0
      for card in thisplayingCards:
        if round == cnt:
          sumRank += card.rankNr
          sumCnt += 1
          break
        cnt = cnt + 1

    
    if res and sumCnt >= 1:
      return round(sumRank / sumCnt)
    else:
      return -1


class PlayerAnalyze:
  def __init__(self):
    self.file = ""
    self.jsonobjects = []
    self.rankAverage = 0
    self.longsuite = False
    self.hit = False
    self.lsSticks = 0
    self.playingCards = []

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
            game = jsondata["game"]
            if "plump" == game:
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
      if "cardcount" in jsondata.keys() and jsondata["catdcount"] == cardcount:
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
      if "cardcount" in jsondata.keys() and jsondata["cardcount"] == cardcount:
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
      if "cardcount" in jsondata.keys() and jsondata["cardcount"] == cardcount:
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

  def analyzeDataFromCountingCards(self, cardcount, strongroyalcards, royalCards, middleCards, lowCards, longsuite):
    sticks = 0
    averagecntr = 0
    longsuitecntr = 0
    stickssum = 0
    longsuitessticks = 0

    for jsondata in self.jsonobjects:
      if "cardcount" in jsondata.keys() and jsondata["cardcount"] == cardcount:
        tmpStrongRoyalCards = self.countCardsInterval(jsondata["cards"], 13, 14)
        tmpRoyalCards = self.countCardsInterval(jsondata["cards"], 11, 12)
        tmpmiddleCards = self.countCardsInterval(jsondata["cards"], 7, 10)
        tmplowCards = self.countCardsInterval(jsondata["cards"], 2, 6)
        if tmpStrongRoyalCards == strongroyalcards and tmpRoyalCards == royalCards and tmpmiddleCards == middleCards and tmplowCards == lowCards:
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

  def GetPlayingCards(self):
    return self.playingCards
    
  




