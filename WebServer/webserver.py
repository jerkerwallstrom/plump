# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import time
import json
#how to import from "C:\Users\A403326\OneDrive - AFRY\Documents\Python\CardGame" 
import carddeck
import game
from io import BytesIO

hostName = "localhost"
serverPort = 8080

CORS_ORIGIN_WHITELIST = ('http://localhost:8080')

game = game.Game()
game.addPlayer("Test1")

class MyServer(BaseHTTPRequestHandler):
    '''
    #def do_GET(self):
    #    self.send_response(200)
    #    self.send_header("Content-type", "text/html")
    #    self.end_headers()
    #    self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
    #    self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
    #    self.wfile.write(bytes("<body>", "utf-8"))
    #    self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
    #    self.wfile.write(bytes("</body></html>", "utf-8"))
    '''
    '''
    def _set_headers(self):
        #self.send_response(200)
        #self.send_header('Content-type', 'application/json')
        #self.end_headers()
        #self.send_response(200)
        #self.send_header("Content-type", "text/html")
        #self.end_headers()
    ''' 

    def do_GET(self):
      #self._set_headers()
      query = urlparse(self.path).query
      szResult = game.Handle(query)

      #jsonStr = json.dumps(szResult)

      if game.format == "json":        
        try:
          message = bytes(szResult, 'utf-8')
          self.send_response(200)
          self.send_header('Access-Control-Allow-Origin', '*')
          self.send_header('Content-type', 'application/json; charset=utf-8')
          self.send_header('Content-length', str(len(message)))
          self.end_headers()    
          #szJsonTmp = game.jSonV
          self.wfile.write(message)
        except:
          self.send_response(100)
        filename = "readme.txt"  
        if len(game.function) > 0:
          filename = game.function  + ".txt"
        with open(filename, 'w') as f:
           f.write(szResult)  
      elif game.format == "test":    
        #jsonStr = bytes("{\"result\": 1};", 'utf-8')
        message = bytes(szResult, 'utf-8')
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Content-length', str(len(message)))
        self.end_headers()
        self.wfile.write(message)
      else:
        if len(szResult) > 0:    
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.end_headers()
          self.wfile.write(bytes("<html><head><title>Card Game Test</title></head>", "utf-8"))
          #if game.function == "getplayers":
          #  szPath = "http://localhost:8080/getplayers"
          #  self.wfile.write(bytes("<p>Request: %s</p>" % szPath, "utf-8"))
          
          self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
          self.wfile.write(bytes("<body>", "utf-8"))
          self.wfile.write(bytes("<p>" + szResult + "</p>", "utf-8"))
          self.wfile.write(bytes("</body></html>", "utf-8"))
        else:
          self.send_response(100)

        return  

    def do_POST(self):
      query = "func=getplayers&format=test"
      szResult = game.Handle(query)

      message = bytes(szResult, 'utf-8')
      #message = bytes(str(self.headers) + "\n" + self.requestline + "\n", 'utf8')
      self.send_response(200)
      #self.send_header('Content-type', 'text/plain; charset=utf-8')
      #self.send_header('Content-length', str(len(message)))
      self.end_headers()
      self.wfile.write(message)

      return

    

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")