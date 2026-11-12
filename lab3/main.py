from items import DefaultCatalog
from world import Forest, Crypt, DragonLair, LocationRegistry, DragonLair
from camp import Merchant
from hero import Hero, HeroClass
from view import ConsoleView
from combat import Outcome

VIEW = ConsoleView()

def main():
    catalog = DefaultCatalog.create()
    locations = LocationRegistry([
        Forest(catalog), Crypt(catalog), DragonLair(catalog)
    ])
    merchant = Merchant(catalog, [
        DefaultCatalog.IRON_SWORD, DefaultCatalog.ELVEN_BOW, DefaultCatalog.EMBER_STAFF,
        DefaultCatalog.CHAINMAIL, DefaultCatalog.PLATE_ARMOR
    ])

    hero = create_hero(catalog)
    print(f"{hero.get_name()} разбивает лагерь на опушке мистического леса.")

    while True:
        print()
        VIEW.print_hero(hero)
        print("1 - отправиться в экспедицию, 2 - снаряжение, 3 - торговец, 0 - выйти из игры")
        choice = input().strip()
        if choice == "1": go_on_expedition(hero, locations)
        elif choice == "2": manage_equipment(hero)
        elif choice == "3": visit_merchant(hero, merchant)
        elif choice == "0": return
        else: print("Такого варианта нет")

def create_hero(catalog):
    print("Создайте своего героя!")
    while True:
        print("Выберите класс:")
        hero_classes = HeroClass.get_all()
        for i, hc in enumerate(hero_classes):
            kit = hc.get_starter_kit(catalog)
            print(f"{i + 1} - {hc.display_name} (здоровье {hc.base_health}): "
                  f"{VIEW.describe(kit.create_weapon())}, {VIEW.describe(kit.create_armor())}")
        idx = read_choice(len(hero_classes))
        if idx < 0: continue
        
        hc = hero_classes[idx]
        print("Введите имя:")
        name = input().strip()
        try:
            return Hero.Builder().set_name(name).set_hero_class(hc).set_starter_kit(hc.get_starter_kit(catalog)).build()
        except ValueError as e:
            print(f"Не получилось создать героя: {e}")

def go_on_expedition(hero, locations):
    all_locs = locations.get_all()
    print("Куда отправимся?")
    for i, loc in enumerate(all_locs):
        print(f"{i + 1} - {loc.display_name} (рекомендуемый уровень {loc.recommended_level})")
    idx = read_choice(len(all_locs))
    if idx < 0: return

    loc = all_locs[idx]
    report = loc.explore(hero)
    print()
    VIEW.print_report(report, loc.display_name)

    if report.battle.outcome == Outcome.VICTORY and loc.code == DragonLair.CODE:
        print(f"\nДракон повержен! Барды еще долго будут петь о подвиге героя по имени {hero.get_name()}.")

def manage_equipment(hero):
    inv = hero.get_inventory()
    if not inv:
        print("Инвентарь пуст")
        return
    print("Что экипировать? (0 - назад)")
    for i, item in enumerate(inv):
        print(f"{i + 1} - {VIEW.describe(item)}")
    idx = read_choice(len(inv))
    if idx < 0: return
    hero.equip(inv[idx])
    print(f"Экипировано: {VIEW.describe(inv[idx])}")

def visit_merchant(hero, merchant):
    print(f"Торговец: \"Чего желаешь?\" (золото: {hero.gold})")
    print("1 - купить, 2 - продать, 0 - назад")
    choice = input().strip()
    if choice == "1": buy(hero, merchant)
    elif choice == "2": sell(hero, merchant)

def buy(hero, merchant):
    showcase = merchant.get_showcase()
    for i, item in enumerate(showcase):
        print(f"{i + 1} - {VIEW.describe(item)}: {item.get_price()} золота")
    idx = read_choice(len(showcase))
    if idx < 0: return
    try:
        item = merchant.buy(hero, showcase[idx].get_code())
        print(f"Куплено: {VIEW.describe(item)}")
    except RuntimeError as e:
        print(e)

def sell(hero, merchant):
    inv = hero.get_inventory()
    if not inv:
        print("Продавать нечего (экипированные предметы продать нельзя)")
        return
    for i, item in enumerate(inv):
        print(f"{i + 1} - {VIEW.describe(item)}: {merchant.get_sell_price(item)} золота")
    idx = read_choice(len(inv))
    if idx < 0: return
    item = inv[idx]
    price = merchant.sell(hero, item)
    print(f"Продано: {item.get_name()} за {price} золота")

def read_choice(count):
    try:
        choice = int(input().strip())
        if 1 <= choice <= count:
            return choice - 1
    except ValueError:
        pass
    return -1

if __name__ == "__main__":
    main()