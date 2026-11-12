from dataclasses import dataclass
from typing import Optional, List
from combat import Battle, Outcome
from core import Dice, UnknownCodeException
from enemies import Goblin, Skeleton, Dragon
from items import Item, DefaultCatalog

@dataclass(frozen=True)
class Rewards:
    experience: int
    gold: int
    loot: Optional[Item]
    levels_gained: int

@dataclass(frozen=True)
class ExpeditionReport:
    seed: int
    location_code: str
    battle: 'BattleReport'
    rewards: Rewards

class Location:
    LOOT_CHANCE = 0.6
    ENCHANT_CHANCE = 0.3

    def __init__(self, code, display_name, recommended_level, catalog):
        self.code = code
        self.display_name = display_name
        self.recommended_level = recommended_level
        self.catalog = catalog

    def create_enemy(self): pass
    def get_loot_table(self): pass

    def explore(self, hero, seed=None):
        if seed is None:
            seed = Dice.get_instance().next_seed()

        dice = Dice.get_instance()
        dice.reseed(seed)
        hero.restore_health()

        enemy = self.create_enemy()
        battle_report = Battle(hero, enemy).run()

        if battle_report.outcome == Outcome.VICTORY:
            exp = enemy.get_experience_reward()
            gold = enemy.roll_gold_reward()
            loot = self._roll_loot(dice)
            levels = hero.gain_experience(exp)
            hero.add_gold(gold)
            if loot: hero.add_item(loot)
            rewards = Rewards(exp, gold, loot, levels)
        else:
            lost_gold = hero.gold // 2
            hero.spend_gold(lost_gold)
            rewards = Rewards(0, -lost_gold, None, 0)

        return ExpeditionReport(seed, self.code, battle_report, rewards)

    def _roll_loot(self, dice):
        if not dice.chance(self.LOOT_CHANCE): return None
        loot = self.catalog.create(dice.pick(self.get_loot_table()))
        if dice.chance(self.ENCHANT_CHANCE):
            loot.enchant(dice.pick(loot.get_possible_enchantments()))
        return loot

class Forest(Location):
    CODE = "forest"
    def __init__(self, catalog): super().__init__(self.CODE, "Мистический лес", 1, catalog)
    def create_enemy(self): return Goblin()
    def get_loot_table(self): return [DefaultCatalog.GOBLIN_CLEAVER, DefaultCatalog.HUNTING_BOW, DefaultCatalog.LEATHER_ARMOR]

class Crypt(Location):
    CODE = "crypt"
    def __init__(self, catalog): super().__init__(self.CODE, "Заброшенный склеп", 3, catalog)
    def create_enemy(self): return Skeleton()
    def get_loot_table(self):
        return [DefaultCatalog.KNIGHT_BLADE, DefaultCatalog.BONE_BOW, DefaultCatalog.NECROMANCER_STAFF, DefaultCatalog.CRYPT_MAIL]

class DragonLair(Location):
    CODE = "dragon-lair"
    def __init__(self, catalog): super().__init__(self.CODE, "Логово дракона", 5, catalog)
    def create_enemy(self): return Dragon()
    def get_loot_table(self): return [DefaultCatalog.DAWN_BLADE, DefaultCatalog.DRAGONSCALE_ARMOR]

class LocationRegistry:
    def __init__(self, locations):
        self.locations = {loc.code: loc for loc in locations}

    def get(self, code):
        if code not in self.locations:
            raise UnknownCodeException("Локация", code)
        return self.locations[code]

    def get_all(self):
        return list(self.locations.values())