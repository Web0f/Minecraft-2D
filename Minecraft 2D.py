import pygame, math, random, sys, time

pygame.init()
pygame.font.init()

# ============ ПОЛНЫЙ ЭКРАН ============
info = pygame.display.Info()
SCREEN_W, SCREEN_H = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)
pygame.display.set_caption("Minecraft 2D — Web0f & germagen1737")
clock = pygame.time.Clock()

FPS = 60
TILE_SIZE = 32
CHUNK_W = 16
WORLD_HEIGHT = 96
SEA_LEVEL = 62

REACH = 6 * TILE_SIZE
GRAVITY = 0.7
JUMP_VEL = -13
PLAYER_SPEED = 4.5
DAY_LENGTH = 240

MAX_HEALTH = 20
MAX_HUNGER = 20
INVULN_FRAMES = 30
MOB_SPAWN_CAP = 18
SPAWN_INTERVAL = 90
SPAWN_RADIUS_MIN = 8 * TILE_SIZE
SPAWN_RADIUS_MAX = 20 * TILE_SIZE

HUNGER_DRAIN_STAND = 60 * 45
HUNGER_DRAIN_MOVE  = 60 * 18
REGEN_INTERVAL     = 60 * 4
STARVE_INTERVAL    = 60 * 4

GOAL_DIAMONDS = 5
GOAL_COINS = 50

AUTHORS = "Web0f  &  germagen1737"
SECRET_WIN_CODE = "Web0fAndGermagen1737WIN"
CONSOLE_TOGGLE_KEY = pygame.K_BACKQUOTE

# Шрифты
try:
    font_small = pygame.font.SysFont("Consolas", 13, bold=True)
    font = pygame.font.SysFont("Arial", 16, bold=True)
    font_med = pygame.font.SysFont("Arial", 22, bold=True)
    font_big = pygame.font.SysFont("Arial", 40, bold=True)
    font_huge = pygame.font.SysFont("Arial", 60, bold=True)
    font_mega = pygame.font.SysFont("Arial", 80, bold=True)
except:
    font_small = font = font_med = font_big = font_huge = font_mega = pygame.font.Font(None, 24)

# ============ БЛОКИ ============
(AIR, GRASS, DIRT, STONE, WOOD, LEAVES, SAND, SANDSTONE, WATER, SNOW,
 ICE, COAL_ORE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, BEDROCK,
 CACTUS, PLANKS, GLASS, BRICK, GRAVEL, CHEST, STALL) = range(23)

RAW_PORK, RAW_BEEF, RAW_MUTTON, APPLE, BREAD = 100, 101, 102, 103, 104
WOOD_SWORD, STONE_SWORD, IRON_SWORD, DIAMOND_SWORD = 200, 201, 202, 203
WOOD_PICK, STONE_PICK, IRON_PICK, DIAMOND_PICK = 210, 211, 212, 213
COIN, DIAMOND = 300, 301

BLOCK_INFO = {
    AIR:         {"name": "Воздух",   "solid": False, "breakable": False},
    GRASS:       {"name": "Трава",    "solid": True,  "breakable": True},
    DIRT:        {"name": "Земля",    "solid": True,  "breakable": True},
    STONE:       {"name": "Камень",   "solid": True,  "breakable": True},
    WOOD:        {"name": "Дерево",   "solid": True,  "breakable": True},
    LEAVES:      {"name": "Листва",   "solid": True,  "breakable": True},
    SAND:        {"name": "Песок",    "solid": True,  "breakable": True, "falls": True},
    SANDSTONE:   {"name": "Песчаник", "solid": True,  "breakable": True},
    WATER:       {"name": "Вода",     "solid": False, "breakable": False},
    SNOW:        {"name": "Снег",     "solid": True,  "breakable": True},
    ICE:         {"name": "Лёд",      "solid": True,  "breakable": True},
    COAL_ORE:    {"name": "Уголь",    "solid": True,  "breakable": True},
    IRON_ORE:    {"name": "Железо",   "solid": True,  "breakable": True},
    GOLD_ORE:    {"name": "Золото",   "solid": True,  "breakable": True},
    DIAMOND_ORE: {"name": "Алмазная руда", "solid": True, "breakable": True},
    BEDROCK:     {"name": "Бедрок",   "solid": True,  "breakable": False},
    CACTUS:      {"name": "Кактус",   "solid": True,  "breakable": True, "damage": 2},
    PLANKS:      {"name": "Доски",    "solid": True,  "breakable": True},
    GLASS:       {"name": "Стекло",   "solid": True,  "breakable": True},
    BRICK:       {"name": "Кирпич",   "solid": True,  "breakable": True},
    GRAVEL:      {"name": "Гравий",   "solid": True,  "breakable": True, "falls": True},
    CHEST:       {"name": "Сундук",   "solid": True,  "breakable": True, "special": "chest"},
    STALL:       {"name": "Ларёк",    "solid": True,  "breakable": True, "special": "stall"},
}

FOOD_INFO = {
    RAW_PORK:   {"name": "Сырая свинина",  "heal": 2, "feed": 4},
    RAW_BEEF:   {"name": "Сырая говядина", "heal": 3, "feed": 5},
    RAW_MUTTON: {"name": "Сырая баранина", "heal": 2, "feed": 4},
    APPLE:      {"name": "Яблоко",         "heal": 2, "feed": 5},
    BREAD:      {"name": "Хлеб",           "heal": 4, "feed": 8},
}

WEAPON_INFO = {
    WOOD_SWORD:    {"name": "Деревянный меч",  "damage": 3, "color": (150, 105, 55)},
    STONE_SWORD:   {"name": "Каменный меч",    "damage": 4, "color": (150, 150, 150)},
    IRON_SWORD:    {"name": "Железный меч",    "damage": 6, "color": (220, 220, 235)},
    DIAMOND_SWORD: {"name": "Алмазный меч",    "damage": 9, "color": (100, 230, 230)},
}

PICK_INFO = {
    WOOD_PICK:    {"name": "Деревянная кирка", "speed": 4, "color": (150, 105, 55)},
    STONE_PICK:   {"name": "Каменная кирка",   "speed": 3, "color": (150, 150, 150)},
    IRON_PICK:    {"name": "Железная кирка",   "speed": 2, "color": (220, 220, 235)},
    DIAMOND_PICK: {"name": "Алмазная кирка",   "speed": 1, "color": (100, 230, 230)},
}

ITEM_INFO = {}
for bid, info_ in BLOCK_INFO.items():
    ITEM_INFO[bid] = {**info_, "type": "block", "stackable": False}
for fid, info_ in FOOD_INFO.items():
    ITEM_INFO[fid] = {**info_, "type": "food", "stackable": True}
for wid, info_ in WEAPON_INFO.items():
    ITEM_INFO[wid] = {**info_, "type": "weapon", "stackable": False}
for pid, info_ in PICK_INFO.items():
    ITEM_INFO[pid] = {**info_, "type": "pick", "stackable": False}
ITEM_INFO[COIN] = {"name": "Монета", "type": "money", "stackable": True, "color": (240, 200, 60)}
ITEM_INFO[DIAMOND] = {"name": "Алмаз", "type": "resource", "stackable": True, "color": (100, 230, 230)}

FALLING_BLOCKS = {bid for bid, info_ in BLOCK_INFO.items() if info_.get("falls")}

