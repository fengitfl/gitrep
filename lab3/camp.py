from core import UnknownCodeException

class Merchant:
    SELL_PRICE_PERCENT = 50

    def __init__(self, catalog, assortment):
        self.catalog = catalog
        self.assortment = list(assortment)

    def get_showcase(self):
        return [self.catalog.create(code) for code in self.assortment]

    def buy(self, hero, code):
        if code not in self.assortment:
            raise UnknownCodeException("Товар", code)
        item = self.catalog.create(code)
        hero.spend_gold(item.get_price())
        hero.add_item(item)
        return item

    def sell(self, hero, item):
        price = self.get_sell_price(item)
        hero.remove_item(item)
        hero.add_gold(price)
        return price

    def get_sell_price(self, item):
        return item.get_price() * self.SELL_PRICE_PERCENT // 100
    