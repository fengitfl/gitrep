from items import DefaultCatalog

class StarterKitFactory:
    def create_weapon(self): pass
    def create_armor(self): pass

class WarriorKitFactory(StarterKitFactory):
    def __init__(self, catalog): self.catalog = catalog
    def create_weapon(self): return self.catalog.create_weapon(DefaultCatalog.TRAINING_SWORD)
    def create_armor(self): return self.catalog.create_armor(DefaultCatalog.CHAINMAIL)

class RangerKitFactory(StarterKitFactory):
    def __init__(self, catalog): self.catalog = catalog
    def create_weapon(self): return self.catalog.create_weapon(DefaultCatalog.HUNTING_BOW)
    def create_armor(self): return self.catalog.create_armor(DefaultCatalog.LEATHER_ARMOR)

class MageKitFactory(StarterKitFactory):
    def __init__(self, catalog): self.catalog = catalog
    def create_weapon(self): return self.catalog.create_weapon(DefaultCatalog.APPRENTICE_STAFF)
    def create_armor(self): return self.catalog.create_armor(DefaultCatalog.LINEN_ROBE)