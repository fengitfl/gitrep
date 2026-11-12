from dataclasses import dataclass
from core import Dice, UnknownCodeException
from combat import Hit

@dataclass(frozen=True)
class Enchantment:
    code: str
    name: str
    bonus_damage: int
    bonus_defense: float
    bonus_price: int

SHARP = Enchantment("sharp", "Острое", 3, 0, 20)
FIERY = Enchantment("fiery", "Огненное", 6, 0, 50)
STURDY = Enchantment("sturdy", "Прочное", 0, 0.05, 20)
WARDING = Enchantment("warding", "Охранное", 0, 0.10, 50)

FOR_WEAPONS = [SHARP, FIERY]
FOR_ARMOR = [STURDY, WARDING]

class Item:
    def __init__(self, code, name, base_price):
        self.code = code
        self.name = name
        self.base_price = base_price
        self.enchantments = []

    def copy(self):
        raise NotImplementedError

    def get_possible_enchantments(self):
        return []

    def get_description(self):
        raise NotImplementedError

    def enchant(self, enchantment):
        if enchantment not in self.get_possible_enchantments():
            raise ValueError(f"Зачарование '{enchantment.name}' не подходит для предмета '{self.name}'")
        self.enchantments.append(enchantment)

    def get_code(self): return self.code
    def get_name(self): return self.name

    def get_price(self):
        return self.base_price + sum(e.bonus_price for e in self.enchantments)

    def get_enchantments(self):
        return list(self.enchantments)

class Weapon(Item):
    def __init__(self, code, name, base_price, damage):
        super().__init__(code, name, base_price)
        self.damage = damage

    def roll_damage(self): pass

    def get_damage(self):
        return self.damage + sum(e.bonus_damage for e in self.enchantments)

    def get_possible_enchantments(self):
        return FOR_WEAPONS

class Sword(Weapon):
    def copy(self): return Sword(self.code, self.name, self.base_price, self.damage)
    def roll_damage(self): return Hit(self.get_damage(), False)
    def get_description(self): return f"урон {self.get_damage()}"

class Bow(Weapon):
    def __init__(self, code, name, base_price, damage, critical_chance):
        super().__init__(code, name, base_price, damage)
        self.critical_chance = critical_chance

    def copy(self): return Bow(self.code, self.name, self.base_price, self.damage, self.critical_chance)
    
    def roll_damage(self):
        if Dice.get_instance().chance(self.critical_chance):
            return Hit(self.get_damage() * 2, True)
        return Hit(self.get_damage(), False)

    def get_description(self): return f"урон {self.get_damage()}, шанс крита {round(self.critical_chance * 100)}%"

class Staff(Weapon):
    def __init__(self, code, name, base_price, damage, scatter):
        super().__init__(code, name, base_price, damage)
        self.scatter = scatter

    def copy(self): return Staff(self.code, self.name, self.base_price, self.damage, self.scatter)
    
    def roll_damage(self):
        min_dmg = round(self.get_damage() * (1 - self.scatter))
        max_dmg = round(self.get_damage() * (1 + self.scatter))
        return Hit(Dice.get_instance().roll(min_dmg, max_dmg), False)

    def get_description(self):
        min_dmg = round(self.get_damage() * (1 - self.scatter))
        max_dmg = round(self.get_damage() * (1 + self.scatter))
        return f"урон {min_dmg}-{max_dmg}"

class Armor(Item):
    MAX_DEFENSE = 0.75
    def __init__(self, code, name, base_price, defense):
        super().__init__(code, name, base_price)
        self.defense = defense

    def copy(self): return Armor(self.code, self.name, self.base_price, self.defense)
    def get_possible_enchantments(self): return FOR_ARMOR
    
    def get_defense(self):
        return min(self.defense + sum(e.bonus_defense for e in self.enchantments), self.MAX_DEFENSE)

    def get_description(self): return f"защита {round(self.get_defense() * 100)}%"

