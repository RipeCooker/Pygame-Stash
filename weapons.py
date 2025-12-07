"""Procedural weapon sprite generator."""
import pygame
from constants import *

# Simple cache to avoid recreating surfaces every frame
_WEAPON_CACHE = {}

def get_weapon_surface(name, color, scale=2):
    """Return a pygame.Surface for the weapon `name` colored with `color`.
    Surfaces are cached by (name,color,scale).
    """
    key = (name, color, scale)
    if key in _WEAPON_CACHE:
        return _WEAPON_CACHE[key]

    # base dimensions (relative)
    info = WEAPONS.get(name, {})
    w = info.get("width", 40) * scale
    h = info.get("height", 10) * scale

    # allocate with alpha
    surf = pygame.Surface((max(64, int(w) + 20), max(64, int(h) + 40)), pygame.SRCALPHA)
    surf = surf.convert_alpha()

    # center coords for drawing
    sw, sh = surf.get_size()
    cx = sw // 2
    cy = sh // 2

    # draw weapon by type
    if name in ("sword", "dagger", "spear"):
        # long blade
        blade_w = max(6, int(w))
        blade_h = max(12, int(h * 3))
        blade_rect = pygame.Rect(cx, cy - blade_h // 2, blade_w, blade_h)
        pygame.draw.rect(surf, color, blade_rect)
        # tip triangle
        tip = [(cx + blade_w, cy - blade_h // 2), (cx + blade_w + blade_h//3, cy), (cx + blade_w, cy + blade_h // 2)]
        pygame.draw.polygon(surf, color, tip)
        # handle
        handle_rect = pygame.Rect(cx - int(blade_w*0.2), cy + blade_h//2, int(blade_w*0.6), int(blade_h*0.25))
        pygame.draw.rect(surf, (50,50,50), handle_rect)

    elif name in ("axe",):
        # handle
        handle_w = max(6, int(h/2))
        handle_h = max(24, int(h*4))
        handle_rect = pygame.Rect(cx - handle_w//2, cy - handle_h//2, handle_w, handle_h)
        pygame.draw.rect(surf, (80,50,30), handle_rect)
        # blade
        blade_radius = max(20, int(w))
        pygame.draw.polygon(surf, color, [(cx + handle_w//2, cy - blade_radius//2), (cx + handle_w//2 + blade_radius, cy), (cx + handle_w//2, cy + blade_radius//2)])

    elif name in ("mace", "hammer"):
        # handle
        handle_w = max(6, int(h/2))
        handle_h = max(24, int(h*4))
        handle_rect = pygame.Rect(cx - handle_w//2, cy - handle_h//2, handle_w, handle_h)
        pygame.draw.rect(surf, (80,50,30), handle_rect)
        # head
        head_radius = max(12, int(w//1.2))
        pygame.draw.circle(surf, color, (cx + handle_w//2 + head_radius//2, cy), head_radius)

    elif name in ("stick", "staff", "whip"):
        rod_w = max(4, int(h/2))
        rod_h = max(30, int(w*1.5))
        rod_rect = pygame.Rect(cx - rod_h//2, cy - rod_w//2, rod_h, rod_w)
        pygame.draw.rect(surf, color, rod_rect)
        if name == "staff":
            pygame.draw.circle(surf, (220,220,255), (cx + rod_h//2, cy), max(6, int(rod_w*1.5)))
        if name == "whip":
            pygame.draw.circle(surf, (200,180,50), (cx + rod_h//2, cy), 4)

    elif name == "scythe":
        # curved blade approximated by polygon
        blade = [(cx + 10, cy - 20), (cx + 40, cy - 10), (cx + 60, cy), (cx + 40, cy + 10), (cx + 10, cy + 20), (cx + 20, cy)]
        pygame.draw.polygon(surf, color, blade)
        pygame.draw.rect(surf, (80,50,30), (cx - 8, cy - 4, 20, 8))

    else:
        # default: simple rectangle
        pygame.draw.rect(surf, color, (cx - int(w//2), cy - int(h//2), int(w), int(h)))

    _WEAPON_CACHE[key] = surf
    return surf
