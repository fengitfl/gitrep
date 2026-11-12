from animal import Animal

class Turtle(Animal):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)

    def get_age_in_human_years(self) -> int:
        age = self.get_age()
        if age <= 0:
            return 0
        return 15 + (age - 1) * 2

    def express(self):
        print(f"{self.get_name()} медленно моргает и прячется в панцирь.")