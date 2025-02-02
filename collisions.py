from pygame.rect import Rect
from pygame.math import Vector2


def handle_collisons_one_to_many_x(
    target: Rect,
    vel: Vector2,
    has_rects,
) -> Rect:
    for item in has_rects:
        if target.colliderect(item.get_hitbox()):
            if vel.x > 0:
                target.right = item.get_hitbox().left
            else:
                target.left = item.get_hitbox().right
    return target


def handle_collisons_one_to_many_y(
    target: Rect,
    vel: Vector2,
    has_rects,
) -> Rect:
    for item in has_rects:
        if target.colliderect(item.get_hitbox()):
            if vel.y > 0:
                target.bottom = item.get_hitbox().top
            else:
                target.top = item.get_hitbox().bottom
    return target