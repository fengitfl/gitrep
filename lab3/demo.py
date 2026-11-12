from core import Dice
from items import DefaultCatalog, Enchantment, FIERY
from hero import Hero, HeroClass
from world import Forest, Crypt
from view import ConsoleView

def main():
    catalog = DefaultCatalog.create()
    view = ConsoleView()

    print("===== Одиночка =====")
    first = Dice.get_instance()
    second = Dice.get_instance()
    print(f"Dice.get_instance() возвращает один и тот же объект: {first is second}\n")

    print("===== Прототип =====")
    plain_sword = catalog.create(DefaultCatalog.IRON_SWORD)
    fiery_sword = catalog.create(DefaultCatalog.IRON_SWORD)
    fiery_sword.enchant(FIERY)
    print(f"Первая копия:        {view.describe(plain_sword)}")
    print(f"Вторая копия:        {view.describe(fiery_sword)}")
    print(f"Новая копия шаблона: {view.describe(catalog.create(DefaultCatalog.IRON_SWORD))}")
    print(f"Копии - разные объекты: {plain_sword is not fiery_sword}\n")

    print("===== Абстрактная фабрика =====")
    for hero_class in HeroClass.get_all():
        kit = hero_class.get_starter_kit(catalog)
        print(f"{hero_class.display_name}: {view.describe(kit.create_weapon())}, {view.describe(kit.create_armor())}")
    print()

    print("===== Строитель =====")
    hero = Hero.Builder().set_name("Артур").set_hero_class(HeroClass.by_code("warrior")).set_starter_kit(HeroClass.by_code("warrior").get_starter_kit(catalog)).set_level(3).build()
    view.print_hero(hero)
    try:
        Hero.Builder().set_hero_class(HeroClass.by_code("mage")).set_starter_kit(HeroClass.by_code("mage").get_starter_kit(catalog)).build()
    except ValueError as e:
        print(f"Герой без имени не создается: {e}")
    try:
        Hero.Builder().set_name("Мерлин").build()
    except ValueError as e:
        print(f"Герой без класса не создается: {e}")
    print()

    print("===== Фабричный метод =====")
    forest = Forest(catalog)
    crypt = Crypt(catalog)
    view.print_report(forest.explore(hero, 7), forest.display_name)
    print()
    view.print_report(crypt.explore(hero, 7), crypt.display_name)

if __name__ == "__main__":
    main()