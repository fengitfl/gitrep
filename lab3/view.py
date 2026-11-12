from combat import Outcome, Side, EventType

class ConsoleView:
    def describe(self, item):
        desc = item.get_name()
        enchants = item.get_enchantments()
        if enchants:
            desc += f" [{', '.join(e.name for e in enchants)}]"
        return f"{desc} ({item.get_description()})"

    def print_hero(self, hero):
        print(f"{hero.get_name()}, {hero.hero_class.display_name} {hero.level} ур. | "
              f"здоровье {hero.get_max_health()} | опыт {hero.experience}/{hero.get_experience_to_next_level()} | золото {hero.gold}")
        print(f"  Оружие: {self.describe(hero.weapon)}")
        print(f"  Броня:  {self.describe(hero.armor)}")

    def print_report(self, report, location_name):
        battle = report.battle
        print(f"=== {location_name} (сид {report.seed}) ===")
        print(f"{battle.hero.name} встречает врага: {battle.enemy.name} ({battle.enemy.max_health} здоровья)")

        for e in battle.events:
            source = battle.hero.name if e.source == Side.HERO else battle.enemy.name
            target = battle.hero.name if e.target == Side.HERO else battle.enemy.name
            target_max_hp = battle.hero.max_health if e.target == Side.HERO else battle.enemy.max_health

            if e.type == EventType.HIT:
                print(f"[раунд {e.round}] {source} -> {target}: {e.amount} урона, осталось {e.target_health_after}/{target_max_hp}")
            elif e.type == EventType.CRITICAL_HIT:
                print(f"[раунд {e.round}] {source} -> {target}: КРИТ! {e.amount} урона, осталось {e.target_health_after}/{target_max_hp}")
            elif e.type == EventType.DEATH:
                print(f"{target} повержен!")

        rewards = report.rewards
        if battle.outcome == Outcome.DEFEAT:
            print(f"Поражение... {battle.hero.name} едва уносит ноги и теряет {-rewards.gold} золота")
            return

        print(f"Победа! +{rewards.experience} опыта, +{rewards.gold} золота")
        if rewards.loot:
            print(f"Добыча: {self.describe(rewards.loot)}")
        if rewards.levels_gained > 0:
            print("Новый уровень!")