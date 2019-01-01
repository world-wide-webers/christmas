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


class Joshua:
    SPRITES = load_images([
        'res/img/josh_1.png',
        'res/img/josh_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_SPRITES = load_images([
        'res/img/josh_mug_1.png',
        'res/img/josh_mug_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_ANIM_DELAY = 10
    NAME = 'Joshua'
    QUOTES = [
        'You guys aren\'t well read.'
        'Fact: EM waves are killing your cummies.',
        'This family is diagnosably insane.',
        'I\'m tall.',
    ]
    MOVES = [
        MoveOption('5G', 'Radio waves never hurt so good.'),
        MoveOption('LITERATURE', 'A package of knowledge. But this time, it be deadly.'),
        MoveOption('SEMEN', 'This guy fucks.'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Joshua.SPRITES,
                    Joshua.NAME, Joshua.QUOTES, Joshua.MOVES,
                    Joshua.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(JoshuaFlag())