from pygame.locals import *

from .component import *


class System:
    def run(self, entities, pressed_keys):
        filtered_entities = [entity for entity in entities
                             if all(map(lambda c: entity.has_comp(c), self.COMPS))]
        self._run(filtered_entities, pressed_keys)

    def _run(self, *_):
        raise NotImplementedError


class PlayerUpdateSystem(System):
    COMPS = [VelocityComp, TurnFlagComp]

    def _run(self, entities, pressed_keys):
        MOVE_SPEED = 5.0

        assert(len(entities) == 1)
        for entity in entities:
            vel = entity.get_comp(VelocityComp)
            if pressed_keys[K_UP]:
                vel.y -= MOVE_SPEED
            if pressed_keys[K_DOWN]:
                vel.y += MOVE_SPEED
            if pressed_keys[K_LEFT]:
                vel.x -= MOVE_SPEED
            if pressed_keys[K_RIGHT]:
                vel.x += MOVE_SPEED


class PositionBoundSystem(System):
    COMPS = [PositionComp, VelocityComp, SizeComp, PositionBoundComp]

    def _run(self, entities, _):
        for entity in entities:
            pos, vel, size, bound = entity.get_comps(PositionComp, VelocityComp, SizeComp, PositionBoundComp)
            intended_pos = PositionComp(pos.x + vel.x, pos.y + vel.y)
            if intended_pos.x < bound.x:
                pos.x = bound.x
                vel.x *= -10
            elif intended_pos.x + size.w > bound.x + bound.w:
                pos.x = bound.x + bound.w - size.w
                vel.x *= -10
            if intended_pos.y < bound.y:
                pos.y = bound.y
                vel.y *= -10
            elif intended_pos.y + size.h > bound.y + bound.h:
                pos.y = bound.y + bound.h - size.h
                vel.y *= -10


class PositionUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp]

    def _run(self, entities, _):
        for entity in entities:
            pos, vel = entity.get_comps(PositionComp, VelocityComp)
            pos.x += vel.x
            pos.y += vel.y


class VelocityAttenuateSystem(System):
    COMPS = [VelocityComp]

    def _run(self, entities, _):
        VELOCITY_ATTENUATION = 0.5

        for entity in entities:
            vel = entity.get_comp(VelocityComp)
            vel.x *= VELOCITY_ATTENUATION
            vel.y *= VELOCITY_ATTENUATION


class AnimateUpdateSystem(System):
    COMPS = [VelocityComp, DrawComp, AnimateComp]

    def _run(self, entities, _):
        # Number of ticks to wait between animation frames
        IDLE_ANIM_DELAY = 5
        MOVING_ANIM_DELAY = 2
        IDLE_VELOCITY_THRESHOLD = 0.1

        for entity in entities:
            vel, draw, anim = entity.get_comps(VelocityComp, DrawComp, AnimateComp)

            if abs(vel.x) < IDLE_VELOCITY_THRESHOLD and abs(vel.y) < IDLE_VELOCITY_THRESHOLD:
                anim_delay = IDLE_ANIM_DELAY
            else:
                anim_delay = MOVING_ANIM_DELAY

            if anim.clock >= anim_delay:
                draw.img_idx = (draw.img_idx + 1) % len(draw.images)
                draw.image = draw.images[draw.img_idx]
                anim.clock = 0
            anim.clock += 1


class DrawUpdateSystem(System):
    COMPS = [PositionComp, DrawComp]

    def _run(self, entities, _):
        for entity in entities:
            pos, draw = entity.get_comps(PositionComp, DrawComp)
            draw.rect.topleft = (pos.x, pos.y)
