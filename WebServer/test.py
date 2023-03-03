import game

game = game.Game()

res = game.addPlayerToGame("jerka", False)
print(res)
res = game.addPlayerToGame("virre", True)
print(res)
res = game.addPlayerToGame("pirlo", True)
print(res)

res = game.setNumberOfCards()
print(res)
res = game.dealCard()
print(res)
res = game.summerycards()
print(res)
res = game.startTheGame()
print(res)

res = game.setBidSticksForPlayer("jerka", 2, False)
print(res)
res = game.setBidSticksForPlayer("virre", 0, True)
print(res)
res = game.setBidSticksForPlayer("pirlo", 0, True)
print(res)
#first played card
next = game.nextPlayer.name
res = game.playTheVirtualCardFor(next)
next = game.nextPlayer.name
res = game.playTheVirtualCardFor(next)
next = game.nextPlayer.name
res = game.playTheVirtualCardFor(next)

res = game.getLatestStatusOfGame()
#second played card
if game.nextPlayer == None:
  next = game.winner  
else:
  next = game.nextPlayer.name
    
res = game.playTheVirtualCardFor(next)
next = game.nextPlayer.name
res = game.playTheVirtualCardFor(next)
next = game.nextPlayer.name
res = game.playTheVirtualCardFor(next)

print(res)
