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


class Logan:
    SPRITES = load_images([
        'res/img/logan_1.png',
        'res/img/logan_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_SPRITES = load_images([
        'res/img/logan_mug_1.png',
        'res/img/logan_mug_2.png'
    ], scale_factor=Player.SPRITE_SCALE_FACTOR)
    MUG_ANIM_DELAY = 10
    NAME = 'Logan'
    QUOTES = [
        'Eat carpel toobley!',
        'I\'m very ready to zonk right about now. Zzzzz.',
        'Now, what\'s going on there?',
        'See my erection? Just. Don\'t. Think. About. It.',
        'Yeah, sure. I\'ll just write a mediocre program on my $5,000 laptop. COME ON!.',
    ]
    MOVES = [
        MoveOption('BREAKDANCE TORNADO', 'Little tornado of sick dance moves for Santa.'),
        MoveOption('SILENT NIGHT', 'Throws a void of silent treatment.'),
        MoveOption('FULL SEND', 'A 50 lbs dumbbell.'),
    ]

    @staticmethod
    def init(entity, x, y, pos_bounds):
        Player.init(entity, x, y, pos_bounds, Logan.SPRITES,
                    Logan.NAME, Logan.QUOTES, Logan.MOVES,
                    Logan.MUG_SPRITES)
        entity.add_comp(TopPlayerFlag())
        entity.add_comp(InputConfigComp(TOP_PLAYER_INPUT_CONFIG))
        entity.add_comp(LoganFlag())