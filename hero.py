from marshmallow_sqlalchemy import ModelSchema
from .character import Character
from .models import Hero
from .dice import Dice


class HeroSchema(ModelSchema):
    class Meta:
        model = Hero


class HeroOld(Character):
    def __init__(self, name, health, ac, initiative_bonus, speed, player):
        super().__init__(name, health, ac, initiative_bonus, 0, speed)
        self.death_saves = {'failed' : 0, 'saved' : 0}
        if player != '':
            self.player = player
        else:
            self.player = 'DM'

    def death(self):
        die = Dice(1, 20)
        roll = 0
        while not roll:
            roll = die.check_roll(int(input("Enter death save roll for {0}: ".format(self.name))))
        if roll == 1:  # roll a nat 1
            self.death_saves['failed'] += 2
            if self.death_saves['failed'] == 3:
                self.death_saves['saves'] = 0
                self.death_saves['failed'] = 0
                self.status = 'dead'
        elif roll < 10:  # rolled 2-9
            self.death_saves['failed'] += 1
            if self.death_saves['failed'] == 3:
                self.death_saves['saves'] = 0
                self.death_saves['failed'] = 0
                self.status = 'dead'
        elif roll < 20:  # rolled 11-19
            self.death_saves['saved'] += 1
            if self.death_saves['saved'] == 3:
                self.death_saves['saves'] = 0
                self.death_saves['failed'] = 0
                self.status = 'stable'
        else:  # rolled a nat 20
            self.health = 1
            self.death_saves['saves'] = 0
            self.death_saves['failed'] = 0
            self.status = 'alive'