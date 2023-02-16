#game
import player
import carddeck
import webparser
import json

#players = [];
#l = 1
#i = 0
gameStatus = set(("idle", "playeradd", "deal", "start", "end"))

class Game:

  def __init__(self):
    self.players = []
    self.playersOrder = []
    self.cardPlayerName = ""
    self.tokenName = ""
    self.cardDeck = carddeck.CardDeck()
    self.nrofcards = 9 #Start with one more than in the first round
    self.webparser = webparser.webParser()
    self.format = "text"
    self.jSonV = json.dumps("text")
    self.function = ""
    self.gamestatus = "idle"
    self.checkthewinner = False
    self.winner = ""
    self.firstcard = True
    self.playingSuit = carddeck.suits[0]
    self.playedcards = []
    self.nextPlayer = None
    self.bestcard = None
    self.maxnrofcards = 10
    self.round = 0
    self.logplayedcards = dict()

  def Handle(self, query):
    szRtn = "no function"
    self.format = "json"
    #slRtn = []
    function = self.webparser.getFunction(query)
    self.function = function
    if function == "addplayer":
      szRtn = self.addPlayer(query)
    elif function == "getplayers": 
      szRtn = self.getPlayers(query)       
    elif function == "checkplayer":
      szRtn = self.validPlayer(query)
    elif function == "deal":  
      szRtn = self.deal(query)
    elif function == "start":
      szRtn = self.start(query)
    elif function == "getcards":
      szRtn = self.getCards(query)
    elif function == "playcard":
      szRtn = self.playCard(query)
    elif function == "playvirtual":
      szRtn = self.playVirtualCard(query)
    elif function == "nextround":
      szRtn = self.nextround(query)
    elif function == "actualgameinfo":
      szRtn = self.getActualGameInfo(query)
    elif function == "actualplayer":
      szRtn = self.getActualPlayer(query)    
    elif function == "bidsticks":
      szRtn = self.setBidSticks(query)
    
    if len(szRtn) <= 0:
      szRtn = "no function"

    return szRtn

  def getActualGameInfo(self, query):
    #rtns = dict()
    #rtns["player"] = self.cardPlayerName
    #szRtn = json.dumps(rtns)
    szRtn = self.getActualStatusOfGame()
    return szRtn

  def getPlayerForName(self, name):
    for p in self.playersOrder:
      if p.name == name:
        return p

  def addPlayer(self, query):
    name = self.webparser.parseCmd("name", query)
    self.format = self.webparser.parseCmd("format", query)
    virtual = self.webparser.parseCmd("virtual", query) == "true"
    szRtn = self.addPlayerToGame(name, virtual)
    return szRtn

  def validPlayer(self, query):  
    name = self.webparser.parseCmd("name", query)
    self.format = "json" #self.webparser.parseCmd("format", query)
    rtns = dict()
    rtns["name"] = name
    rtns["valid"] = "true" if name ==  self.cardPlayerName else "false"
    rtns["player"] = self.cardPlayerName
    szRtn = json.dumps(rtns)
    return szRtn

  def getCards(self, query):
    szRtn = ""
    self.format = self.webparser.parseCmd("format", query)
    name = self.webparser.parseCmd("name", query)
    for p in self.players:
      if p.name == name:
        cards = p.GetCards()
        tmpCards = []
        for card in cards:
          tmpCard = {}
          tmpCard.update({"suit": card.suit})
          tmpCard.update({"rank": card.rank})
          tmpCards.append(tmpCard)
        cardsdic = dict()
        cardsdic["player"] = name
        cardsdic["cards"] = tmpCards
        self.jSonV = json.dumps(cardsdic)
        szRtn = str(self.jSonV)
        break

    return szRtn  
  
  def setBidSticks(self, query):
    rtns = dict()
    res = False
    virtual = False
    self.format = self.webparser.parseCmd("format", query)
    name = self.webparser.parseCmd("name", query)
    value = self.webparser.parseCmd("value", query)
    virtual = self.webparser.parseCmd("virtual", query) == "true"
    #Set value for user in query
    ipcnt = 0
    for p in self.playersOrder:
      if name == p.name:
        if virtual:
          ivalue = p.SetVirtualBidSticks(ipcnt)
          value = str(ivalue)
          res = (ivalue >= 0) and (ivalue <= self.nrofcards)
        else:  
          res = p.SetBidSticks(value)
          ivalue = p.bid
          if res:
            try:
              res = (ivalue >= 0) and (ivalue <= self.nrofcards)
            except:
              res = False  
        rtns["player"] = name
        rtns["bid"] = value
        break
      ipcnt += 1

    if res:  
      tmpBids = 0
      for p in self.playersOrder:
        tmpBids = tmpBids + p.bid
      for p in self.playersOrder:
        p.totalbids = tmpBids


    #Prepare for next user
    next = ""
    bNext = False
    
    if res:
      lastName = self.playersOrder[len(self.playersOrder)-1].name
      last = False
      for p in self.playersOrder:
        if name == p.name:
          bNext = True
        else:
          if bNext:
            next = p.name
            last = lastName == next
            virtual = p.virtual
            break
      bids = 0
      for p in self.playersOrder:
        p.lastbid = p.name == lastName
        if p.name != lastName:
          bids = bids + p.bid
      notbid = (self.nrofcards) - bids
      self.playersOrder[len(self.playersOrder)-1].notbid = notbid

    rtns["result"] = "true" if res else "false"
    if res:
      rtns["next"] = next
      rtns["virtual"] = "true" if virtual else "false"
      rtns["last"] = "true" if last else "false"
      if last:
        rtns["notbid"] = str(notbid)
      playcard = len(next) <= 0 
      rtns["playcard"] = "false" if not playcard else "true"
      if playcard:
        self.setNewPlayersOrder()
        self.cardPlayerName = self.playersOrder[0].name
        self.nextPlayer = self.playersOrder[0]
        self.bestcard = None
        self.playedcards = []
        rtns["nextplaycard"] = self.cardPlayerName

    return json.dumps(rtns)

  def setNewPlayersOrder(self):
    starter = ""
    highBid = -1
    for p in self.playersOrder:
      if p.bid > highBid:
        highBid = p.bid
        starter = p.name

    bfound = False
    self.playersOrder = []
    for p in self.players:
      if starter == p.name:
        self.playersOrder.append(p)
        bfound = True
      elif bfound:  
        self.playersOrder.append(p)

    for p in self.players:
      if starter == p.name:
        bfound = False
      elif bfound:  
        self.playersOrder.append(p)

    return self.playersOrder

  def playVirtualCard(self, query):
    szRtn = ""
    rtns = dict();  
    self.format = self.webparser.parseCmd("format", query)
    name = self.webparser.parseCmd("name", query)
    nameOk = name == self.nextPlayer.name
    #dummycheck
    if (self.nextPlayer == None) or (not nameOk):
      rtns["result"] = "false"
      szRtn = json.dumps(rtns)
    else:  
      virtualPlayerName = self.nextPlayer.name
      self.firstcard = virtualPlayerName == self.playersOrder[0].name
      #play automatic card
      asuit = None
      arankint = -1
      if self.bestcard != None:
        asuit = self.bestcard.suit
        arankint = self.bestcard.rankNr

      card = self.nextPlayer.getAutomaticPlaycard(asuit, arankint)
      szRtn = self.thePlayerPlayCard(name, card)
    return szRtn
  
  def playCard(self, query):
    szRtn = ""
    rtns = dict();  
    self.format = self.webparser.parseCmd("format", query)
    name = self.webparser.parseCmd("name", query)

    if name != self.nextPlayer.name:
      rtns["result"] = "false"
      szRtn = json.dumps(rtns)
      return szRtn

    self.firstcard = name == self.playersOrder[0].name
    card = None
    for p in self.players:
      if p.name == name:
        cardsuit = self.webparser.parseCmd("suit", query)
        cardrank = self.webparser.parseCmd("rank", query)
        siut = ""
        for s in carddeck.suits:
          if str(s) == cardsuit:
            suit = s
            break
        for r in carddeck.ranks:
          if str(r) == cardrank:
            rank = r
            break
        card = carddeck.Card(suit, rank)
        break
    szRes = self.thePlayerPlayCard(name, card)
    return szRes

  def thePlayerPlayCard(self, name, card):
    rtns = dict();  
    iRtn = self.playCardForPlayer(name, card)
    rtns["player"] = name
    rtns["card"] = str(card)
    rtns["result"] = "true" if iRtn != 100 else "false"
    if iRtn != 200:
      rtns["error"] = str(iRtn)
    elif iRtn == 200: #200 = Okay!
      if self.firstcard:
        self.playingSuit = card.suit
        self.firstcard = False
      self.playedcards.append(carddeck.Card(card.suit, card.rank))
      bestcard = self.getBestPlayedCard()
      self.bestcard = bestcard
      next = self.setNextPlayer()
      self.nextPlayer = next

      if next != None:
        rtns["next"] = next.name
        rtns["nextvirtual"] = "true" if next.virtual else "false"
      rtns["roundfinish"] = "true" if next == None else "false"
      rtns["playingsuit"] = str(self.playingSuit).lower()
      rtns["firstcard"] = "ture" if self.firstcard else "false"
      if self.checkthewinner:
        winner = self.checkWinner(self.playersOrder)
        rtns["winner"] = winner
        self.updatelogplayedcards()
        self.playedcards = []
        cardsleft = self.checkCardsLeft(self.playersOrder)
        rtns["cardsleft"] = cardsleft
        if cardsleft == "no":
          self.setPoints()
          self.summerygame()
          self.gamestatus = "end"
      if next == None:    
        tmpPlayers = []
        for p in self.playersOrder:
          slPlayer = {};
          slPlayer.update({"name": p.name})
          slPlayer.update({"bid": p.bid})
          slPlayer.update({"sticks": p.sticks})
          slPlayer.update({"points": p.points})
          slPlayer.update({"winner": p.winner})
          tmpPlayers.append(slPlayer)
        rtns["players"] = tmpPlayers

    szRtn = json.dumps(rtns)
    return szRtn

  def getBestPlayedCard(self):
    bestCard = None
    fsuit = None
    bfirst = True
    for card in self.playedcards:
      if bfirst:
        bestCard = card
        fsuit = bestCard.suit
        bfirst = False  
      else:    
        if card.suit == fsuit:
          if card.rankNr > bestCard.rankNr:
            bestCard = card
    
    return bestCard  

    
  def setPoints(self):
    for p in self.playersOrder:
      p.setPoints()

  def updatelogplayedcards(self):
    self.round = self.round + 1
    tmpCards = []
    i = 0
    for c in self.playedcards:
      slCards = {}
      slCards.update({"suit": c.suit})
      slCards.update({"rank": c.rank})
      if i < len(self.playersOrder):
        p = self.playersOrder[i]
        slCards.update({"player": p.name})
      else:  
        slCards.update({"player": "bug"})
      tmpCards.append(slCards)
      i = i + 1
    self.logplayedcards["round" + str(self.round)] = tmpCards

  def summerycards(self):
    for p in self.players:
      p.summerycards()

  def summerygame(self):
    for p in self.players:
      szSummary = p.summerygame() + "\n"
      #Append summery to file
      f = open("AIdata.txt", "a")
      f.write(szSummary)
      f.close()
    f = open("AIdata.txt", "a")
    rounds = len(self.logplayedcards)
    self.logplayedcards["rounds"] = rounds
    szplayedcards = json.dumps(self.logplayedcards)
    f.write(szplayedcards + "\n")
    f.close()
    self.logplayedcards.clear()
    #Append empty row to file
    f = open("AIdata.txt", "a")
    f.write("\n")
    f.close()


  def nextround(self, query):
    szRtn = ""
    self.format = self.webparser.parseCmd("format", query)
    self.playersOrder = []
    self.playersOrder = self.getPlayersOrder(self.players)
    self.firstcard = True
    szRtn = self.getLatestStatusOfGame()
    return szRtn

  def getLatestStatusOfGame(self):
    tmpPlayers = []
    for p in self.playersOrder:
      slPlayer = {};
      slPlayer.update({"name": p.name})
      slPlayer.update({"sticks": p.sticks})
      slPlayer.update({"bid": p.bid})
      slPlayer.update({"points": p.points})
      slPlayer.update({"winner": p.winner})
      tmpPlayers.append(slPlayer)
    slRet = dict()  
    slRet["result"] = "true"
    slRet["next"] = self.playersOrder[0].name

    self.cardPlayerName = self.playersOrder[0].name
    self.nextPlayer = self.playersOrder[0]
    self.bestcard = None
    self.playedcards = []

    slRet["player"] = self.cardPlayerName
    slRet["players"] = tmpPlayers
    slRet["cardsleft"] = self.checkCardsLeft(self.playersOrder)
    #szSuit = str(self.playingSuit).lower()
    #slRet["suit"] = szSuit
    slRet["firstcard"] = "true" if self.firstcard else "false"

    self.jSonV = json.dumps(slRet)
    szRtn = str(self.jSonV)
    return szRtn

  def getActualStatusOfGame(self):
    tmpPlayers = []
    for p in self.players:
      slPlayer = {}
      slPlayer.update({"name": p.name})
      slPlayer.update({"sticks": p.sticks})
      slPlayer.update({"bid": p.bid})
      slPlayer.update({"points": p.points})
      slPlayer.update({"winner": p.winner})
      slPlayer.update({"virtual": "true" if p.virtual else "false"})
      tmpPlayers.append(slPlayer)
    slRet = dict()  
    try:
      szResult = "true" if self.getPlayerForName(self.cardPlayerName).playedCardResult else "false"
      slRet["result"] = szResult
    except:
      slRet["result"] = "false"
    slRet["next"] =  self.cardPlayerName
    slRet["player"] =  self.cardPlayerName
    slRet["players"] = tmpPlayers
    slRet["cardsleft"] = self.checkCardsLeft(self.playersOrder)
    szSuit = str(self.playingSuit).lower()
    slRet["playingsuit"] = szSuit
    slRet["firstcard"] = "true" if self.firstcard else "false"
    slPlayedCards = []
    for card in self.playedcards:
      slCard = {};
      slCard.update({"suit": card.suit})
      slCard.update({"rank": card.rank})
      slPlayedCards.append(slCard)
    slRet["playedcards"] = slPlayedCards

    self.jSonV = json.dumps(slRet)
    szRtn = str(self.jSonV)
    return szRtn

  def setNextPlayer(self):
    pnext = None
    if self.cardPlayerName == "":
      return ""

    next = ""
    bNext = False
    for p in self.playersOrder:
      if bNext:
        pnext = p
        next = p.name
        self.cardPlayerName = p.name
        break
      if p.name == self.cardPlayerName:
        bNext = True

    self.checkthewinner = (bNext == True) and (len(next) <= 0)

    if len(next) <= 0:
      self.cardPlayerName = ""

    return pnext
  
  def getActualPlayer(self, query):
    player = dict();  
    player["player"] = self.cardPlayerName
    self.jSonV = json.dumps(player)
    return str(self.jSonV)


  def getPlayers(self, query):
    szRtn = ""
    self.format = self.webparser.parseCmd("format", query)
    """
      if format == "test":
        szTest = ""
        for p in self.players:
          szTest = szTest + p.name + "_"
        szRtn = szTest  
    """      
    #elif format == "json":
    tmpPlayers = []
    for p in self.players:
      tmpPlayer = {}
      tmpPlayer.update({"name": p.name})
      tmpPlayer.update({"pos": p.pos})
      tmpPlayer.update({"points": p.points})
      tmpPlayer.update({"winner": p.winner})
      tmpPlayer.update({"bid": p.bid})
      tmpPlayer.update({"sticks": p.sticks})
      tmpPlayer.update({"virtual": "true" if p.virtual else "false"})
      tmpPlayers.append(tmpPlayer)
    players = dict();  
    players["players"] = tmpPlayers
    self.jSonV = json.dumps(players)
    szRtn = str(self.jSonV)
    #else:
    """ 
        if len(self.players) > 0:
          szRtn = "<ul>"
          for p in self.players:
            szRtn = szRtn + "<li>" + str(p) + "</li> "
          szRtn = szRtn + "</ul>"  
    """
    return szRtn    

  def deal(self, query):
    self.nrofcards = self.nrofcards - 1
    szRtn = ""
    self.format = self.webparser.parseCmd("format", query)
    #"idle", "playeradd", "deal", "start", "end"
    if self.gamestatus in ["idle", "deal", "start"]:
      players = dict();  
      players["result"] = "false"
      self.jSonV = json.dumps(players)
      szRtn = str(self.jSonV)
    elif len(self.players) > 0:
      self.dealCard()
      
      self.summerycards()
      tmpPlayers = [];
      for p in self.players:
        slPlayer = {};
        slPlayer.update({"name": p.name})
        szCards = p.showcards()
        slPlayer.update({"cards": szCards})
        tmpPlayers.append(slPlayer)
      players = dict()
      players["result"] = "true"
      players["players"] = tmpPlayers
      players["nrofcards"] = str(self.nrofcards)
      self.jSonV = json.dumps(players)
      szRtn = str(self.jSonV)
      self.gamestatus = "deal"

    return szRtn

  def start(self, query):
    self.round = 0
    self.gamestatus = "start"
    self.format = self.webparser.parseCmd("format", query)

    self.playersOrder = []
    self.playersOrder = self.getPlayersOrderWithToken(self.players, self.tokenName)
    self.tokenName = self.setNextToken(self.players, self.tokenName)
    tmpPlayers = []
    for p in self.playersOrder:
      p.bid = 0
      p.sticks = 0
      slPlayer = {}
      slPlayer.update({"name": p.name})
      virtual = "true" if p.virtual else "false"
      slPlayer.update({"virtual": virtual})
      tmpPlayers.append(slPlayer)
    slRet = dict()  
    slRet["result"] = "true"
    slRet["next"] = self.playersOrder[0].name
    self.cardPlayerName = self.playersOrder[0].name
    slRet["playersorder"] = tmpPlayers
    self.jSonV = json.dumps(slRet)
    szRtn = str(self.jSonV)
    return szRtn

  def setNextToken(self, players, tokenName):
    bNext = False
    bfound = False
    newTokenName = ""
    for p in players:
      if p.name == tokenName:
        bNext = True
      else:
        if bNext:
          newTokenName = p.name
          bfound = True
          break

    if bfound == False:
      for p in players:
        newTokenName = p.name
        break

    return newTokenName  


  def getPlayersOrderWithToken(self, players, token):
    playersOrder = []
    found = False
  
    for p in players:
      if p.name == token:
        found = True      
      else:   
        if found:
          playersOrder.append(p)
            
  
    if found == True:
      for p in players:
        if p.name == token:
          playersOrder.append(p)  
          break
        else:  
          playersOrder.append(p)  
    else:
      playersOrder = []
      for p in players:
        playersOrder.append(p)
    return playersOrder
  
  def getPlayersOrder(self, players):
    playersOrder = []
    found = False
  
    for p in players:
      if p.winner:
        #print("Winner!: " + str(p))
        found = True      
      if found:
        #print("Append (found):" + str(p))
        playersOrder.append(p)
            
  
    if found == True:
      #print("Found winner")
      for p in players:
        if p.winner:
          #print("Set winner")
          p.setWinner(False)
          break
        else:  
          #print("Append (x2):" + str(p))
          playersOrder.append(p)  
    else:
      playersOrder = []
      for p in players:
        #print("Append (x3):" + str(p))
        playersOrder.append(p)
    return playersOrder
  
  def checkCardsLeft(self, playersOrder):
    cardsleft = "no"
    for p in playersOrder:
      if p.cardsleft() > 0:
        cardsleft = "yes"
    return cardsleft

  def checkWinner(self, playersOrder):
    theWinner = ""
  
    bfirst = True 
    for p in playersOrder:
      #print("Test showcard x1 " + str(p))
      #p.showcards()
      if bfirst:
        bestCard = p.getPlayedCard()
        fsuit = bestCard.suit
        #print("Bestcard1:" + str(bestCard))
        #if fsuit != bestCard.suit:
        #  print("suit error")
        bfirst = False  
      else:    
        card = p.getPlayedCard()
        #print("card1:" + str(card))
        if card.suit == fsuit:
          if card.rankNr > bestCard.rankNr:
            bestCard = card
            #print("Bestcard2:" + str(bestCard))
    for p in playersOrder:
      bwinner = bestCard == p.getPlayedCard()
      p.setWinner(bwinner)
      if bwinner:
        p.addSticks(1);
        theWinner = p
  
    #print("TheWinner (x3):" + str(theWinner))
    #print("Best card:" + str(bestCard))

    #for p in playersOrder:
      #print("Test showcard x2 " + str(p))
      #p.showcards()
    self.winner = theWinner.name  
    return theWinner.name  

  def addPlayerToGame(self, name, virtual):
    result = False
    iPos = -1
    #gameStatus = set(("idle", "playeradd", "deal", "start", "end"))
    if self.gamestatus in ["deal",  "start", "end"]:
      result = False
    elif len(name)<=0:
      result = False
    elif self.nameExist(name):
      result = False
    else:  
      iPos = len(self.players)
      aPlayer = player.Player(name, iPos)
      aPlayer.virtual = virtual
      self.players.append(aPlayer)
      self.tokenName = name
      result = True

    if result:
      self.gamestatus = "playeradd"

    slResult = dict();
    slResult["name"] = name
    slResult["pos"] = iPos
    slResult["virtual"] = "true" if virtual else "false"
    slResult["result"] = "true" if result else "false"
    self.jSonV = json.dumps(slResult)
    return self.jSonV

  def nameExist(self, name):
    exist = False
    for p in self.players:
      if name.lower() == p.name.lower():
        exist = True
        break
    return exist

  def playCardForPlayer(self, name, card):
    iRtn = 100
    for p in self.players:
      if p.name == name:
        iRtn = p.playerPlayCard(card)
        break
    return iRtn  
  
  def dealCard(self):
    self.cardDeck.createDeck()
    self.cardDeck.shuffle()  
    #deal cards
    n = 0
    while n < self.nrofcards:
      for p in self.players:
        if self.cardDeck.cardleft:
          p.addcard(self.cardDeck.getcard())
      n += 1
    

  

    