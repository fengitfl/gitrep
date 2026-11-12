from dataclasses import dataclass
from typing import List
from enum import Enum

@dataclass(frozen=True)
class Hit:
    damage: int
    critical: bool

class Side(Enum):
    HERO = 1
    ENEMY = 2

class EventType(Enum):
    HIT = 1
    CRITICAL_HIT = 2
    DEATH = 3

class Outcome(Enum):
    VICTORY = 1
    DEFEAT = 2

@dataclass(frozen=True)
class BattleEvent:
    round: int
    type: EventType
    source: Side
    target: Side
    amount: int
    target_health_after: int

@dataclass(frozen=True)
class Participant:
    code: str
    name: str
    max_health: int

    @classmethod
    def of(cls, combatant):
        return cls(combatant.get_code(), combatant.get_name(), combatant.get_max_health())

@dataclass(frozen=True)
class BattleReport:
    hero: Participant
    enemy: Participant
    outcome: Outcome
    events: List[BattleEvent]

class Combatant:
    def get_code(self) -> str: pass
    def get_name(self) -> str: pass
    def get_health(self) -> int: pass
    def get_max_health(self) -> int: pass
    def is_alive(self) -> bool: pass
    def roll_damage(self) -> Hit: pass
    def receive_hit(self, damage: int) -> int: pass

class Battle:
    def __init__(self, hero: Combatant, enemy: Combatant):
        self.hero = hero
        self.enemy = enemy
        self.events = []
        self.round = 0

    def run(self) -> BattleReport:
        while self.hero.is_alive() and self.enemy.is_alive():
            self.round += 1
            self._strike(self.hero, Side.HERO, self.enemy, Side.ENEMY)
            if self.enemy.is_alive():
                self._strike(self.enemy, Side.ENEMY, self.hero, Side.HERO)

        outcome = Outcome.VICTORY if self.hero.is_alive() else Outcome.DEFEAT
        return BattleReport(Participant.of(self.hero), Participant.of(self.enemy), outcome, self.events)

    def _strike(self, attacker: Combatant, source: Side, defender: Combatant, target: Side):
        hit = attacker.roll_damage()
        dealt = defender.receive_hit(hit.damage)
        event_type = EventType.CRITICAL_HIT if hit.critical else EventType.HIT
        self.events.append(BattleEvent(self.round, event_type, source, target, dealt, defender.get_health()))
        
        if not defender.is_alive():
            self.events.append(BattleEvent(self.round, EventType.DEATH, source, target, 0, 0))