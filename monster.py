class Monster:

  def __init__(self):
      self.id = 0
      self.avatar = ""
      self.image = ""
      self.en_name = ""
      self.jp_name = ""
      self.type = ""
      self.element = []
      self.rarity = 0
      self.cost = 0
      self.monster_points = 0
      self.min_level = 0
      self.max_level = 0
      self.base_atk = 0
      self.base_hp = 0
      self.base_rcv = 0
      self.max_atk = 0
      self.max_hp = 0
      self.max_rcv = 0
      self.base_weighted_stats = 0
      self.max_weighted_stats = 0
      self.max_exp = 0
      self.exp_curve = 0
      self.active_skill = ""
      self.active_skill_description = ""
      self.active_skill_cooldown = ""
      self.same_active_skill = []
      self.leader_skill = ""
      self.leader_skill_description = ""
      self.awakenings = []
      self.evolutions = []

  def info(self):
      print("ID: " + str(self.id))
      print("EN Name: " + self.en_name)
      print("JP Name: " + self.jp_name)
      print("Avatar: " + self.avatar)
      print("Image: " + self.image)
      print("Type: " + str(self.type))
      print("Element: " + str(self.element))
      print("Rarity: " + str(self.rarity))
      print("Cost: " + str(self.cost))
      print("Monster Points: " + str(self.monster_points))
      print("Min Level: " + str(self.min_level))
      print("Base HP: " + str(self.base_hp))
      print("Base ATK: " + str(self.base_atk))
      print("Base RCV: " + str(self.base_rcv))
      print("Max Level: " + str(self.max_level))
      print("Max HP: " + str(self.max_hp))
      print("Max ATK: " + str(self.max_atk))
      print("Max RCV: " + str(self.max_rcv))
      print("Base Weighted Stats: " + str(self.base_weighted_stats))
      print("Max Weighted Stats: " + str(self.max_weighted_stats))
      print("Growth Curve: " + str(self.exp_curve))
      print("Max EXP: " + str(self.max_exp))
      print("Active Skill: " + self.active_skill)
      print("Active Skill Description: " + self.active_skill_description)
      print("Active Skill Cooldown: " + self.active_skill_cooldown)
      print("Same Active Skill: " + str(self.same_active_skill))
      print("Leader Skill: " + self.leader_skill)
      print("Leader Skill Description: " + self.leader_skill_description)
      print("Awakenings: " + str(self.awakenings))
      print("Evolutions: " + str(self.evolutions))
