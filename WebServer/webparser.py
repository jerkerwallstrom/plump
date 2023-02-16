#python module/class webParser

class webParser:
  
  def __init__(self):
    self.result = 100
    self.szResult = ""
    self.function = ""

  def getFunction(self, query):
    szFunc = self.parseFunction(query)
    self.function = szFunc
    return self.function

  def parseFunction(self, query):
    func = ""
    szTmp = query.lower()
    iFind = szTmp.find("func=")
    if iFind < 0:
      return "no_function"
    index = szTmp.index("func=")
    iMax = len(szTmp)
    szTmp = szTmp[index+5:iMax]
    if szTmp.find("&") > 0:
      iEnd = szTmp.index("&")
      func = szTmp[0:iEnd]
    elif szTmp.find("?") > 0:
      iEnd = szTmp.index("?")
      func = szTmp[0:iEnd]
    else:
      func = szTmp
    return func.lower()


  def parseCmd(self, param, query):
    result = self.getParameter(param, query)
    return result

  def getParameter(self, param, query):
    iLen = len(param)
    if iLen <= 0:
      return "error"
    szTmp = query
    szTmp = szTmp.lower()
    iFind = szTmp.find(param)
    if iFind < 0:
      return ""
    index = szTmp.index(param)
    iMax = len(szTmp)
    szTmp = szTmp[index+iLen+1:iMax]
    if szTmp.find("&") > 0:
      iEnd = szTmp.index("&")
      value = szTmp[0:iEnd]
    elif szTmp.find("?") > 0:
      iEnd = szTmp.index("?")
      value = szTmp[0:iEnd]
    else:
      value = szTmp
    return value  
    #return name.capitalize()
        