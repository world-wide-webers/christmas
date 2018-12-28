import itertools

from pygame.locals import *

from .component import *
from .input_handler import InputIntent


class System:
    def __init__(self, game):
        self.game = game

    def run(self):
        filtered_entities = [entity for entity in self.game.entities
                             if entity is not None and
                             all(map(lambda c: entity.has_comp(c), self.COMPS))]
        self._run(filtered_entities)

    def _run(self, *_):
        raise NotImplementedError


class PlayerUpdateSystem(System):
    COMPS = [VelocityComp, InputConfigComp]
    MOVE_SPEED = 5.0

    def _run(self, entities):
        inp_handler = self.game.get_input_handler()
        for entity in entities:
            vel, inp_conf = entity.get_comps(VelocityComp, InputConfigComp)
            if inp_handler.is_key_down(inp_conf.key_map[InputIntent.UP]):
                vel.y -= PlayerUpdateSystem.MOVE_SPEED
            if inp_handler.is_key_down(inp_conf.key_map[InputIntent.DOWN]):
                vel.y += PlayerUpdateSystem.MOVE_SPEED
            if inp_handler.is_key_down(inp_conf.key_map[InputIntent.LEFT]):
                vel.x -= PlayerUpdateSystem.MOVE_SPEED
            if inp_handler.is_key_down(inp_conf.key_map[InputIntent.RIGHT]):
                vel.x += PlayerUpdateSystem.MOVE_SPEED


class AmmoUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp, AmmoComp, InputConfigComp]

    def _run(self, entities):
        inp_handler = self.game.get_input_handler()
        for entity in entities:
            pos, vel, ammo, inp_conf = entity.get_comps(PositionComp, VelocityComp, AmmoComp, InputConfigComp)
            if len(ammo.rounds) == 0:
                # They're empty.  Remove their ammo belt.
                entity.remove_comp(AmmoComp)
            elif inp_handler.is_key_down(inp_conf.key_map[InputIntent.FIRE]):
                projectile_cons = ammo.rounds.popleft()
                projectile = self.game.create_entity()
                projectile_cons.init(projectile, entity, pos.x, pos.y, vel.x, vel.y)


class PositionBoundSystem(System):
    COMPS = [PositionComp, VelocityComp, SizeComp, PositionBoundComp]

    def _run(self, entities):
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


class CollideSystem(System):
    COMPS = [PositionComp, VelocityComp, SizeComp, CollideFlag]

    def _run(self, entities):
        for (e1, e2) in itertools.combinations(entities, 2):
            pos1, vel1, size1 = e1.get_comps(PositionComp, VelocityComp, SizeComp)
            pos2, vel2, size2 = e2.get_comps(PositionComp, VelocityComp, SizeComp)
            intended_pos1 = PositionComp(pos1.x + vel1.x, pos1.y + vel1.y)
            intended_pos2 = PositionComp(pos2.x + vel2.x, pos2.y + vel2.y)
            if (intended_pos1.x < intended_pos2.x + size2.w and
                intended_pos1.x + size1.w > intended_pos2.x and
                intended_pos1.y < intended_pos2.y + size2.h and
                intended_pos1.y + size1.h > intended_pos2.y):
                if e1.has_comp(ProjectileFlag) and e2.has_comp(PlayerComp):
                    proj = e1
                    player = e2
                elif e2.has_comp(ProjectileFlag) and e1.has_comp(PlayerComp):
                    proj = e2
                    player = e1
                else:
                    # We're only interested in projectile <-> player collisions.
                    continue

                if proj.has_comp(OwnerComp) and proj.get_comp(OwnerComp).owner == player:
                    continue
                proj.kill()
                player.get_comp(PlayerComp).curr_health -= 1


class PositionUpdateSystem(System):
    COMPS = [PositionComp, VelocityComp]

    def _run(self, entities):
        for entity in entities:
            pos, vel = entity.get_comps(PositionComp, VelocityComp)
            pos.x += vel.x
            pos.y += vel.y


class VelocityAttenuateSystem(System):
    COMPS = [VelocityComp, VelocityAttenuateFlag]

    def _run(self, entities):
        VELOCITY_ATTENUATION = 0.5

        for entity in entities:
            vel = entity.get_comp(VelocityComp)
            vel.x *= VELOCITY_ATTENUATION
            vel.y *= VELOCITY_ATTENUATION


class LifetimeUpdateSystem(System):
    COMPS = [LifetimeComp]

    def _run(self, entities):
        for entity in entities:
            lifetime = entity.get_comp(LifetimeComp)
            lifetime.life -= 1
            if lifetime.life <= 0:
                entity.kill()


class DeadCleanupSystem(System):
    COMPS = [DeadFlag]

    def _run(self, entities):
        for entity in entities:
            self.game.destroy_entity(entity)


class PlayerAnimateUpdateSystem(System):
    COMPS = [VelocityComp, DrawComp, AnimateComp]
    # Number of ticks to wait between animation frames
    IDLE_ANIM_DELAY = 5
    MOVING_ANIM_DELAY = 2
    IDLE_VELOCITY_THRESHOLD = 0.1

    def _run(self, entities):
        for entity in entities:
            vel, draw, anim = entity.get_comps(VelocityComp, DrawComp, AnimateComp)
            if (abs(vel.x) < PlayerAnimateUpdateSystem.IDLE_VELOCITY_THRESHOLD
                and abs(vel.y) < PlayerAnimateUpdateSystem.IDLE_VELOCITY_THRESHOLD):
                anim.delay = PlayerAnimateUpdateSystem.IDLE_ANIM_DELAY
            else:
                anim.delay = PlayerAnimateUpdateSystem.MOVING_ANIM_DELAY


class AnimateUpdateSystem(System):
    COMPS = [DrawComp, AnimateComp]

    def _run(self, entities):
        for entity in entities:
            draw, anim = entity.get_comps(DrawComp, AnimateComp)
            if anim.clock >= anim.delay:
                draw.img_idx = (draw.img_idx + 1) % len(draw.images)
                draw.image = draw.images[draw.img_idx]
                anim.clock = 0
            anim.clock += 1


class DrawUpdateSystem(System):
    COMPS = [PositionComp, DrawComp]

    def _run(self, entities):
        for entity in entities:
            pos, draw = entity.get_comps(PositionComp, DrawComp)
            draw.rect.topleft = (pos.x, pos.y)
