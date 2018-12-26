import pygame as pg

from .component import *
from .entity import Entity
from .image import load_images
from .player import Player


class Santa:
    SPRITES = load_images([
        'res/img/santa_back_1.png',
        'res/img/santa_back_2.png',
        # 'res/santa_front_down.png',
        # 'res/santa_front_up.png',
    ], scale_factor=4)
    QUOTES = [
        'Get ready for some hot suck of dick!',
        'Hey, you came here to fight!',
        'What are you wearing? \'Cause it looks like something you\'re ready to fight in.',
        'How far have you gotten with a man who\'s in his mid-40s?',
        'On an unrelated note, I\'m 44.',
        'Woah. I sure can take a punch.',
        'That all?  I wish... it was.',
        'Yeah sure, spill blood all over my HAND-CRAFTED SUIT?! COME ON!',
        # TODO: The one's below are actually Luke's.
        'Can we smoke a little weed?  My words get better.',
        'When considering intelligence, you can be a retarded professional and still be retarded.'
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Santa.SPRITES)
        entity.add_comp(SantaFlagComp())


class SantaMug:
    ANIM_DELAY = 10
    SPRITES = load_images([
        'res/img/santa_mug_1.png',
        'res/img/santa_mug_2.png'
    ], scale_factor=4)
    QUOTES = {
        'attack': 'Coal in yo a-hole',
    }

    @staticmethod
    def init(entity, x, y):
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(DrawComp(SantaMug.SPRITES))
        entity.add_comp(AnimateComp(SantaMug.ANIM_DELAY))


class CoalProjectile:
    SPRITES = load_images([
        'res/img/coal.png',
    ], scale_factor=4)
    PROJECTILE_LIFE = 40

    @staticmethod
    def init(entity, x, y, xv, yv):
        entity.add_comp(PositionComp(x, y))
        entity.add_comp(VelocityComp(xv, yv))
        entity.add_comp(LifetimeComp(CoalProjectile.PROJECTILE_LIFE))
        entity.add_comp(DrawComp(CoalProjectile.SPRITES))
