class Monster:

  def __init__(self):
      self.id = 0
      self.avatar = ""
      self.image = ""
      self.name = ""
      self.type = ""
      self.element = []
      self.rarity = 0
      self.cost = 0
      self.monsterpoints = 0
      self.maxlvl = 0
      self.baseatk = 0
      self.basehp = 0
      self.basercv = 0
      self.maxatk = 0
      self.maxhp = 0
      self.maxrcv = 0
      self.evolutions = []

  def info(self):
      print("ID: " + str(self.id))
      print("Name: " + self.name)
      print("Avatar: " + self.avatar)
      print("Image: " + self.image)
      print("Type: " + str(self.type))
      print("Rarity: " + str(self.rarity))
      print("Evolutions: " + str(self.evolutions))
