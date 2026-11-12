from combat import Combatant, Hit
from core import Dice

class Enemy(Combatant):
    def get_experience_reward(self): pass
    def roll_gold_reward(self): pass

class AbstractEnemy(Enemy):
    def __init__(self, code, name, max_health, min_damage, max_damage, exp_reward, gold_reward):
        self.code = code
        self.name = name
        self.max_health = max_health
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.health = max_health

    def roll_damage(self):
        return Hit(Dice.get_instance().roll(self.min_damage, self.max_damage), False)

    def receive_hit(self, damage):
        dealt = max(1, self._reduce_damage(damage))
        self.health = max(0, self.health - dealt)
        return dealt

    def _reduce_damage(self, damage): return damage
    def is_alive(self): return self.health > 0
    def roll_gold_reward(self): return Dice.get_instance().roll(self.gold_reward // 2, self.gold_reward)
    def get_experience_reward(self): return self.exp_reward
    def get_code(self): return self.code
    def get_name(self): return self.name
    def get_health(self): return self.health
    def get_max_health(self): return self.max_health

class Goblin(AbstractEnemy):
    def __init__(self):
        super().__init__("goblin", "Гоблин", 50, 6, 14, 40, 30)

class Skeleton(AbstractEnemy):
    RESISTANCE = 0.3
    def __init__(self):
        super().__init__("skeleton", "Скелет", 110, 10, 24, 90, 70)
    def _reduce_damage(self, damage):
        return round(damage * (1 - self.RESISTANCE))

class Dragon(AbstractEnemy):
    RESISTANCE = 0.25
    FIRE_BREATH_CHANCE = 0.25
    def __init__(self):
        super().__init__("dragon", "Дракон", 260, 16, 22, 500, 400)

    def roll_damage(self):
        bite = super().roll_damage()
        if Dice.get_instance().chance(self.FIRE_BREATH_CHANCE):
            return Hit(bite.damage * 2, True)
        return bite

    def _reduce_damage(self, damage):
        return round(damage * (1 - self.RESISTANCE))
    