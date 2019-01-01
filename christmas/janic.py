from enum import Enum

import pygame as pg
from pygame.locals import *

from .color import *
from .component import *
from .dialog import DialogFrame
from .entity import Entity
from .image import load_images
from .input_handler import TOP_PLAYER_INPUT_CONFIG
from .player import Player, MoveOption


class Janicolous:
    SPRITES = load_images([
        'res/img/janic_1.png',
        'res/img/janic_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_SPRITES = load_images([
        'res/img/janic_mug_1.png',
        'res/img/janic_mug_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_ANIM_DELAY = 10
    NAME = 'Janicolous'
    QUOTES = [
        '...and that\'s the way it was.',
        'Elon Musk ain\'t got nothing on me.',
        'Invest in silver. It\'s good for you.',
    ]
    MOVES = [
        MoveOption('BODHISATTVA BOMB', 'White fluff ball with eyes, but hungry for blood.'),
        MoveOption('THE ROAD TO RUIN', 'Silver coins for safe keeping.'),
        MoveOption('IDKWDYWD', '"I don\'t know, what do you wanna do?" A ball of confusion.'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Janicolous.SPRITES,
                    Janicolous.NAME, Janicolous.QUOTES, Janicolous.MOVES,
                    Janicolous.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(JanicolousFlag())