from combat import Combatant, Hit
from items import Weapon, Armor
from kit import WarriorKitFactory, RangerKitFactory, MageKitFactory
from core import UnknownCodeException

class HeroClass:
    def __init__(self, code, display_name, base_health, kit_factory_class):
        self.code = code
        self.display_name = display_name
        self.base_health = base_health
        self.kit_factory_class = kit_factory_class

    def get_starter_kit(self, catalog):
        return self.kit_factory_class(catalog)

    @staticmethod
    def get_all():
        return [
            HeroClass("warrior", "Воин", 120, WarriorKitFactory),
            HeroClass("ranger", "Следопыт", 100, RangerKitFactory),
            HeroClass("mage", "Маг", 85, MageKitFactory)
        ]

    @staticmethod
    def by_code(code):
        for hc in HeroClass.get_all():
            if hc.code == code:
                return hc
        raise UnknownCodeException("Класс героя", code)

class Hero(Combatant):
    MAX_NAME_LENGTH = 20
    STARTING_GOLD = 50
    HEALTH_PER_LEVEL = 15
    DAMAGE_PER_LEVEL = 3
    EXPERIENCE_PER_LEVEL = 100

    class Builder:
        def __init__(self):
            self.name = None
            self.hero_class = None
            self.weapon = None
            self.armor = None
            self.level = 1
            self.gold = Hero.STARTING_GOLD

        def set_name(self, name):
            self.name = name
            return self

        def set_hero_class(self, hero_class):
            self.hero_class = hero_class
            return self

        def set_weapon(self, weapon):
            self.weapon = weapon
            return self

        def set_armor(self, armor):
            self.armor = armor
            return self

        def set_starter_kit(self, starter_kit):
            self.weapon = starter_kit.create_weapon()
            self.armor = starter_kit.create_armor()
            return self

        def set_level(self, level):
            self.level = level
            return self

        def set_gold(self, gold):
            self.gold = gold
            return self

        def build(self):
            if not self.name or not self.name.strip():
                raise ValueError("У героя должно быть имя")
            if len(self.name) > Hero.MAX_NAME_LENGTH:
                raise ValueError(f"Имя героя не может быть длиннее {Hero.MAX_NAME_LENGTH} символов")
            if not self.hero_class:
                raise ValueError("Не выбран класс героя")
            if not self.weapon or not self.armor:
                raise ValueError("Герою нужны оружие и броня")
            if self.level < 1:
                raise ValueError("Уровень героя не может быть меньше 1")
            if self.gold < 0:
                raise ValueError("Золота не может быть меньше нуля")
            return Hero(self)

    def __init__(self, builder: Builder):
        self.name = builder.name
        self.hero_class = builder.hero_class
        self.level = builder.level
        self.experience = 0
        self.gold = builder.gold
        self.weapon = builder.weapon
        self.armor = builder.armor
        self.inventory = []
        self.health = self.get_max_health()

    def roll_damage(self):
        hit = self.weapon.roll_damage()
        return Hit(hit.damage + (self.level - 1) * self.DAMAGE_PER_LEVEL, hit.critical)

    def receive_hit(self, damage):
        reduced = round(damage * (1 - self.armor.get_defense()))
        dealt = max(1, reduced)
        self.health = max(0, self.health - dealt)
        return dealt

    def is_alive(self): return self.health > 0
    def restore_health(self): self.health = self.get_max_health()

    def gain_experience(self, amount):
        self.experience += amount
        levels_gained = 0
        while self.experience >= self.get_experience_to_next_level():
            self.experience -= self.get_experience_to_next_level()
            self.level += 1
            levels_gained += 1
        return levels_gained

    def add_gold(self, amount): self.gold += amount

    def spend_gold(self, amount):
        if amount > self.gold:
            raise RuntimeError(f"Не хватает золота: нужно {amount}, есть {self.gold}")
        self.gold -= amount

    def add_item(self, item): self.inventory.append(item)

    def remove_item(self, item):
        if item not in self.inventory:
            raise ValueError(f"В инвентаре нет предмета {item.get_name()}")
        self.inventory.remove(item)

    def equip(self, item):
        if isinstance(item, Weapon):
            self.remove_item(item)
            self.inventory.append(self.weapon)
            self.weapon = item
        elif isinstance(item, Armor):
            self.remove_item(item)
            self.inventory.append(self.armor)
            self.armor = item
        else:
            raise ValueError(f"Предмет нельзя экипировать: {item.get_name()}")

    def get_code(self): return self.hero_class.code
    def get_name(self): return self.name
    def get_health(self): return self.health
    def get_max_health(self): return self.hero_class.base_health + (self.level - 1) * self.HEALTH_PER_LEVEL
    def get_experience_to_next_level(self): return self.level * self.EXPERIENCE_PER_LEVEL
    def get_inventory(self): return list(self.inventory)