# ============ ТЕКСТУРЫ ============
def make_block_texture(bid, size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    rng = random.Random(bid * 7919 + 13)
    if bid == GRASS:
        surf.fill((140, 95, 55))
        pygame.draw.rect(surf, (100, 180, 65), (0, 0, size, size // 3))
        for _ in range(8):
            pygame.draw.rect(surf, (110, 70, 40), (rng.randint(2, size-4), rng.randint(size//3+2, size-4), 3, 3))
    elif bid == DIRT:
        surf.fill((140, 95, 55))
        for _ in range(15):
            pygame.draw.rect(surf, (110, 70, 40), (rng.randint(2, size-4), rng.randint(2, size-4), 3, 3))
    elif bid == STONE:
        surf.fill((130, 130, 130))
        for _ in range(10):
            pygame.draw.rect(surf, (105, 105, 105), (rng.randint(2, size-6), rng.randint(2, size-6), 5, 5))
    elif bid == GRAVEL:
        surf.fill((120, 115, 110))
        for _ in range(30):
            pygame.draw.rect(surf, rng.choice([(90,85,80),(150,145,140),(70,65,60)]),
                             (rng.randint(0, size-4), rng.randint(0, size-4), 4, 4))
    elif bid == WOOD:
        surf.fill((110, 75, 40))
        pygame.draw.rect(surf, (90, 55, 25), (size // 3, 0, 2, size))
        pygame.draw.rect(surf, (90, 55, 25), (2 * size // 3, 0, 2, size))
    elif bid == LEAVES:
        surf.fill((55, 145, 45))
        for _ in range(20):
            pygame.draw.rect(surf, rng.choice([(45,125,35),(75,165,55),(35,105,30)]),
                             (rng.randint(1, size-4), rng.randint(1, size-4), 3, 3))
    elif bid == SAND:
        surf.fill((225, 205, 130))
        for _ in range(20):
            pygame.draw.rect(surf, (205, 185, 110), (rng.randint(1, size-2), rng.randint(1, size-2), 2, 2))
    elif bid == SANDSTONE:
        surf.fill((200, 180, 100))
        for y in range(0, size, 8):
            pygame.draw.line(surf, (170, 150, 80), (0, y), (size, y), 1)
    elif bid == WATER:
        surf.fill((55, 110, 220, 160))
    elif bid == SNOW: surf.fill((235, 240, 250))
    elif bid == ICE:  surf.fill((150, 210, 245, 200))
    elif bid in (COAL_ORE, IRON_ORE, GOLD_ORE, DIAMOND_ORE):
        surf.fill((130, 130, 130))
        for _ in range(8):
            pygame.draw.rect(surf, (105, 105, 105), (rng.randint(2, size-6), rng.randint(2, size-6), 4, 4))
        ore_color = {COAL_ORE:(30,30,30), IRON_ORE:(200,160,130),
                     GOLD_ORE:(240,200,60), DIAMOND_ORE:(100,230,230)}[bid]
        for _ in range(5):
            pygame.draw.rect(surf, ore_color, (rng.randint(3, size-8), rng.randint(3, size-8), 5, 5))
    elif bid == BEDROCK:
        surf.fill((40, 40, 40))
        for _ in range(20):
            pygame.draw.rect(surf, rng.choice([(20,20,20),(60,60,60)]),
                             (rng.randint(1, size-3), rng.randint(1, size-3), 3, 3))
    elif bid == CACTUS:
        surf.fill((60, 150, 60))
        for x in range(4, size, 8):
            pygame.draw.line(surf, (40, 110, 40), (x, 0), (x, size), 1)
    elif bid == PLANKS:
        surf.fill((185, 140, 80))
        for y in range(0, size, 8):
            pygame.draw.line(surf, (145, 105, 55), (0, y), (size, y), 1)
    elif bid == GLASS:
        surf.fill((200, 230, 245, 60))
        pygame.draw.rect(surf, (200, 225, 240), (0, 0, size, size), 2)
    elif bid == BRICK:
        surf.fill((180, 80, 60))
        for y in range(0, size, 8):
            pygame.draw.line(surf, (110, 45, 35), (0, y), (size, y), 2)
            off = 0 if (y // 8) % 2 == 0 else 8
            for x in range(off, size, 16):
                pygame.draw.line(surf, (110, 45, 35), (x, y), (x, y + 8), 2)
    elif bid == CHEST:
        surf.fill((140, 90, 40))
        pygame.draw.rect(surf, (100, 60, 25), (0, 0, size, size), 3)
        pygame.draw.line(surf, (90, 55, 20), (0, size//2), (size, size//2), 3)
        pygame.draw.rect(surf, (240, 200, 60), (size//2-4, size//2-3, 8, 8))
        pygame.draw.circle(surf, (60, 40, 20), (size//2, size//2+1), 2)
    elif bid == STALL:
        surf.fill((240, 210, 130))
        for x in range(0, size, 8):
            color = (220, 60, 60) if (x // 8) % 2 == 0 else (245, 245, 245)
            pygame.draw.rect(surf, color, (x, 0, 8, size//3))
        pygame.draw.rect(surf, (140, 90, 40), (0, size//3, size, size*2//3))
        pygame.draw.rect(surf, (100, 60, 25), (0, size//3, size, size*2//3), 2)
        for y in range(size//3+4, size, 6):
            pygame.draw.line(surf, (110, 70, 30), (0, y), (size, y), 1)
    return surf

def make_food_texture(fid, size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    if fid == RAW_PORK:
        pygame.draw.ellipse(surf, (240, 155, 155), (8, 10, size-16, size-20))
        pygame.draw.ellipse(surf, (200, 110, 110), (8, 10, size-16, size-20), 2)
    elif fid == RAW_BEEF:
        pygame.draw.ellipse(surf, (180, 60, 60), (6, 8, size-12, size-16))
        pygame.draw.line(surf, (240, 220, 220), (12, 15), (size-12, 15), 2)
        pygame.draw.line(surf, (240, 220, 220), (10, 22), (size-10, 22), 2)
    elif fid == RAW_MUTTON:
        pygame.draw.ellipse(surf, (200, 80, 80), (4, 10, size-8, size-18))
        pygame.draw.rect(surf, (240, 240, 230), (size//2-2, 4, 4, 10))
    elif fid == APPLE:
        pygame.draw.circle(surf, (220, 40, 40), (size//2, size//2+2), size//2-6)
        pygame.draw.circle(surf, (255, 100, 100), (size//2-3, size//2-2), 3)
        pygame.draw.rect(surf, (100, 60, 30), (size//2-1, 5, 3, 6))
        pygame.draw.ellipse(surf, (80, 160, 60), (size//2+1, 3, 8, 5))
    elif fid == BREAD:
        pygame.draw.ellipse(surf, (200, 140, 60), (3, 8, size-6, size-16))
        pygame.draw.ellipse(surf, (150, 100, 40), (3, 8, size-6, size-16), 2)
        for i in range(4):
            x = 6 + i * (size-14) // 4
            pygame.draw.line(surf, (150, 100, 40), (x, 10), (x+2, size-10), 2)
    return surf

def make_sword_texture(color, size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, (100, 60, 30), (size//2-2, size*3//5, 4, size*2//5-2))
    pygame.draw.circle(surf, (80, 50, 20), (size//2, size-3), 3)
    pygame.draw.rect(surf, (60, 40, 20), (size//2-7, size*3//5-3, 14, 4))
    pts = [(size//2-3, size*3//5-3), (size//2+3, size*3//5-3),
           (size//2+2, size//5), (size//2, size//10),
           (size//2-2, size//5)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(surf, (255, 255, 255, 120), (size//2-1, size//4), (size//2-1, size*3//5-6), 1)
    return surf

def make_pick_texture(color, size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, (100, 60, 30), (size//2-2, size//3, 4, size*2//3-4))
    pygame.draw.rect(surf, color, (size//6, size//4, size*2//3, 5))
    pygame.draw.polygon(surf, color, [(size//6, size//4), (size//6-2, size//3), (size//6+6, size//3)])
    pygame.draw.polygon(surf, color, [(size*5//6, size//4), (size*5//6+2, size//3), (size*5//6-6, size//3)])
    pygame.draw.line(surf, (255, 255, 255, 130), (size//6+3, size//4+1), (size*5//6-3, size//4+1), 1)
    return surf

def make_coin_texture(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, (240, 200, 60), (size//2, size//2), size//2-3)
    pygame.draw.circle(surf, (180, 140, 20), (size//2, size//2), size//2-3, 2)
    pygame.draw.circle(surf, (255, 230, 120), (size//2-2, size//2-2), size//4)
    return surf

def make_diamond_texture(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    pts = [(cx, 4), (size-4, cy//2+2), (cx, size-4), (4, cy//2+2)]
    pygame.draw.polygon(surf, (100, 230, 230), pts)
    pygame.draw.polygon(surf, (60, 180, 180), pts, 2)
    pygame.draw.line(surf, (255, 255, 255), (cx-4, 8), (cx-1, 10), 2)
    return surf

BLOCK_TEX = {bid: make_block_texture(bid, TILE_SIZE).convert_alpha()
             for bid in BLOCK_INFO if bid != AIR}
FOOD_TEX = {fid: make_food_texture(fid, TILE_SIZE).convert_alpha() for fid in FOOD_INFO}
WEAPON_TEX = {wid: make_sword_texture(info_["color"], TILE_SIZE).convert_alpha()
              for wid, info_ in WEAPON_INFO.items()}
PICK_TEX = {pid: make_pick_texture(info_["color"], TILE_SIZE).convert_alpha()
            for pid, info_ in PICK_INFO.items()}
COIN_TEX = make_coin_texture(TILE_SIZE).convert_alpha()
DIAMOND_TEX = make_diamond_texture(TILE_SIZE).convert_alpha()

def get_tex(item_id):
    if item_id in BLOCK_TEX: return BLOCK_TEX[item_id]
    if item_id in FOOD_TEX:  return FOOD_TEX[item_id]
    if item_id in WEAPON_TEX: return WEAPON_TEX[item_id]
    if item_id in PICK_TEX:  return PICK_TEX[item_id]
    if item_id == COIN: return COIN_TEX
    if item_id == DIAMOND: return DIAMOND_TEX
    return None

# ============ ШУМ ============
def hash2(x, y, seed=0):
    n = (int(x)*374761393 + int(y)*668265263 + int(seed)*1013904223 + 0x5bd1e995) & 0x7fffffff
    n = (n ^ (n >> 13)) * 1274126177 & 0x7fffffff
    return ((n ^ (n >> 16)) & 0x7fffffff) / 0x7fffffff

def value_noise(x, y, seed=0):
    x0, y0 = math.floor(x), math.floor(y)
    fx, fy = x - x0, y - y0
    sx = fx*fx*(3-2*fx); sy = fy*fy*(3-2*fy)
    n00 = hash2(x0, y0, seed); n10 = hash2(x0+1, y0, seed)
    n01 = hash2(x0, y0+1, seed); n11 = hash2(x0+1, y0+1, seed)
    a = n00 + sx*(n10-n00); b = n01 + sx*(n11-n01)
    return a + sy*(b-a)

def fbm(x, y, octaves=4, seed=0):
    total, amp, freq, mx = 0, 1, 1, 0
    for _ in range(octaves):
        total += value_noise(x*freq, y*freq, seed) * amp
        mx += amp; amp *= 0.5; freq *= 2
    return total / mx

# ============ МИР ============
class Chunk:
    __slots__ = ['cx', 'blocks']
    def __init__(self, cx):
        self.cx = cx
        self.blocks = [[AIR] * CHUNK_W for _ in range(WORLD_HEIGHT)]

class World:
    def __init__(self, seed=42):
        self.seed = seed
        self.chunks = {}
        self.tick_timer = 0
        self.chest_loot = {}
        self.stall_data = {}

    def get_chunk(self, cx):
        ch = self.chunks.get(cx)
        if ch is None:
            ch = self.generate_chunk(cx)
            self.chunks[cx] = ch
        return ch

    def get_block(self, wx, wy):
        if wy < 0 or wy >= WORLD_HEIGHT: return AIR
        return self.get_chunk(wx // CHUNK_W).blocks[wy][wx % CHUNK_W]

    def set_block(self, wx, wy, bid):
        if wy < 0 or wy >= WORLD_HEIGHT: return
        self.get_chunk(wx // CHUNK_W).blocks[wy][wx % CHUNK_W] = bid

    def get_column_info(self, wx):
        elevation = fbm(wx * 0.008, 0, 4, seed=self.seed + 100)
        temp = fbm(wx * 0.004, 500, 2, seed=self.seed + 200)
        moist = fbm(wx * 0.005, 1000, 2, seed=self.seed + 300)
        if elevation > 0.72: biome = 'Горы'
        elif temp > 0.62 and moist < 0.42: biome = 'Пустыня'
        elif temp < 0.35: biome = 'Снега'
        elif moist > 0.58: biome = 'Лес'
        else: biome = 'Равнины'
        if biome == 'Горы': h = int(SEA_LEVEL - 15 - elevation * 32)
        elif biome == 'Пустыня': h = int(SEA_LEVEL - 3 - elevation * 4)
        elif biome == 'Снега': h = int(SEA_LEVEL - 5 - elevation * 8)
        elif biome == 'Лес': h = int(SEA_LEVEL - 5 - elevation * 11)
        else: h = int(SEA_LEVEL - 5 - elevation * 8)
        return max(8, min(h, WORLD_HEIGHT - 20)), biome

    def is_village_chunk(self, cx):
        return hash2(cx, 777, self.seed) < 0.12

    def generate_chunk(self, cx):
        chunk = Chunk(cx)
        is_village = self.is_village_chunk(cx)

        for lx in range(CHUNK_W):
            wx = cx * CHUNK_W + lx
            surface_y, biome = self.get_column_info(wx)
            for y in range(WORLD_HEIGHT):
                if y < surface_y: block = AIR
                elif y == surface_y:
                    if surface_y >= SEA_LEVEL - 1 or biome == 'Пустыня': block = SAND
                    elif biome == 'Снега' or surface_y < SEA_LEVEL - 25: block = SNOW
                    else: block = GRASS
                elif y < surface_y + 3:
                    if biome == 'Пустыня' or surface_y >= SEA_LEVEL - 1: block = SAND
                    else: block = DIRT
                else: block = STONE
                if block == AIR and y >= SEA_LEVEL: block = WATER
                chunk.blocks[y][lx] = block
            chunk.blocks[WORLD_HEIGHT - 1][lx] = BEDROCK
            if hash2(wx, 999, self.seed + 5) < 0.45:
                chunk.blocks[WORLD_HEIGHT - 2][lx] = BEDROCK

        for lx in range(CHUNK_W):
            wx = cx * CHUNK_W + lx
            for y in range(10, WORLD_HEIGHT - 4):
                if chunk.blocks[y][lx] in (AIR, WATER, BEDROCK): continue
                c1 = fbm(wx*0.07, y*0.07, 2, seed=self.seed+500)
                if c1 > 0.65: chunk.blocks[y][lx] = AIR

        for lx in range(CHUNK_W):
            wx = cx * CHUNK_W + lx
            for y in range(6, WORLD_HEIGHT - 3):
                if chunk.blocks[y][lx] != STONE: continue
                r = hash2(wx, y, self.seed + 700)
                if y > 78 and r < 0.007: chunk.blocks[y][lx] = DIAMOND_ORE
                elif y > 68 and r < 0.014: chunk.blocks[y][lx] = GOLD_ORE
                elif y > 52 and r < 0.030: chunk.blocks[y][lx] = IRON_ORE
                elif y > 35 and r < 0.055: chunk.blocks[y][lx] = COAL_ORE
                elif r < 0.070: chunk.blocks[y][lx] = GRAVEL

        for wx in range(cx * CHUNK_W - 3, (cx + 1) * CHUNK_W + 3):
            self.try_place_tree(chunk, wx)

        for lx in range(CHUNK_W):
            wx = cx * CHUNK_W + lx
            _, biome = self.get_column_info(wx)
            if biome == 'Снега':
                for y in range(WORLD_HEIGHT):
                    if chunk.blocks[y][lx] == WATER:
                        chunk.blocks[y][lx] = ICE; break

        if is_village:
            self.generate_village(chunk, cx)

        return chunk

    def _set_if_in_chunk(self, chunk, wx, wy, bid, only_air=False):
        if wx // CHUNK_W != chunk.cx: return
        if wy < 0 or wy >= WORLD_HEIGHT: return
        lx = wx % CHUNK_W
        if only_air and chunk.blocks[wy][lx] != AIR: return
        chunk.blocks[wy][lx] = bid

    def try_place_tree(self, chunk, wx):
        surface_y, biome = self.get_column_info(wx)
        if biome not in ('Лес', 'Равнины', 'Снега'): return
        if surface_y >= SEA_LEVEL: return
        r = hash2(wx, 1, self.seed + 800)
        if biome == 'Лес' and r > 0.18: return
        if biome == 'Равнины' and r > 0.04: return
        if biome == 'Снега' and r > 0.08: return
        trunk_h = 4 + int(hash2(wx, 2, self.seed + 801) * 3)
        for i in range(trunk_h):
            self._set_if_in_chunk(chunk, wx, surface_y - 1 - i, WOOD)
        cy = surface_y - trunk_h
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if abs(dx) == 2 and abs(dy) == 2: continue
                if abs(dx) + abs(dy) >= 4: continue
                self._set_if_in_chunk(chunk, wx + dx, cy + dy, LEAVES, only_air=True)

    def generate_village(self, chunk, cx):
        wx_center = cx * CHUNK_W + CHUNK_W // 2
        sy, _ = self.get_column_info(wx_center)
        ground = sy - 1

        for lx in range(CHUNK_W):
            for y in range(ground - 8, WORLD_HEIGHT):
                if y < ground: chunk.blocks[y][lx] = AIR
                elif y == ground: chunk.blocks[y][lx] = GRAVEL
            for y in range(ground - 8, ground):
                chunk.blocks[y][lx] = AIR

        def setb(wx, wy, b):
            lx = wx - cx * CHUNK_W
            if 0 <= lx < CHUNK_W and 0 <= wy < WORLD_HEIGHT:
                chunk.blocks[wy][lx] = b

        hx = cx * CHUNK_W
        hw = 5; hh = 5
        for x in range(hx, hx + hw):
            for y in range(ground - hh, ground):
                is_wall = x == hx or x == hx + hw - 1 or y == ground - hh
                if is_wall:
                    setb(x, y, WOOD)
        for x in range(hx, hx + hw):
            setb(x, ground - hh - 1, PLANKS)
        setb(hx + hw // 2, ground - 1, AIR)
        setb(hx + hw // 2, ground - 2, AIR)

        chest_x = hx + 1; chest_y = ground - 1
        setb(chest_x, chest_y, CHEST)
        self.chest_loot[(chest_x, chest_y)] = self._roll_chest_loot()

        stall_x = cx * CHUNK_W + CHUNK_W - 2
        stall_y = ground - 1
        setb(stall_x, stall_y, STALL)
        setb(stall_x, stall_y - 1, STALL)
        self.stall_data[(stall_x, stall_y)] = self._roll_stall_stock()
        self.stall_data[(stall_x, stall_y - 1)] = self.stall_data[(stall_x, stall_y)]

        chest2_x = cx * CHUNK_W + CHUNK_W - 5
        chest2_y = ground - 1
        lx2 = chest2_x - cx * CHUNK_W
        if 0 <= lx2 < CHUNK_W and chunk.blocks[chest2_y][lx2] == GRAVEL:
            setb(chest2_x, chest2_y, CHEST)
            self.chest_loot[(chest2_x, chest2_y)] = self._roll_chest_loot()

    def _roll_chest_loot(self):
        loot = [(COIN, random.randint(5, 15))]
        if random.random() < 0.8:
            loot.append((random.choice([APPLE, BREAD, RAW_PORK, RAW_BEEF]), random.randint(1, 4)))
        r = random.random()
        if r < 0.25:
            loot.append((random.choice([WOOD_SWORD, STONE_SWORD, IRON_SWORD]), 1))
        elif r < 0.45:
            loot.append((random.choice([WOOD_PICK, STONE_PICK, IRON_PICK]), 1))
        if random.random() < 0.15:
            loot.append((DIAMOND, random.randint(1, 2)))
        return loot

    def _roll_stall_stock(self):
        return [
            (APPLE, 3), (BREAD, 4), (RAW_PORK, 5), (RAW_BEEF, 6),
            (STONE_SWORD, 20), (IRON_SWORD, 45), (DIAMOND_SWORD, 120),
            (STONE_PICK, 20), (IRON_PICK, 45), (DIAMOND_PICK, 120),
        ]

    def physics_tick(self, cam_x, cam_y):
        self.tick_timer += 1
        if self.tick_timer % 4 != 0: return
        cx_min = int((cam_x - 6 * TILE_SIZE) // (CHUNK_W * TILE_SIZE))
        cx_max = int((cam_x + SCREEN_W + 6 * TILE_SIZE) // (CHUNK_W * TILE_SIZE))
        for cx in range(cx_min, cx_max + 1):
            chunk = self.get_chunk(cx)
            for y in range(WORLD_HEIGHT - 2, -1, -1):
                for lx in range(CHUNK_W):
                    b = chunk.blocks[y][lx]
                    if b not in FALLING_BLOCKS: continue
                    if chunk.blocks[y + 1][lx] in (AIR, WATER):
                        chunk.blocks[y + 1][lx] = b
                        chunk.blocks[y][lx] = AIR

# ============ СТАТИСТИКА ============
class Stats:
    def __init__(self):
        self.deaths = 0
        self.mobs_killed = 0
        self.blocks_mined = 0
        self.diamonds_mined = 0
        self.coins_earned = 0
        self.start_time = time.time()
        self.death_reasons = []

stats = Stats()

# ============ ИГРОК ============
class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx, self.vy = 0, 0
        self.w, self.h = 24, 48
        self.on_ground = False
        self.facing = 1
        self.in_water = False
        self.health = MAX_HEALTH
        self.max_health = MAX_HEALTH
        self.hunger = MAX_HUNGER
        self.max_hunger = MAX_HUNGER
        self.hunger_timer = 0
        self.regen_timer = 0
        self.starve_timer = 0
        self.hurt_cooldown = 0
        self.attack_cooldown = 0
        self.eat_cooldown = 0
        self.fall_start_y = y
        self.drowning_timer = 0
        self.dead = False
        self.death_reason = ""

        self.inventory = {}
        self.hotbar = []
        self.selected_slot = 0

        self.add_item(COIN, 10)
        self.add_item(WOOD_SWORD, 1)
        self.add_item(WOOD_PICK, 1)
        self.add_item(BREAD, 3)

        self.hotbar = [WOOD_SWORD, WOOD_PICK, GRASS, DIRT, STONE,
                       WOOD, PLANKS, BREAD, COIN]
        self.selected_slot = 0

    def has_item(self, item_id):
        if ITEM_INFO[item_id]["type"] == "block": return True
        return self.inventory.get(item_id, 0) > 0

    def count_item(self, item_id):
        return self.inventory.get(item_id, 0)

    def add_item(self, item_id, count=1):
        if ITEM_INFO[item_id]["type"] == "block":
            if item_id not in self.hotbar and len(self.hotbar) < 9:
                self.hotbar.append(item_id)
            return
        self.inventory[item_id] = self.inventory.get(item_id, 0) + count
        if item_id not in self.hotbar and len(self.hotbar) < 9:
            self.hotbar.append(item_id)

    def use_item(self, item_id, count=1):
        if ITEM_INFO[item_id]["type"] == "block": return True
        if self.inventory.get(item_id, 0) < count: return False
        self.inventory[item_id] -= count
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
            if item_id in self.hotbar:
                self.hotbar.remove(item_id)
                if self.selected_slot >= len(self.hotbar) and self.hotbar:
                    self.selected_slot = len(self.hotbar) - 1
        return True

    def eat(self, item_id):
        if self.eat_cooldown > 0 or self.dead: return False
        if self.hunger >= self.max_hunger: return False
        info_ = FOOD_INFO.get(item_id)
        if not info_: return False
        if not self.use_item(item_id): return False
        self.hunger = min(self.max_hunger, self.hunger + info_["feed"])
        self.health = min(self.max_health, self.health + info_["heal"])
        self.eat_cooldown = 30
        return True

    def get_attack_damage(self, item_id):
        if item_id in WEAPON_INFO:
            return WEAPON_INFO[item_id]["damage"]
        return 1

    def get_mining_speed(self, item_id):
        if item_id in PICK_INFO:
            return PICK_INFO[item_id]["speed"]
        return 6

    def update(self, keys, world):
        if self.dead: return
        self.vx = 0
        moving = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED; self.facing = -1; moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED; self.facing = 1; moving = True

        cx = int((self.x + self.w / 2) // TILE_SIZE)
        cy = int((self.y + self.h / 2) // TILE_SIZE)
        self.in_water = world.get_block(cx, cy) == WATER

        jump_key = keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]

        if self.in_water:
            self.vy *= 0.9
            self.vy = min(self.vy + 0.15, 3)
            if jump_key: self.vy = -3.5
            self.drowning_timer += 1
            if self.drowning_timer > 300:
                self.drowning_timer = 0
                self.take_damage(2, "Утонул")
        else:
            self.drowning_timer = 0
            self.vy = min(self.vy + GRAVITY, 18)
            if jump_key and self.on_ground:
                self.vy = JUMP_VEL; self.on_ground = False
                moving = True

        if self.on_ground: self.fall_start_y = self.y
        self.x += self.vx
        self.collide_x(world)
        self.y += self.vy
        prev_on_ground = self.on_ground
        self.on_ground = False
        self.collide_y(world)

        if self.on_ground and not prev_on_ground:
            fall_dist = (self.y - self.fall_start_y) / TILE_SIZE
            if fall_dist > 3.5:
                dmg = int((fall_dist - 3) * 2)
                if dmg > 0: self.take_damage(dmg, "Упал с высоты")

        if self.hurt_cooldown > 0: self.hurt_cooldown -= 1
        if self.attack_cooldown > 0: self.attack_cooldown -= 1
        if self.eat_cooldown > 0: self.eat_cooldown -= 1

        if self.hurt_cooldown == 0:
            for dy in (0, self.h // 2, self.h - 2):
                bcx = int((self.x + self.w / 2) // TILE_SIZE)
                bcy = int((self.y + dy) // TILE_SIZE)
                b = world.get_block(bcx, bcy)
                if BLOCK_INFO.get(b, {}).get("damage"):
                    self.take_damage(BLOCK_INFO[b]["damage"], "Кактус")
                    break

        self.hunger_timer += 1
        threshold = HUNGER_DRAIN_MOVE if moving else HUNGER_DRAIN_STAND
        if self.hunger_timer >= threshold:
            self.hunger_timer = 0
            if self.hunger > 0: self.hunger -= 1

        if self.hunger >= 18 and self.health < self.max_health and not self.dead:
            self.regen_timer += 1
            if self.regen_timer >= REGEN_INTERVAL:
                self.regen_timer = 0
                self.health = min(self.max_health, self.health + 1)
        else:
            self.regen_timer = 0

        if self.hunger == 0 and not self.dead:
            self.starve_timer += 1
            if self.starve_timer >= STARVE_INTERVAL:
                self.starve_timer = 0
                self.take_damage(1, "Голод")
        else:
            self.starve_timer = 0

    def collide_x(self, world):
        if self.vx == 0: return
        left = int(self.x // TILE_SIZE); right = int((self.x + self.w - 1) // TILE_SIZE)
        top = int(self.y // TILE_SIZE); bottom = int((self.y + self.h - 1) // TILE_SIZE)
        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                if BLOCK_INFO[world.get_block(tx, ty)]["solid"]:
                    if self.vx > 0: self.x = tx * TILE_SIZE - self.w
                    else: self.x = (tx + 1) * TILE_SIZE
                    return

    def collide_y(self, world):
        left = int(self.x // TILE_SIZE); right = int((self.x + self.w - 1) // TILE_SIZE)
        top = int(self.y // TILE_SIZE); bottom = int((self.y + self.h - 1) // TILE_SIZE)
        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                if BLOCK_INFO[world.get_block(tx, ty)]["solid"]:
                    if self.vy > 0:
                        self.y = ty * TILE_SIZE - self.h; self.vy = 0; self.on_ground = True
                    elif self.vy < 0:
                        self.y = (ty + 1) * TILE_SIZE; self.vy = 0
                    return

    def take_damage(self, amount, reason=""):
        if self.dead or self.hurt_cooldown > 0: return
        self.health -= amount
        self.hurt_cooldown = INVULN_FRAMES
        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.death_reason = reason
            stats.deaths += 1
            stats.death_reasons.append(reason)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, surf, cx, cy):
        if self.dead: return
        px, py = int(self.x - cx), int(self.y - cy)
        w, h = self.w, self.h
        if self.hurt_cooldown > 0 and (self.hurt_cooldown // 3) % 2 == 0:
            return
        pygame.draw.rect(surf, (50, 60, 120), (px, py + h - 12, w // 2 - 1, 12))
        pygame.draw.rect(surf, (50, 60, 120), (px + w // 2 + 1, py + h - 12, w // 2 - 1, 12))
        pygame.draw.rect(surf, (70, 130, 200), (px, py + 18, w, h - 30))
        pygame.draw.rect(surf, (235, 185, 145), (px, py, w, 18))
        pygame.draw.rect(surf, (60, 40, 25), (px, py, w, 5))
        eo = 0 if self.facing > 0 else -4
        pygame.draw.rect(surf, (30, 30, 30), (px + 5 + eo, py + 8, 4, 4))
        pygame.draw.rect(surf, (30, 30, 30), (px + 15 + eo, py + 8, 4, 4))
        pygame.draw.rect(surf, (120, 70, 60), (px + 8, py + 14, 8, 2))

# ============ МОБЫ ============
MOB_TYPES = {
    'zombie':  {'name': 'Зомби', 'w':24,'h':48,'hp':20,'speed':1.2,'hostile':True,
                'color':(60,130,60),'head':(100,160,100),'eye':(30,30,30),
                'damage':3,'attack_range':TILE_SIZE*1.2,
                'drops':[(COIN,(1,3))]},
    'skeleton':{'name': 'Скелет', 'w':22,'h':46,'hp':16,'speed':1.4,'hostile':True,
                'color':(200,200,190),'head':(230,230,220),'eye':(20,20,20),
                'damage':2,'attack_range':TILE_SIZE*1.2,
                'drops':[(COIN,(2,4))]},
    'creeper': {'name': 'Крипер', 'w':26,'h':42,'hp':20,'speed':1.3,'hostile':True,
                'color':(60,180,60),'head':(80,200,80),'eye':(0,0,0),
                'damage':6,'attack_range':TILE_SIZE*1.4,
                'drops':[(COIN,(3,6))]},
    'pig':     {'name': 'Свинья', 'w':32,'h':24,'hp':10,'speed':0.8,'hostile':False,
                'color':(230,150,165),'head':(245,180,190),'eye':(30,30,30),
                'damage':0,'attack_range':0,
                'drops':[(RAW_PORK,(1,2))]},
    'cow':     {'name': 'Корова', 'w':34,'h':30,'hp':10,'speed':0.7,'hostile':False,
                'color':(200,200,200),'head':(240,240,240),'eye':(30,30,30),
                'damage':0,'attack_range':0,
                'drops':[(RAW_BEEF,(1,2))]},
    'sheep':   {'name': 'Овца', 'w':32,'h':28,'hp':8,'speed':0.8,'hostile':False,
                'color':(240,240,240),'head':(255,220,210),'eye':(30,30,30),
                'damage':0,'attack_range':0,
                'drops':[(RAW_MUTTON,(1,2))]},
}

class Mob:
    def __init__(self, mob_type, x, y):
        self.type = mob_type
        info_ = MOB_TYPES[mob_type]
        self.w = info_['w']; self.h = info_['h']
        self.x, self.y = x, y
        self.vx, self.vy = 0, 0
        self.hp = info_['hp']; self.max_hp = info_['hp']
        self.on_ground = False
        self.facing = random.choice([-1, 1])
        self.hostile = info_['hostile']
        self.speed = info_['speed']
        self.wander_timer = 0
        self.wander_dir = 0
        self.attack_cooldown = 0
        self.hurt_flash = 0
        self.death_anim = 0
        self.dead = False
        self.dropped = False
        self.killed_by_player = False

    def update(self, world, player):
        if self.dead:
            self.death_anim += 1
            return
        if self.hurt_flash > 0: self.hurt_flash -= 1
        if self.attack_cooldown > 0: self.attack_cooldown -= 1

        dx = (player.x + player.w / 2) - (self.x + self.w / 2)
        dy = (player.y + player.h / 2) - (self.y + self.h / 2)
        dist = math.hypot(dx, dy)

        if self.hostile:
            if dist < 14 * TILE_SIZE:
                if dx > 0: self.vx = self.speed; self.facing = 1
                else: self.vx = -self.speed; self.facing = -1
                if self.on_ground and abs(dx) < 3 * TILE_SIZE and dy < -TILE_SIZE:
                    self.vy = -11; self.on_ground = False
                if dist < MOB_TYPES[self.type]['attack_range'] and self.attack_cooldown == 0:
                    if not player.dead:
                        player.take_damage(MOB_TYPES[self.type]['damage'],
                                           f"Убит {MOB_TYPES[self.type]['name']}")
                        self.attack_cooldown = 45
            else:
                self._wander()
        else:
            if dist < 6 * TILE_SIZE and not player.dead:
                if dx > 0: self.vx = -self.speed * 1.3; self.facing = -1
                else: self.vx = self.speed * 1.3; self.facing = 1
                if self.on_ground and random.random() < 0.05:
                    self.vy = -10; self.on_ground = False
            else:
                self._wander()

        self.vy = min(self.vy + GRAVITY, 18)
        self.x += self.vx
        self.collide_x(world)
        self.y += self.vy
        self.on_ground = False
        self.collide_y(world)

        if self.vy > 15 and self.on_ground:
            self.hp -= 2
            if self.hp <= 0 and not self.dead:
                self.dead = True; self.death_anim = 0

        cx = int((self.x + self.w / 2) // TILE_SIZE)
        cy = int((self.y + self.h / 2) // TILE_SIZE)
        if world.get_block(cx, cy) == WATER: self.vy = -2

    def _wander(self):
        self.wander_timer -= 1
        if self.wander_timer <= 0:
            self.wander_timer = random.randint(40, 180)
            self.wander_dir = random.choice([-1, 0, 1])
        if self.wander_dir == 0:
            self.vx = 0
        else:
            self.vx = self.speed * 0.5 * self.wander_dir
            self.facing = self.wander_dir
            if self.on_ground and random.random() < 0.02:
                self.vy = -10; self.on_ground = False

    def collide_x(self, world):
        if self.vx == 0: return
        left = int(self.x // TILE_SIZE); right = int((self.x + self.w - 1) // TILE_SIZE)
        top = int(self.y // TILE_SIZE); bottom = int((self.y + self.h - 1) // TILE_SIZE)
        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                if BLOCK_INFO[world.get_block(tx, ty)]["solid"]:
                    if self.vx > 0: self.x = tx * TILE_SIZE - self.w
                    else: self.x = (tx + 1) * TILE_SIZE
                    return

    def collide_y(self, world):
        left = int(self.x // TILE_SIZE); right = int((self.x + self.w - 1) // TILE_SIZE)
        top = int(self.y // TILE_SIZE); bottom = int((self.y + self.h - 1) // TILE_SIZE)
        for ty in range(top, bottom + 1):
            for tx in range(left, right + 1):
                if BLOCK_INFO[world.get_block(tx, ty)]["solid"]:
                    if self.vy > 0:
                        self.y = ty * TILE_SIZE - self.h; self.vy = 0; self.on_ground = True
                    elif self.vy < 0:
                        self.y = (ty + 1) * TILE_SIZE; self.vy = 0
                    return

    def take_damage(self, amount, knock_from_x=None, by_player=False):
        if self.dead: return
        self.hp -= amount
        self.hurt_flash = 8
        if knock_from_x is not None:
            dx = (self.x + self.w / 2) - knock_from_x
            if dx > 0: self.vx = 6
            else: self.vx = -6
            self.vy = -4; self.on_ground = False
        if self.hp <= 0:
            self.dead = True
            self.death_anim = 0
            self.killed_by_player = by_player
            if by_player:
                stats.mobs_killed += 1

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, surf, cx, cy):
        px, py = int(self.x - cx), int(self.y - cy)
        info_ = MOB_TYPES[self.type]
        if self.dead:
            a = max(0, 255 - self.death_anim * 20)
            if a <= 0: return
            s = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            s.fill((*info_['color'], a))
            surf.blit(s, (px, py + self.death_anim))
            return
        col = info_['color']; head_c = info_['head']
        if self.hurt_flash > 0:
            col = (255, 120, 120); head_c = (255, 160, 160)
        body_top = py + self.h // 3
        pygame.draw.rect(surf, col, (px, body_top, self.w, self.h - self.h // 3))
        head_h = self.h // 3
        pygame.draw.rect(surf, head_c, (px, py, self.w, head_h))
        eo = 0 if self.facing > 0 else -4
        eye_c = info_['eye']
        if self.type in ('pig', 'cow', 'sheep'):
            pygame.draw.rect(surf, (180, 100, 110) if self.type == 'pig' else (100, 80, 70),
                             (px + 4 + eo, py + head_h - 6, 6, 4))
            pygame.draw.rect(surf, eye_c, (px + 3, py + 4, 3, 3))
            pygame.draw.rect(surf, eye_c, (px + self.w - 6, py + 4, 3, 3))
        else:
            pygame.draw.rect(surf, eye_c, (px + 4 + eo, py + 4, 4, 4))
            pygame.draw.rect(surf, eye_c, (px + self.w - 8 + eo, py + 4, 4, 4))
            if self.type == 'zombie':
                pygame.draw.rect(surf, (100, 30, 30), (px + 4, py + head_h - 4, self.w - 8, 3))
        if self.hp < self.max_hp and not self.dead:
            ratio = max(0, self.hp / self.max_hp)
            pygame.draw.rect(surf, (60, 20, 20), (px, py - 6, self.w, 3))
            pygame.draw.rect(surf, (60, 220, 60), (px, py - 6, int(self.w * ratio), 3))

# ============ СПАВН ============
def spawn_mob_near_player(world, player, is_night):
    side = random.choice([-1, 1])
    dist = random.randint(SPAWN_RADIUS_MIN, SPAWN_RADIUS_MAX)
    wx = int(player.x // TILE_SIZE) + side * (dist // TILE_SIZE)
    if world.is_village_chunk(wx // CHUNK_W): return None
    surface_y, _ = world.get_column_info(wx)
    wy = surface_y - 1
    found = False
    for dy in range(-3, 8):
        ty = surface_y - 1 + dy
        if world.get_block(wx, ty) == AIR and BLOCK_INFO[world.get_block(wx, ty + 1)]["solid"]:
            wy = ty; found = True; break
    if not found: return None
    if is_night:
        mob_type = random.choice(['zombie', 'zombie', 'skeleton', 'creeper'])
    else:
        mob_type = random.choice(['pig', 'cow', 'sheep'])
    x = wx * TILE_SIZE + TILE_SIZE // 2 - MOB_TYPES[mob_type]['w'] // 2
    y = wy * TILE_SIZE + TILE_SIZE - MOB_TYPES[mob_type]['h']
    return Mob(mob_type, x, y)

# ============ МИР / ИГРОК ============
world = World(seed=random.randint(0, 9999))
spawn_wx = 0
spawn_sy, _ = world.get_column_info(spawn_wx)
player = Player(spawn_wx * TILE_SIZE, (spawn_sy - 3) * TILE_SIZE)
mobs = []

# ============ UI ============
def draw_heart(surf, x, y, color):
    pygame.draw.rect(surf, color, (x + 2, y + 2, 14, 8))
    pygame.draw.rect(surf, color, (x + 2, y + 8, 4, 4))
    pygame.draw.rect(surf, color, (x + 12, y + 8, 4, 4))
    pygame.draw.rect(surf, color, (x + 4, y + 10, 10, 4))
    pygame.draw.rect(surf, color, (x + 6, y + 12, 6, 2))
    pygame.draw.rect(surf, (255, 180, 180), (x + 4, y + 3, 3, 3))

def draw_heart_half(surf, x, y, color):
    pygame.draw.rect(surf, color, (x + 2, y + 2, 7, 8))
    pygame.draw.rect(surf, color, (x + 2, y + 8, 4, 4))
    pygame.draw.rect(surf, color, (x + 4, y + 10, 5, 4))
    pygame.draw.rect(surf, color, (x + 6, y + 12, 3, 2))

def draw_drumstick(surf, x, y, color):
    pygame.draw.circle(surf, color, (x + 8, y + 7), 7)
    pygame.draw.circle(surf, tuple(max(0, c - 40) for c in color), (x + 8, y + 7), 7, 2)
    pygame.draw.circle(surf, tuple(min(255, c + 50) for c in color), (x + 6, y + 5), 2)
    pygame.draw.rect(surf, (245, 245, 230), (x + 12, y + 12, 4, 5))
    pygame.draw.circle(surf, (245, 245, 230), (x + 13, y + 17), 2)
    pygame.draw.circle(surf, (245, 245, 230), (x + 16, y + 17), 2)

def draw_hunger_bar(surf, player):
    slots = player.max_hunger // 2
    total_w = slots * 22
    x0 = SCREEN_W - total_w - 12
    y0 = SCREEN_H - 40
    for i in range(slots):
        hx = x0 + i * 22
        hp = player.hunger - i * 2
        draw_drumstick(surf, hx, y0, (90, 50, 30))
        if hp >= 2:
            draw_drumstick(surf, hx, y0, (200, 130, 70))
        elif hp == 1:
            pygame.draw.circle(surf, (200, 130, 70), (hx + 8, y0 + 7), 7)
            s = pygame.Surface((22, 22), pygame.SRCALPHA)
            pygame.draw.rect(s, (60, 30, 20, 200), (9, 0, 13, 22))
            surf.blit(s, (hx, y0))
            pygame.draw.rect(surf, (245, 245, 230), (hx + 12, y0 + 12, 4, 5))
            pygame.draw.circle(surf, (245, 245, 230), (hx + 13, y0 + 17), 2)
            pygame.draw.circle(surf, (245, 245, 230), (hx + 16, y0 + 17), 2)

def draw_hotbar(surf, player):
    slots = player.hotbar
    n = len(slots)
    if n == 0: return
    slot_size = 60
    total = n * slot_size
    start_x = (SCREEN_W - total) // 2
    y = SCREEN_H - 70
    bg = pygame.Surface((total + 10, 70), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 150))
    surf.blit(bg, (start_x - 5, y - 5))
    for i, item_id in enumerate(slots):
        x = start_x + i * slot_size
        rect = pygame.Rect(x + 2, y + 2, slot_size - 4, slot_size - 4)
        if i == player.selected_slot:
            pygame.draw.rect(surf, (255, 240, 130), rect.inflate(6, 6), 3)
        pygame.draw.rect(surf, (75, 75, 75), rect)
        pygame.draw.rect(surf, (35, 35, 35), rect, 2)
        tex = get_tex(item_id)
        if tex:
            icon = pygame.transform.scale(tex, (slot_size - 14, slot_size - 14))
            surf.blit(icon, (x + 7, y + 7))
        if ITEM_INFO[item_id].get("stackable", False):
            cnt = player.count_item(item_id)
            if cnt > 1:
                t = font.render(str(cnt), True, (255, 255, 255))
                tg = font.render(str(cnt), True, (0, 0, 0))
                surf.blit(tg, (x + slot_size - 17, y + slot_size - 23))
                surf.blit(t, (x + slot_size - 18, y + slot_size - 24))
        num = font.render(str((i + 1) % 10), True, (255, 255, 255))
        surf.blit(num, (x + 6, y + 4))
    if 0 <= player.selected_slot < n:
        item_id = slots[player.selected_slot]
        info_ = ITEM_INFO[item_id]
        name_str = info_["name"]
        if info_["type"] == "food":
            name_str += f" (+{info_['heal']} HP, +{info_['feed']} еды)"
        elif info_["type"] == "weapon":
            name_str += f" (Урон: {info_['damage']})"
        elif info_["type"] == "pick":
            name_str += f" (Скорость: x{7-info_['speed']})"
        name = font_med.render(name_str, True, (255, 255, 255))
        nb = pygame.Surface((name.get_width() + 24, name.get_height() + 12), pygame.SRCALPHA)
        nb.fill((0, 0, 0, 170))
        surf.blit(nb, (SCREEN_W // 2 - name.get_width() // 2 - 12, y - 50))
        surf.blit(name, (SCREEN_W // 2 - name.get_width() // 2, y - 44))

def draw_quest(surf, player):
    diamonds = player.count_item(DIAMOND)
    coins = player.count_item(COIN)
    w = 300; h = 110
    x = SCREEN_W - w - 20
    y = 20
    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 160))
    pygame.draw.rect(panel, (240, 200, 60), (0, 0, w, h), 2)
    surf.blit(panel, (x, y))
    title = font_med.render("ЦЕЛЬ ПОБЕДЫ", True, (240, 200, 60))
    surf.blit(title, (x + 12, y + 8))
    d_ok = "[X]" if diamonds >= GOAL_DIAMONDS else "[ ]"
    d_t = font.render(f"{d_ok} Алмазы: {diamonds}/{GOAL_DIAMONDS}", True, (255, 255, 255))
    surf.blit(d_t, (x + 12, y + 42))
    c_ok = "[X]" if coins >= GOAL_COINS else "[ ]"
    c_t = font.render(f"{c_ok} Монеты: {coins}/{GOAL_COINS}", True, (255, 255, 255))
    surf.blit(c_t, (x + 12, y + 66))
    if diamonds >= GOAL_DIAMONDS and coins >= GOAL_COINS:
        s_t = font.render("ГОТОВО!", True, (100, 255, 100))
    else:
        s_t = font.render("Собери ресурсы", True, (200, 200, 200))
    surf.blit(s_t, (x + 12, y + 88))

def draw_ui(surf, player, world, fps, biome, time_of_day):
    hours = int((time_of_day * 24 + 6) % 24)
    minutes = int((time_of_day * 24 * 60) % 60)
    info_lines = [
        f"FPS: {int(fps)}",
        f"X: {int(player.x // TILE_SIZE)}  Y: {int(player.y // TILE_SIZE)}",
        f"Биом: {biome}",
        f"Время: {hours:02d}:{minutes:02d}",
        f"Смертей: {stats.deaths}  |  Убито мобов: {stats.mobs_killed}",
    ]
    y = 10
    for line in info_lines:
        t = font.render(line, True, (255, 255, 255))
        bg = pygame.Surface((t.get_width() + 12, t.get_height() + 4), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 140))
        surf.blit(bg, (10, y)); surf.blit(t, (16, y + 2))
        y += t.get_height() + 6

def draw_death_screen(surf, player):
    ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    ov.fill((120, 0, 0, 140))
    surf.blit(ov, (0, 0))
    t1 = font_huge.render("ВЫ ПОГИБЛИ", True, (255, 220, 220))
    reason = font_med.render(player.death_reason or "", True, (255, 200, 200))
    deaths_text = font_med.render(f"Всего смертей: {stats.deaths}", True, (255, 220, 220))
    t2 = font_med.render("Нажмите R для возрождения", True, (255, 255, 255))
    surf.blit(t1, (SCREEN_W // 2 - t1.get_width() // 2, SCREEN_H // 2 - 140))
    if reason.get_width() > 0:
        surf.blit(reason, (SCREEN_W // 2 - reason.get_width() // 2, SCREEN_H // 2 - 50))
    surf.blit(deaths_text, (SCREEN_W // 2 - deaths_text.get_width() // 2, SCREEN_H // 2 - 20))
    surf.blit(t2, (SCREEN_W // 2 - t2.get_width() // 2, SCREEN_H // 2 + 30))

# ============ ФОН ============
def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def get_sky_color(t):
    brightness = (math.cos((t - 0.5) * 2 * math.pi) + 1) / 2
    day = (135, 206, 235); night = (10, 15, 45); sunset = (255, 130, 80)
    if brightness > 0.5:
        return lerp(sunset, day, (brightness - 0.5) * 2), brightness
    return lerp(night, sunset, brightness * 2), brightness

def draw_sun_moon(surf, t):
    angle = (t - 0.25) * 2 * math.pi
    sx = SCREEN_W * (0.5 - math.cos(angle) * 0.5)
    sy = SCREEN_H * 0.7 - math.sin(angle) * SCREEN_H * 0.7
    if math.sin(angle) > -0.2:
        a = max(0, min(255, int(255 * (math.sin(angle) + 0.2) / 1.2)))
        s = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 240, 150, a), (60, 60), 50)
        surf.blit(s, (sx - 60, sy - 60))
    if math.sin(angle) < 0.2:
        a = max(0, min(255, int(255 * (0.2 - math.sin(angle)) / 1.2)))
        m = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(m, (230, 230, 240, a), (40, 40), 30)
        surf.blit(m, (sx - 40, sy - 40))

def draw_clouds(surf, cam_x, cam_y):
    for i in range(25):
        base_x = i * 340
        cy = 60 + (i * 73) % 160
        px = (base_x - cam_x * 0.35) % (SCREEN_W + 500) - 250
        py = cy - cam_y * 0.35
        pygame.draw.ellipse(surf, (255, 255, 255), (px, py, 110, 38))
        pygame.draw.ellipse(surf, (255, 255, 255), (px + 35, py - 14, 95, 42))
        pygame.draw.ellipse(surf, (255, 255, 255), (px + 75, py, 85, 38))

def draw_world(surf, world, cam_x, cam_y, time_of_day):
    brightness = (math.cos((time_of_day - 0.5) * 2 * math.pi) + 1) / 2
    first_cx = math.floor(cam_x / (CHUNK_W * TILE_SIZE))
    last_cx = math.floor((cam_x + SCREEN_W - 1) / (CHUNK_W * TILE_SIZE))
    first_wy = max(0, math.floor(cam_y / TILE_SIZE))
    last_wy = min(WORLD_HEIGHT - 1, math.floor((cam_y + SCREEN_H - 1) / TILE_SIZE))
    for cx in range(first_cx, last_cx + 1):
        chunk = world.get_chunk(cx)
        base_sx = cx * CHUNK_W * TILE_SIZE - cam_x
        for lx in range(CHUNK_W):
            sx = base_sx + lx * TILE_SIZE
            if sx < -TILE_SIZE or sx > SCREEN_W: continue
            for wy in range(first_wy, last_wy + 1):
                b = chunk.blocks[wy][lx]
                if b == AIR: continue
                surf.blit(BLOCK_TEX[b], (sx, wy * TILE_SIZE - cam_y))
    if brightness < 0.5:
        alpha = int((0.5 - brightness) * 2 * 160)
        if alpha > 0:
            ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            ov.fill((10, 20, 70, alpha))
            surf.blit(ov, (0, 0))

# ============ ИНТРО ============
def draw_intro(surf, t):
    surf.fill((8, 8, 18))
    rng = random.Random(12345)
    for _ in range(200):
        x = rng.randint(0, SCREEN_W)
        y = rng.randint(0, SCREEN_H // 2)
        brightness = 100 + int(155 * abs(math.sin(t * 0.5 + x * 0.01)))
        pygame.draw.circle(surf, (brightness, brightness, brightness), (x, y), 1)

    title = font_huge.render("МАЙНКРАФТ 2D", True, (240, 220, 120))
    surf.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 20))

    if t > 0.3:
        subtitle = font_med.render(f"От создателей: {AUTHORS}", True, (180, 220, 255))
        surf.blit(subtitle, (SCREEN_W // 2 - subtitle.get_width() // 2, 95))
        line = pygame.Surface((subtitle.get_width() + 40, 2), pygame.SRCALPHA)
        line.fill((180, 220, 255, 180))
        surf.blit(line, (SCREEN_W // 2 - line.get_width() // 2, 125))

    story = [
        "",
        "Ты — обычный игрок в Minecraft. Однажды ночью,",
        "исследуя старую шахту, ты наткнулся на странный портал.",
        "",
        "Ты шагнул в него... и очнулся здесь.",
        "Этот мир похож на твой, но что-то не так.",
        "Здесь есть деревни с торговцами, странные монеты,",
        "и опасные мобы, которые выходят по ночам.",
        "",
        "Чтобы вернуться домой, ты должен собрать:",
        f"  {GOAL_DIAMONDS} алмазов  и  {GOAL_COINS} монет,",
        "и найти путь назад через древний портал.",
    ]
    y = 145
    for i, line_text in enumerate(story):
        if t > 0.6 + i * 0.12:
            color = (220, 220, 220)
            if "алмазов" in line_text or "портал" in line_text: color = (100, 230, 230)
            if "монет" in line_text: color = (240, 200, 60)
            if "деревни" in line_text: color = (240, 180, 100)
            txt = font_med.render(line_text, True, color)
            surf.blit(txt, (SCREEN_W // 2 - txt.get_width() // 2, y))
        y += 26

    if t > 3.5:
        box_w = 620
        box_h = 220
        box_x = SCREEN_W // 2 - box_w // 2
        box_y = SCREEN_H - 330
        box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box.fill((20, 20, 40, 210))
        pygame.draw.rect(box, (100, 180, 240), (0, 0, box_w, box_h), 2)
        surf.blit(box, (box_x, box_y))

        head = font_med.render("УПРАВЛЕНИЕ", True, (100, 220, 255))
        surf.blit(head, (box_x + box_w // 2 - head.get_width() // 2, box_y + 10))

        controls = [
            ("A / D  или  <- ->",        "Ходить"),
            ("SPACE / W / ^",            "Прыжок"),
            ("ЛКМ",                      "Копать / Атаковать мобов"),
            ("ПКМ",                      "Ставить / Есть / Сундук / Ларёк"),
            ("E",                        "Открыть ларёк (магазин)"),
            ("1-9  или  колесо мыши",    "Выбрать предмет"),
            ("R",                        "Возродиться после смерти"),
            ("F11",                      "Полный экран / окно"),
            ("ESC",                      "Выход"),
        ]
        y_c = box_y + 42
        for key, action in controls:
            k_txt = font.render(key, True, (255, 240, 130))
            a_txt = font.render(action, True, (230, 230, 230))
            surf.blit(k_txt, (box_x + 20, y_c))
            surf.blit(a_txt, (box_x + 290, y_c))
            y_c += 19

    if t > 4.5:
        blink = (math.sin(t * 4) + 1) / 2
        c = int(150 + 105 * blink)
        hint = font_med.render(">>> Нажмите ENTER чтобы начать <<<", True, (c, c, c))
        surf.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H - 55))

    if t > 1.0:
        footer = font_small.render(
            f"(c) {AUTHORS}  -  All Rights Reserved  -  2026",
            True, (120, 120, 140)
        )
        surf.blit(footer, (SCREEN_W // 2 - footer.get_width() // 2, SCREEN_H - 25))

# ============ ЭКРАН ПОБЕДЫ ============
def draw_victory(surf, t, player):
    surf.fill((5, 5, 20))
    rng = random.Random(999)
    for _ in range(300):
        x = rng.randint(0, SCREEN_W)
        y = rng.randint(0, SCREEN_H)
        b = 100 + int(155 * abs(math.sin(t + x * 0.01 + y * 0.01)))
        pygame.draw.circle(surf, (b, b, b), (x, y), 1)

    cx_portal = SCREEN_W // 2
    cy_portal = 130
    pulse = (math.sin(t * 3) + 1) / 2
    for r in range(110, 20, -10):
        col = (int(150 * pulse), int(100 + 100*pulse), 255)
        pygame.draw.circle(surf, col, (cx_portal, cy_portal), r, 2)
    for r in range(55, 15, -8):
        col = (int(200 * pulse), int(150 + 80*pulse), 255)
        pygame.draw.circle(surf, col, (cx_portal, cy_portal), r, 1)

    title = font_mega.render("ПОБЕДА!", True, (255, 230, 100))
    surf.blit(title, (SCREEN_W // 2 - title.get_width() // 2, cy_portal - 55))

    congrats = font_big.render(f"Поздравляем от команды {AUTHORS}!", True, (180, 220, 255))
    surf.blit(congrats, (SCREEN_W // 2 - congrats.get_width() // 2, cy_portal + 60))

    line1 = font_med.render("Ты собрал всё необходимое и вернулся домой через портал!",
                             True, (220, 220, 220))
    surf.blit(line1, (SCREEN_W // 2 - line1.get_width() // 2, cy_portal + 108))

    box_w = 780
    box_h = 300
    box_x = SCREEN_W // 2 - box_w // 2
    box_y = cy_portal + 155
    box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    box.fill((15, 15, 35, 220))
    pygame.draw.rect(box, (100, 200, 255), (0, 0, box_w, box_h), 2)
    surf.blit(box, (box_x, box_y))

    head = font_med.render("СТАТИСТИКА ПРОХОЖДЕНИЯ", True, (100, 220, 255))
    surf.blit(head, (box_x + box_w // 2 - head.get_width() // 2, box_y + 10))

    elapsed = int(time.time() - stats.start_time)
    mins = elapsed // 60
    secs = elapsed % 60

    left_stats = [
        ("Здоровье в конце:",   f"{player.health}/{player.max_health}"),
        ("Алмазов собрано:",    f"{stats.diamonds_mined}"),
        ("Монет заработано:",   f"{stats.coins_earned}"),
        ("Блоков накопано:",    f"{stats.blocks_mined}"),
    ]
    right_stats = [
        ("Мобов убито:",        f"{stats.mobs_killed}"),
        ("Раз погиб:",          f"{stats.deaths}"),
        ("Время игры:",         f"{mins} мин {secs} сек"),
        ("Финальный счёт:",     f"{player.count_item(DIAMOND)} алм / {player.count_item(COIN)} мон"),
    ]

    y_l = box_y + 55
    y_r = box_y + 55
    for label, val in left_stats:
        l = font.render(label, True, (200, 200, 200))
        v = font.render(val, True, (255, 240, 130))
        surf.blit(l, (box_x + 40, y_l))
        surf.blit(v, (box_x + 340, y_l))
        y_l += 28
    for label, val in right_stats:
        l = font.render(label, True, (200, 200, 200))
        v = font.render(val, True, (255, 240, 130))
        surf.blit(l, (box_x + 40, y_r))
        surf.blit(v, (box_x + 340, y_r))
        y_r += 28

    rating = "S"
    if stats.deaths >= 10: rating = "C"
    elif stats.deaths >= 5: rating = "B"
    elif stats.deaths >= 2: rating = "A"
    rating_color = {"S": (255, 230, 100), "A": (100, 255, 100),
                    "B": (255, 200, 100), "C": (255, 130, 100)}[rating]
    r_txt = font_big.render(f"Ранг: {rating}", True, rating_color)
    surf.blit(r_txt, (box_x + box_w // 2 - r_txt.get_width() // 2, box_y + box_h - 55))

    reason_txt = font_small.render(f"Ранг зависит от количества смертей (0-1=S, 2-4=A, 5-9=B, 10+=C)",
                                    True, (180, 180, 180))
    surf.blit(reason_txt, (box_x + box_w // 2 - reason_txt.get_width() // 2, box_y + box_h - 20))

    blink = (math.sin(t * 4) + 1) / 2
    c = int(150 + 105 * blink)
    hint = font_med.render("Нажмите ESC или кликните чтобы выйти", True, (c, c, c))
    surf.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H - 45))

# ============ МАГАЗИН ============
class ShopUI:
    def __init__(self, world, stall_pos):
        self.world = world
        self.stall_pos = stall_pos
        self.stock = world.stall_data.get(stall_pos, [])
        self.selected = 0
        self.hover = -1

    def handle_event(self, event, player):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_e):
                return "close"
            elif event.key == pygame.K_UP:
                if self.stock:
                    self.selected = (self.selected - 1) % len(self.stock)
            elif event.key == pygame.K_DOWN:
                if self.stock:
                    self.selected = (self.selected + 1) % len(self.stock)
            elif event.key == pygame.K_RETURN:
                self.try_buy(player)
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self.hover = -1
            for i in range(len(self.stock)):
                rect = self.get_item_rect(i)
                if rect.collidepoint(mx, my):
                    self.hover = i
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover >= 0:
                self.selected = self.hover
                self.try_buy(player)
        return None

    def try_buy(self, player):
        if not self.stock: return
        item_id, price = self.stock[self.selected]
        if player.count_item(COIN) < price: return
        player.use_item(COIN, price)
        cnt = 3 if ITEM_INFO[item_id]["type"] == "food" else 1
        player.add_item(item_id, cnt)

    def get_item_rect(self, i):
        w = 500
        x = SCREEN_W // 2 - w // 2
        y = SCREEN_H // 2 - 250 + 90 + i * 55
        return pygame.Rect(x + 20, y, w - 40, 50)

    def draw(self, surf, player):
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        surf.blit(ov, (0, 0))
        w = 500; h = 500
        x = SCREEN_W // 2 - w // 2
        y = SCREEN_H // 2 - h // 2
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((40, 30, 20, 240))
        pygame.draw.rect(panel, (240, 200, 60), (0, 0, w, h), 4)
        pygame.draw.rect(panel, (140, 90, 40), (0, 70, w, 4))
        surf.blit(panel, (x, y))
        title = font_big.render("ЛАРЁК", True, (240, 200, 60))
        surf.blit(title, (x + w // 2 - title.get_width() // 2, y + 15))
        coins = player.count_item(COIN)
        coin_txt = font_med.render(f"Монеты: {coins}", True, (255, 230, 120))
        surf.blit(coin_txt, (x + 20, y + h - 50))
        hint = font.render("Стрелки - выбрать, ENTER/ЛКМ - купить, ESC - закрыть",
                           True, (200, 200, 200))
        surf.blit(hint, (x + w // 2 - hint.get_width() // 2, y + h - 25))
        for i, (item_id, price) in enumerate(self.stock):
            rect = self.get_item_rect(i)
            is_sel = (i == self.selected)
            is_hover = (i == self.hover)
            bg_color = (90, 70, 40) if is_sel else (60, 50, 30)
            if is_hover: bg_color = (110, 90, 50)
            pygame.draw.rect(surf, bg_color, rect)
            if is_sel: pygame.draw.rect(surf, (240, 200, 60), rect, 3)
            tex = get_tex(item_id)
            if tex:
                icon = pygame.transform.scale(tex, (36, 36))
                surf.blit(icon, (rect.x + 8, rect.y + 7))
            name = font_med.render(ITEM_INFO[item_id]["name"], True, (255, 255, 255))
            surf.blit(name, (rect.x + 55, rect.y + 14))
            can_afford = player.count_item(COIN) >= price
            price_color = (100, 255, 100) if can_afford else (255, 100, 100)
            pt = font_med.render(f"{price} монет", True, price_color)
            surf.blit(pt, (rect.right - pt.get_width() - 15, rect.y + 14))

# ============ КОНСОЛЬ ============
def console_execute(cmd, player, world, mobs_list):
    global state, console_message, console_message_timer, victory_time
    cmd = cmd.strip()
    if not cmd: return

    if cmd == SECRET_WIN_CODE:
        player.add_item(DIAMOND, GOAL_DIAMONDS)
        player.add_item(COIN, GOAL_COINS)
        player.health = player.max_health
        player.hunger = player.max_hunger
        player.dead = False
        state = "victory"
        victory_time = 0
        console_message = ">>> ПОБЕДА АКТИВИРОВАНА <<<"
        console_message_timer = 180
        return

    if cmd == "heal":
        player.health = player.max_health
        player.hunger = player.max_hunger
        console_message = "Здоровье и голод восстановлены"
    elif cmd == "god":
        player.health = player.max_health
        player.hurt_cooldown = 999999
        console_message = "Бессмертие включено"
    elif cmd.startswith("give "):
        parts = cmd.split()
        try:
            amount = int(parts[1]) if len(parts) > 1 else 1
            player.add_item(COIN, amount)
            console_message = f"Выдано {amount} монет"
        except:
            console_message = "Синтаксис: give <число>"
    elif cmd == "diamond":
        player.add_item(DIAMOND, 1)
        console_message = "+1 алмаз"
    elif cmd == "killmobs":
        for m in mobs_list:
            if m.hostile and not m.dead:
                m.hp = 0
                m.dead = True
                m.death_anim = 0
        console_message = "Все враждебные мобы убиты"
    elif cmd == "help":
        console_message = "Команды: heal, god, give N, diamond, killmobs, clear"
    elif cmd == "clear":
        console_message = ""
    else:
        console_message = f"Неизвестная команда: {cmd}"

    console_message_timer = 150


def draw_console(surf, text, msg, msg_timer):
    bar_h = 40
    bar = pygame.Surface((SCREEN_W, bar_h), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 220))
    surf.blit(bar, (0, SCREEN_H - bar_h))
    pygame.draw.line(surf, (0, 255, 100), (0, SCREEN_H - bar_h), (SCREEN_W, SCREEN_H - bar_h), 2)

    prompt = font.render(">", True, (0, 255, 100))
    surf.blit(prompt, (15, SCREEN_H - bar_h + 10))

    cursor_blink = "_" if (pygame.time.get_ticks() // 400) % 2 == 0 else " "
    txt = font.render(text + cursor_blink, True, (200, 255, 200))
    surf.blit(txt, (40, SCREEN_H - bar_h + 10))

    head = font_small.render("DEV CONSOLE — Web0f & germagen1737", True, (0, 200, 80))
    surf.blit(head, (SCREEN_W - head.get_width() - 12, SCREEN_H - bar_h - 18))

    if msg_timer > 0 and msg:
        alpha = min(255, msg_timer * 3)
        m = font.render(msg, True, (255, 255, 100))
        bg = pygame.Surface((m.get_width() + 20, m.get_height() + 10), pygame.SRCALPHA)
        bg.fill((0, 0, 0, min(200, alpha)))
        surf.blit(bg, (10, SCREEN_H - bar_h - 50))
        surf.blit(m, (20, SCREEN_H - bar_h - 45))

# ============ ГЛАВНЫЙ ЦИКЛ ============
state = "intro"
intro_time = 0
victory_time = 0
holding = {1: False, 3: False}
hold_timer = 0
time_of_day = 0.35
spawn_timer = 0
running = True
eat_flash = 0
shop = None
message = ""
message_timer = 0

console_active = False
console_text = ""
console_message = ""
console_message_timer = 0

def show_message(text, duration=180):
    global message, message_timer
    message = text
    message_timer = duration

def respawn_player():
    global mobs
    sy, _ = world.get_column_info(spawn_wx)
    player.x = spawn_wx * TILE_SIZE
    player.y = (sy - 3) * TILE_SIZE
    player.vx = player.vy = 0
    player.health = player.max_health
    player.hunger = player.max_hunger
    player.hunger_timer = 0
    player.regen_timer = 0
    player.starve_timer = 0
    player.dead = False
    player.death_reason = ""
    player.hurt_cooldown = 0
    player.drowning_timer = 0
    player.fall_start_y = player.y
    mobs = [m for m in mobs if not m.hostile or
            math.hypot(m.x - player.x, m.y - player.y) > 15 * TILE_SIZE]

def check_victory():
    return (player.count_item(DIAMOND) >= GOAL_DIAMONDS and
            player.count_item(COIN) >= GOAL_COINS)

while running:
    dt = clock.tick(FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()

    # ============ ИНТРО ============
    if state == "intro":
        intro_time += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    state = "playing"
                    stats.start_time = time.time()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                state = "playing"
                stats.start_time = time.time()
        draw_intro(screen, intro_time)
        pygame.display.flip()
        continue

    # ============ ПОБЕДА ============
    if state == "victory":
        victory_time += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        draw_victory(screen, victory_time, player)
        pygame.display.flip()
        continue

    # ============ ИГРА ============
    time_of_day = (time_of_day + dt / DAY_LENGTH) % 1.0
    brightness = (math.cos((time_of_day - 0.5) * 2 * math.pi) + 1) / 2
    is_night = brightness < 0.4

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        # ============ КОНСОЛЬ ============
        if event.type == pygame.KEYDOWN and event.key == CONSOLE_TOGGLE_KEY:
            if state in ("playing", "shop"):
                console_active = not console_active
                console_text = ""
                if state == "shop" and console_active:
                    state = "playing"
                    shop = None
            continue

        if console_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    console_execute(console_text, player, world, mobs)
                    console_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    console_text = console_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    console_active = False
                    console_text = ""
                else:
                    ch = event.unicode
                    if ch and ch.isprintable() and len(console_text) < 100:
                        console_text += ch
            continue
        # ==================================

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if state == "shop":
                    state = "playing"; shop = None
                else:
                    running = False
            elif event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            elif state == "playing":
                if event.key == pygame.K_r and player.dead:
                    respawn_player()
                elif event.key == pygame.K_e and not player.dead:
                    px, py = player.x + player.w/2, player.y + player.h/2
                    opened = False
                    for dx in range(-3, 4):
                        for dy in range(-3, 4):
                            tx = int(px // TILE_SIZE) + dx
                            ty = int(py // TILE_SIZE) + dy
                            if world.get_block(tx, ty) == STALL:
                                shop = ShopUI(world, (tx, ty))
                                state = "shop"
                                opened = True; break
                        if opened: break
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    idx = event.key - pygame.K_1
                    if idx < len(player.hotbar):
                        player.selected_slot = idx
                elif event.key == pygame.K_0 and len(player.hotbar) >= 10:
                    player.selected_slot = 9
        elif event.type == pygame.MOUSEWHEEL and state == "playing":
            if player.hotbar:
                player.selected_slot = (player.selected_slot - event.y) % len(player.hotbar)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == "playing":
                if event.button in (1, 3):
                    holding[event.button] = True
                    hold_timer = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in (1, 3):
                holding[event.button] = False

        if state == "shop" and shop:
            res = shop.handle_event(event, player)
            if res == "close":
                state = "playing"; shop = None

    if state == "playing":
        keys = pygame.key.get_pressed()
        player.update(keys, world)

    cam_x = player.x + player.w / 2 - SCREEN_W / 2
    cam_y = player.y + player.h / 2 - SCREEN_H / 2
    world.physics_tick(cam_x, cam_y)

    spawn_timer += 1
    if spawn_timer >= SPAWN_INTERVAL and len(mobs) < MOB_SPAWN_CAP and not player.dead and state == "playing":
        spawn_timer = 0
        for _ in range(random.randint(1, 2)):
            m = spawn_mob_near_player(world, player, is_night)
            if m: mobs.append(m)

    for m in mobs:
        m.update(world, player)

    for m in mobs:
        if m.dead and not m.dropped and m.killed_by_player:
            m.dropped = True
            dist = math.hypot((m.x + m.w/2) - (player.x + player.w/2),
                              (m.y + m.h/2) - (player.y + player.h/2))
            if dist < 8 * TILE_SIZE:
                for item_id, (mn, mx) in MOB_TYPES[m.type]['drops']:
                    cnt = random.randint(mn, mx)
                    if cnt > 0:
                        player.add_item(item_id, cnt)
                        if item_id == COIN:
                            stats.coins_earned += cnt

    mobs = [m for m in mobs if not (m.dead and m.death_anim > 15)]
    mobs = [m for m in mobs if math.hypot(m.x - player.x, m.y - player.y) < 40 * TILE_SIZE]

    tx = int((mouse_pos[0] + cam_x) // TILE_SIZE)
    ty = int((mouse_pos[1] + cam_y) // TILE_SIZE)
    pcx = player.x + player.w / 2; pcy = player.y + player.h / 2
    bcx = tx * TILE_SIZE + TILE_SIZE / 2; bcy = ty * TILE_SIZE + TILE_SIZE / 2
    in_reach = (pcx - bcx) ** 2 + (pcy - bcy) ** 2 <= REACH ** 2

    current_item = None
    if 0 <= player.selected_slot < len(player.hotbar):
        current_item = player.hotbar[player.selected_slot]

    if state == "playing" and not player.dead and not console_active:
        if holding[1] and player.attack_cooldown == 0:
            click_wx = mouse_pos[0] + cam_x
            click_wy = mouse_pos[1] + cam_y
            for m in mobs:
                if m.dead: continue
                if m.x <= click_wx <= m.x + m.w and m.y <= click_wy <= m.y + m.h:
                    dist = math.hypot(pcx - (m.x + m.w / 2), pcy - (m.y + m.h / 2))
                    if dist < REACH:
                        dmg = player.get_attack_damage(current_item)
                        m.take_damage(dmg, pcx, by_player=True)
                        player.attack_cooldown = 12
                        break

        if in_reach and current_item is not None:
            item_type = ITEM_INFO[current_item]["type"]
            if holding[1] and hold_timer <= 0:
                b = world.get_block(tx, ty)
                if BLOCK_INFO[b]["breakable"]:
                    if b == LEAVES and random.random() < 0.08:
                        player.add_item(APPLE, 1)
                        show_message("+1 Яблоко!", 90)
                    if b == DIAMOND_ORE:
                        player.add_item(DIAMOND, 1)
                        stats.diamonds_mined += 1
                        show_message("+1 Алмаз!", 120)
                    world.set_block(tx, ty, AIR)
                    stats.blocks_mined += 1
                    speed = player.get_mining_speed(current_item)
                    hold_timer = max(1, speed)
            if holding[3] and hold_timer <= 0:
                b = world.get_block(tx, ty)
                if b == CHEST:
                    pos = (tx, ty)
                    if pos in world.chest_loot:
                        loot = world.chest_loot.pop(pos)
                        msgs = []
                        for item_id, cnt in loot:
                            player.add_item(item_id, cnt)
                            if item_id == COIN:
                                stats.coins_earned += cnt
                            msgs.append(f"{cnt}x{ITEM_INFO[item_id]['name']}")
                        show_message("Сундук: " + ", ".join(msgs), 180)
                        world.set_block(tx, ty, AIR)
                    hold_timer = 20
                elif b == STALL:
                    shop = ShopUI(world, (tx, ty))
                    state = "shop"
                    hold_timer = 20
                elif item_type == "food":
                    if player.eat(current_item):
                        eat_flash = 20
                    hold_timer = 20
                elif item_type == "block":
                    if b in (AIR, WATER):
                        new_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        blocked_by_mob = any(new_rect.colliderect(m.rect()) for m in mobs if not m.dead)
                        if not new_rect.colliderect(player.rect()) and not blocked_by_mob:
                            world.set_block(tx, ty, current_item)
                            hold_timer = 5

    if hold_timer > 0: hold_timer -= 1
    if eat_flash > 0: eat_flash -= 1
    if message_timer > 0: message_timer -= 1
    if console_message_timer > 0: console_message_timer -= 1

    sky_col, _ = get_sky_color(time_of_day)
    screen.fill(sky_col)
    draw_sun_moon(screen, time_of_day)
    draw_clouds(screen, cam_x, cam_y)
    draw_world(screen, world, cam_x, cam_y, time_of_day)

    if in_reach:
        cur = world.get_block(tx, ty)
        if cur == CHEST:
            col = (240, 200, 60)
        elif cur == STALL:
            col = (100, 255, 100)
        elif current_item is not None and ITEM_INFO[current_item]["type"] == "food":
            col = (100, 255, 100)
        else:
            col = (255, 80, 80) if cur != AIR and BLOCK_INFO[cur]["breakable"] else (255, 255, 255)
        pygame.draw.rect(screen, col, (tx*TILE_SIZE-cam_x, ty*TILE_SIZE-cam_y, TILE_SIZE, TILE_SIZE), 2)
    else:
        pygame.draw.rect(screen, (140, 140, 140),
                         (tx*TILE_SIZE-cam_x, ty*TILE_SIZE-cam_y, TILE_SIZE, TILE_SIZE), 1)

    for m in mobs:
        m.draw(screen, cam_x, cam_y)

    player.draw(screen, cam_x, cam_y)

    if player.in_water and not player.dead:
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((40, 80, 200, 60))
        screen.blit(ov, (0, 0))

    if eat_flash > 0:
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        a = int(80 * (eat_flash / 20))
        ov.fill((255, 230, 100, a))
        screen.blit(ov, (0, 0))

    draw_hunger_bar(screen, player)
    hearts = player.max_health // 2
    for i in range(hearts):
        hx = 12 + i * 22
        hp_remaining = player.health - i * 2
        draw_heart(screen, hx, SCREEN_H - 40, (60, 20, 20))
        if hp_remaining >= 2:
            draw_heart(screen, hx, SCREEN_H - 40, (220, 40, 40))
        elif hp_remaining == 1:
            draw_heart_half(screen, hx, SCREEN_H - 40, (220, 40, 40))

    draw_hotbar(screen, player)
    _, biome = world.get_column_info(int(player.x // TILE_SIZE))
    draw_ui(screen, player, world, clock.get_fps(), biome, time_of_day)
    draw_quest(screen, player)

    if message_timer > 0:
        alpha = min(255, message_timer * 5)
        msg_t = font_med.render(message, True, (255, 255, 200))
        bg = pygame.Surface((msg_t.get_width() + 30, msg_t.get_height() + 16), pygame.SRCALPHA)
        bg.fill((0, 0, 0, min(180, alpha)))
        mx = SCREEN_W // 2 - bg.get_width() // 2
        my = 120
        screen.blit(bg, (mx, my))
        screen.blit(msg_t, (mx + 15, my + 8))

    if state == "shop" and shop:
        shop.draw(screen, player)

    if player.dead:
        draw_death_screen(screen, player)

    if check_victory() and state == "playing" and not player.dead:
        state = "victory"
        victory_time = 0

    if console_active:
        draw_console(screen, console_text, console_message, console_message_timer)

    pygame.display.flip()

pygame.quit()
sys.exit()