class ItemCatalog:
    def __init__(self):
        self.prototypes = {}

    def register(self, prototype):
        self.prototypes[prototype.get_code()] = prototype

    def create(self, code):
        if code not in self.prototypes:
            raise UnknownCodeException("Предмет", code)
        return self.prototypes[code].copy()

    def create_weapon(self, code):
        item = self.create(code)
        if not isinstance(item, Weapon):
            raise ValueError(f"Предмет '{code}' не является оружием")
        return item

    def create_armor(self, code):
        item = self.create(code)
        if not isinstance(item, Armor):
            raise ValueError(f"Предмет '{code}' не является броней")
        return item

    def get_codes(self): return list(self.prototypes.keys())

class DefaultCatalog:
    TRAINING_SWORD = "training-sword"
    HUNTING_BOW = "hunting-bow"
    APPRENTICE_STAFF = "apprentice-staff"
    CHAINMAIL = "chainmail"
    LEATHER_ARMOR = "leather-armor"
    LINEN_ROBE = "linen-robe"
    IRON_SWORD = "iron-sword"
    ELVEN_BOW = "elven-bow"
    EMBER_STAFF = "ember-staff"
    PLATE_ARMOR = "plate-armor"
    GOBLIN_CLEAVER = "goblin-cleaver"
    BONE_BOW = "bone-bow"
    NECROMANCER_STAFF = "necromancer-staff"
    KNIGHT_BLADE = "knight-blade"
    CRYPT_MAIL = "crypt-mail"
    DAWN_BLADE = "dawn-blade"
    DRAGONSCALE_ARMOR = "dragonscale-armor"

    @staticmethod
    def create():
        catalog = ItemCatalog()
        catalog.register(Sword(DefaultCatalog.TRAINING_SWORD, "Тренировочный меч", 20, 12))
        catalog.register(Bow(DefaultCatalog.HUNTING_BOW, "Охотничий лук", 20, 10, 0.3))
        catalog.register(Staff(DefaultCatalog.APPRENTICE_STAFF, "Посох ученика", 20, 14, 0.3))
        catalog.register(Armor(DefaultCatalog.CHAINMAIL, "Кольчуга", 40, 0.3))
        catalog.register(Armor(DefaultCatalog.LEATHER_ARMOR, "Кожаная броня", 30, 0.2))
        catalog.register(Armor(DefaultCatalog.LINEN_ROBE, "Льняная роба", 15, 0.1))
        catalog.register(Sword(DefaultCatalog.IRON_SWORD, "Железный меч", 80, 17))
        catalog.register(Bow(DefaultCatalog.ELVEN_BOW, "Эльфийский лук", 90, 14, 0.4))
        catalog.register(Staff(DefaultCatalog.EMBER_STAFF, "Тлеющий посох", 90, 20, 0.3))
        catalog.register(Armor(DefaultCatalog.PLATE_ARMOR, "Латы", 120, 0.4))
        catalog.register(Sword(DefaultCatalog.GOBLIN_CLEAVER, "Гоблинский тесак", 40, 15))
        catalog.register(Bow(DefaultCatalog.BONE_BOW, "Костяной лук", 140, 17, 0.4))
        catalog.register(Staff(DefaultCatalog.NECROMANCER_STAFF, "Посох некроманта", 150, 25, 0.35))
        catalog.register(Sword(DefaultCatalog.KNIGHT_BLADE, "Клинок рыцаря", 150, 23))
        catalog.register(Armor(DefaultCatalog.CRYPT_MAIL, "Кольчуга стража склепа", 160, 0.45))
        catalog.register(Sword(DefaultCatalog.DAWN_BLADE, "Клинок рассвета", 500, 35))
        catalog.register(Armor(DefaultCatalog.DRAGONSCALE_ARMOR, "Драконья чешуя", 500, 0.55))
        return catalog