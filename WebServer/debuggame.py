import game
import json

def test():
  aGame = game.Game()
  szRtn = aGame.Handle("?name=lisa&func=addplayer")
  print(szRtn)

  szRtn = aGame.Handle("?name=kalle&func=addplayer")
  print(szRtn)

  szRtn = aGame.Handle("?name=sluggo&func=addplayer")
  print(szRtn)
  
  szRtn = aGame.Handle("?name=sluggo&func=getplayers")
  print(szRtn)

  szRtn = aGame.Handle("?func=getplayers&format=json")
  print(szRtn)
  
  szRtn = aGame.Handle("?func=deal")
  print(szRtn)

  szRtn = aGame.Handle("?func=getcards&name=kalle")
  print(szRtn)

  cards = json.loads(szRtn)
  szCards = cards["cards"]
  for szCard in szCards:
    suit = szCard["suit"]
    rank = szCard["rank"]
    txt = "?func=playcard&name=kalle&suit={}&rank={}"
    txt = txt.format(suit, rank)
    szRtn = aGame.Handle(txt)
    print(szRtn + " = " + suit + " " + rank)

  exit = input("Exit?")
  return exit

test()  
