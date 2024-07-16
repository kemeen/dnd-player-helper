from pydantic import BaseModel
from random import randint


class Die(BaseModel):
    die_type: int
    num_dice: int
    modifier: int

    def roll(self):
        total = 0
        for _ in range(self.num_dice):
            total += randint(1, self.die_type)
        return total + self.modifier

    def __str__(self):
        return f"{self.num_dice}d{self.die_type}+{self.modifier}"

    def __repr__(self):
        return f"Die(die_type={self.die_type}, num_dice={self.num_dice}, modifier={self.modifier})"
