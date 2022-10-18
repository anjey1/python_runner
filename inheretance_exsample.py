class Pokemon():
  def __init__(self, name='default2'):
    self.name = name

  def printname(self):
    print('my name is: ',self.name)
    

class Fire(Pokemon):
  def __init__(self, name):
    super().__init__()
    self.type = 'fire'
    self.name = name

  def printtype(self):
    print('my type is: ', self.type)

class Water(Pokemon):
  def __init__(self, name = 'Water'):
    super().__init__()
    self.type = 'water'
    self.name = name

  def printtype(self):
    print('my type is: ', self.type)


class Magikarp(Water):
  def __init__(self, name='Magikarp'):
    super().__init__()
    self.name = name
    
  def Splash(self):
    print('Splash Attack !!', self.type)

pokemon1 = Water('Moshe')
pokemon2 = Fire('Avi')
magi = Magikarp()

pokemon1.printname()
pokemon1.printtype()

pokemon2.printname()
pokemon2.printtype()

magi.printname()
magi.printtype()
magi.Splash()