import pygame
import random
import sys

# инициализация
pygame.init()

# цвета
rozoviy_fon = (255, 230, 240)
yarko_rozoviy = (255, 20, 147)
rozoviy_platforma = (230, 180, 200)
goluboy = (180, 220, 240)
fionetoviy = (160, 100, 160)
zolotoy = (255, 215, 0)
krasnyy = (240, 80, 80)
belyy = (255, 255, 255)
chernyy = (30, 30, 30)
temno_rozoviy = (200, 100, 150)
siniy = (100, 150, 255)
oranzhevyy = (255, 180, 100)

# размеры экрана
shirina = 800
visota = 600
fps = 60

# физика
gravitaciya = 0.5
sila_pryzhka = -14
skorost = 6

# уровни
urovni = [
    {
        'platformy': [
            (0, 560, 800, "normal"),
            (200, 500, 150, "normal"),
            (400, 400, 150, "oblako"),
            (100, 300, 120, "normal"),
            (500, 250, 180, "oblako"),
            (300, 150, 100, "normal"),
            (600, 100, 120, "normal"),
            (50, 200, 100, "oblako"),
        ],
        'monetki': [
            (250, 470), (450, 370), (150, 270), (550, 220),
            (350, 120), (650, 70), (100, 170), (700, 270),
        ],
        'vragi': [
            (300, 470), (500, 370), (200, 250)
        ],
        'tip': 'normal'
    },
    {
        'platformy': [
            (0, 560, 800, "normal"),
            (150, 500, 120, "normal"),
            (450, 450, 120, "oblako"),
            (100, 380, 100, "normal"),
            (550, 350, 150, "normal"),
            (200, 280, 100, "oblako"),
            (400, 200, 150, "normal"),
            (600, 150, 120, "normal"),
            (50, 100, 100, "oblako"),
            (300, 50, 150, "normal"),
        ],
        'monetki': [
            (200, 470), (500, 420), (150, 350), (600, 320),
            (250, 250), (450, 170), (650, 120), (100, 70),
            (350, 20),
        ],
        'vragi': [
            (300, 470), (500, 420), (200, 250), (400, 150)
        ],
        'tip': 'normal'
    },
    {
        'platformy': [
            (0, 560, 800, "normal"),
            (100, 500, 100, "normal"),
            (300, 500, 100, "normal"),
            (500, 500, 100, "normal"),
            (200, 400, 150, "oblako"),
            (450, 400, 150, "oblako"),
            (100, 300, 120, "normal"),
            (350, 300, 120, "normal"),
            (600, 300, 120, "normal"),
            (50, 200, 100, "oblako"),
            (250, 200, 100, "oblako"),
            (450, 200, 100, "oblako"),
            (650, 200, 100, "normal"),
            (150, 100, 120, "normal"),
            (400, 100, 120, "normal"),
            (550, 100, 120, "normal"),
        ],
        'monetki': [
            (150, 470), (350, 470), (550, 470), (250, 370),
            (500, 370), (150, 270), (400, 270), (650, 270),
            (100, 170), (300, 170), (500, 170), (700, 170),
            (200, 70), (450, 70), (600, 70),
        ],
        'vragi': [
            (200, 470), (400, 470), (600, 470), (300, 370),
            (500, 270), (250, 170), (450, 70)
        ],
        'tip': 'normal'
    },
    {
        'platformy': [
            (0, 560, 800, "normal"),
            (200, 450, 150, "normal"),
            (500, 350, 150, "normal"),
            (100, 250, 150, "normal"),
            (400, 150, 150, "normal"),
            (600, 50, 150, "normal"),
        ],
        'monetki': [
            (250, 420), (550, 320), (150, 220), (450, 120), (650, 20),
        ],
        'vragi': [
            (250, 450), (550, 450),
            (350, 350), (150, 250), (450, 250),
            (250, 150), (550, 150),
        ],
        'tip': 'zvezdy'
    },
    {
        'platformy': [
            (0, 560, 800, "normal"),
            (150, 450, 120, "normal"),
            (350, 350, 150, "normal"),
            (550, 250, 150, "normal"),
            (250, 150, 150, "normal"),
            (450, 50, 150, "normal"),
        ],
        'monetki': [
            (200, 420), (400, 320), (600, 220), (300, 120), (500, 20),
            (100, 470), (700, 470),
        ],
        'vragi': [
            (100, 450), (300, 450), (500, 450), (700, 450),
            (200, 350), (400, 350), (600, 350),
            (300, 250), (500, 250),
            (200, 150), (400, 150), (600, 150),
            (300, 50), (500, 50),
        ],
        'tip': 'kapelki'
    }
]
# класс героя
class kotik:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.speed_x = 0
        self.speed_y = 0
        self.on_ground = False
        self.can_double_jump = True
        self.jumps_made = 0
        self.max_jumps = 2
        self.jump_key_was_pressed = False
        self.looking_right = True
        self.invulnerable = False
        self.invulnerable_time = 0
        self.coins = 0
        self.lives = 3
        self.victory = False

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -skorost
            self.looking_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = skorost
            self.looking_right = True
        else:
            self.speed_x = 0

        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]

        if jump_pressed:
            if not self.jump_key_was_pressed:
                if self.on_ground:
                    self.speed_y = sila_pryzhka
                    self.on_ground = False
                    self.jumps_made = 1
                elif self.can_double_jump and self.jumps_made == 1:
                    self.speed_y = sila_pryzhka * 0.9
                    self.jumps_made = 2
            self.jump_key_was_pressed = True
        else:
            self.jump_key_was_pressed = False

        self.speed_y += gravitaciya
        self.y += self.speed_y
        self.x += self.speed_x

        if self.x < self.radius:
            self.x = self.radius
        if self.x > shirina - self.radius:
            self.x = shirina - self.radius

        if self.y > visota + 50:
            self.lives -= 1
            self.x = shirina // 2
            self.y = 100
            self.speed_y = 0
            self.invulnerable = True
            self.invulnerable_time = 120

    def update_invulnerable(self):
        if self.invulnerable:
            self.invulnerable_time -= 1
            if self.invulnerable_time <= 0:
                self.invulnerable = False

    def draw(self, screen):
        if self.invulnerable and self.invulnerable_time % 10 < 5:
            color = zolotoy
        else:
            color = yarko_rozoviy

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, chernyy, (int(self.x), int(self.y)), self.radius, 2)

        if self.looking_right:
            pygame.draw.polygon(screen, temno_rozoviy, [
                (self.x + 10, self.y - 18),
                (self.x + 22, self.y - 30),
                (self.x + 18, self.y - 15)
            ])
            pygame.draw.polygon(screen, temno_rozoviy, [
                (self.x - 10, self.y - 18),
                (self.x - 22, self.y - 30),
                (self.x - 18, self.y - 15)
            ])
        else:
            pygame.draw.polygon(screen, temno_rozoviy, [
                (self.x + 8, self.y - 18),
                (self.x + 20, self.y - 30),
                (self.x + 16, self.y - 15)
            ])
            pygame.draw.polygon(screen, temno_rozoviy, [
                (self.x - 12, self.y - 18),
                (self.x - 24, self.y - 30),
                (self.x - 20, self.y - 15)
            ])

        if self.looking_right:
            pygame.draw.circle(screen, belyy, (int(self.x + 8), int(self.y - 4)), 6)
            pygame.draw.circle(screen, chernyy, (int(self.x + 10), int(self.y - 4)), 3)
            pygame.draw.circle(screen, belyy, (int(self.x - 8), int(self.y - 4)), 6)
            pygame.draw.circle(screen, chernyy, (int(self.x - 6), int(self.y - 4)), 3)
        else:
            pygame.draw.circle(screen, belyy, (int(self.x + 8), int(self.y - 4)), 6)
            pygame.draw.circle(screen, chernyy, (int(self.x + 6), int(self.y - 4)), 3)
            pygame.draw.circle(screen, belyy, (int(self.x - 8), int(self.y - 4)), 6)
            pygame.draw.circle(screen, chernyy, (int(self.x - 10), int(self.y - 4)), 3)

        if self.speed_y < 0:
            pygame.draw.arc(screen, krasnyy, [self.x - 8, self.y + 2, 16, 10], 3.14, 0, 2)
        else:
            pygame.draw.arc(screen, krasnyy, [self.x - 8, self.y - 2, 16, 10], 0, 3.14, 2)


# класс платформы
class platforma:
    def __init__(self, x, y, width, tip="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        self.tip = tip
        self.active = True
        self.life_time = 90
        self.cat_on_cloud = False

    def update(self, cat):
        if self.tip == "oblako" and self.active:
            if (cat.x + cat.radius > self.x and
                    cat.x - cat.radius < self.x + self.width and
                    abs(cat.y + cat.radius - self.y) < 10 and
                    cat.speed_y >= 0):

                if not self.cat_on_cloud:
                    self.cat_on_cloud = True

                self.life_time -= 1
                if self.life_time <= 0:
                    self.active = False
            else:
                self.cat_on_cloud = False

    def check_collision(self, cat):
        if not self.active:
            return False

        if (cat.x + cat.radius > self.x and
                cat.x - cat.radius < self.x + self.width and
                cat.y + cat.radius <= self.y + 10 and
                cat.y + cat.radius + cat.speed_y >= self.y):
            cat.y = self.y - cat.radius
            cat.speed_y = 0
            cat.on_ground = True
            cat.jumps_made = 0
            return True
        return False

    def draw(self, screen):
        if not self.active:
            return

        if self.tip == "normal":
            color = rozoviy_platforma
        else:
            if self.life_time < 30:
                color = (255, 200, 200)
            elif self.life_time < 60:
                color = (200, 220, 250)
            else:
                color = goluboy

        pygame.draw.rect(screen, color,
                         (self.x, self.y, self.width, self.height),
                         border_radius=5)
        pygame.draw.rect(screen, chernyy,
                         (self.x, self.y, self.width, self.height), 1,
                         border_radius=5)


# класс монетки
class coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8
        self.collected = False
        self.angle = 0

    def check_collection(self, cat):
        if self.collected:
            return False

        dist = ((cat.x - self.x) ** 2 + (cat.y - self.y) ** 2) ** 0.5
        if dist < cat.radius + self.radius:
            self.collected = True
            cat.coins += 1
            return True
        return False

    def draw(self, screen):
        if self.collected:
            return

        self.angle += 5
        pygame.draw.circle(screen, zolotoy, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, belyy, (self.x, self.y), self.radius, 2)

        if self.angle % 30 < 15:
            pygame.draw.circle(screen, belyy, (self.x - 2, self.y - 2), 2)


# класс врага
class enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 25
        self.speed_x = random.choice([-2, -1, 1, 2])
        self.speed_y = random.choice([-1, 1]) if random.random() < 0.3 else 0
        self.active = True

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < 0 or self.x > shirina - self.width:
            self.speed_x *= -1
        if self.y < 50 or self.y > 550 - self.height:
            self.speed_y *= -1

    def check_collision(self, cat):
        if not self.active or cat.invulnerable:
            return False

        dist_x = abs(cat.x - (self.x + self.width // 2))
        dist_y = abs(cat.y - (self.y + self.height // 2))

        if dist_x < cat.radius + self.width // 2 and dist_y < cat.radius + self.height // 2:

            if cat.speed_y > 0 and cat.y + cat.radius < self.y + 10:
                self.active = False
                cat.speed_y = sila_pryzhka * 0.7
                return "killed"
            else:
                cat.lives -= 1
                cat.x = shirina // 2
                cat.y = 100
                cat.invulnerable = True
                cat.invulnerable_time = 120
                return "hurt"
        return False

    def draw(self, screen):
        if not self.active:
            return

        pygame.draw.ellipse(screen, fionetoviy,
                            (self.x, self.y, self.width, self.height))
        pygame.draw.circle(screen, chernyy, (int(self.x + 8), int(self.y + 8)), 3)
        pygame.draw.circle(screen, chernyy, (int(self.x + 22), int(self.y + 8)), 3)
        pygame.draw.circle(screen, krasnyy, (int(self.x + 7), int(self.y + 7)), 1)
        pygame.draw.circle(screen, krasnyy, (int(self.x + 21), int(self.y + 7)), 1)


# класс звезды
class star:
    def __init__(self):
        self.x = random.randint(20, shirina - 20)
        self.y = random.randint(-100, -20)
        self.radius = 8
        self.speed = random.randint(3, 6)
        self.active = True

    def update(self):
        self.y += self.speed
        if self.y > visota + 20:
            self.active = False

    def check_collection(self, cat):
        if not self.active:
            return False

        dist = ((cat.x - self.x) ** 2 + (cat.y - self.y) ** 2) ** 0.5
        if dist < cat.radius + self.radius:
            self.active = False
            cat.coins += 1
            return True
        return False

    def draw(self, screen):
        if not self.active:
            return

        pygame.draw.circle(screen, oranzhevyy, (self.x, self.y), self.radius)
        for i in range(4):
            angle = i * 3.14 / 2
            x2 = self.x + (self.radius + 4) * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            y2 = self.y + (self.radius + 4) * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            pygame.draw.line(screen, zolotoy, (self.x, self.y), (x2, y2), 2)


# класс капельки
class drop:
    def __init__(self):
        self.x = random.randint(20, shirina - 20)
        self.y = random.randint(-100, -20)
        self.radius = 8
        self.speed = random.randint(4, 7)
        self.active = True

    def update(self):
        self.y += self.speed
        if self.y > visota + 20:
            self.active = False

    def check_collision(self, cat):
        if not self.active or cat.invulnerable:
            return False

        dist = ((cat.x - self.x) ** 2 + (cat.y - self.y) ** 2) ** 0.5
        if dist < cat.radius + self.radius:
            self.active = False
            cat.lives -= 1
            cat.invulnerable = True
            cat.invulnerable_time = 120
            return True
        return False

    def draw(self, screen):
        if not self.active:
            return

        pygame.draw.circle(screen, siniy, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, belyy, (self.x - 2, self.y - 2), 2)


# класс игры
class game:
    def __init__(self):
        self.screen = pygame.display.set_mode((shirina, visota))
        pygame.display.set_caption("game 1")
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        self.start_game()

    def start_game(self):
        self.cat = kotik(shirina // 2, 500)
        self.level = 0
        self.coins_needed = 5
        self.falling_objects = []
        self.create_time = 0
        self.load_level()

    def load_level(self):
        if self.level >= len(urovni):
            self.cat.victory = True
            return

        level_data = urovni[self.level]

        self.platforms = []
        for x, y, w, tip in level_data['platformy']:
            self.platforms.append(platforma(x, y, w, tip))

        self.coins = []
        for x, y in level_data['monetki']:
            self.coins.append(coin(x, y))

        self.enemies = []
        for x, y in level_data['vragi']:
            self.enemies.append(enemy(x, y))

        self.cat.coins = 0
        self.coins_needed = 5 + self.level * 2
        self.level_type = level_data.get('tip', 'normal')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r and (self.cat.lives <= 0 or self.cat.victory):
                    self.start_game()
        return True

    def update(self):
        keys = pygame.key.get_pressed()

        self.cat.move(keys)
        self.cat.update_invulnerable()

        self.cat.on_ground = False
        for platform in self.platforms:
            platform.update(self.cat)
            platform.check_collision(self.cat)

        for coin in self.coins:
            coin.check_collection(self.cat)

        for enemy in self.enemies:
            enemy.move()
            enemy.check_collision(self.cat)

        self.enemies = [e for e in self.enemies if e.active]
        self.platforms = [p for p in self.platforms if p.active]

        for obj in self.falling_objects:
            obj.update()

            if self.level_type == 'zvezdy' and hasattr(obj, 'check_collection'):
                obj.check_collection(self.cat)
            elif self.level_type == 'kapelki' and hasattr(obj, 'check_collision'):
                obj.check_collision(self.cat)

        self.falling_objects = [obj for obj in self.falling_objects if obj.active]

        if self.level_type in ['zvezdy', 'kapelki']:
            self.create_time += 1
            if self.create_time > random.randint(15, 30):
                if self.level_type == 'zvezdy':
                    self.falling_objects.append(star())
                else:
                    self.falling_objects.append(drop())
                self.create_time = 0

        all_coins_collected = all(c.collected for c in self.coins)
        if all_coins_collected or self.cat.coins >= self.coins_needed:
            self.level += 1
            if self.level < len(urovni):
                self.load_level()
            else:
                self.cat.victory = True

    def draw(self):
        self.screen.fill(rozoviy_fon)

        for platform in self.platforms:
            platform.draw(self.screen)

        for coin in self.coins:
            coin.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for obj in self.falling_objects:
            obj.draw(self.screen)

        self.cat.draw(self.screen)

        level_name = f"level: {self.level + 1}"
        if self.level_type == 'zvezdy':
            level_name += " *"
        elif self.level_type == 'kapelki':
            level_name += " v"

        text_level = self.font_small.render(level_name, True, fionetoviy)
        self.screen.blit(text_level, (shirina // 2 - 40, 10))

        text_coins = self.font_small.render(f"coins: {self.cat.coins}/{self.coins_needed}", True, zolotoy)
        self.screen.blit(text_coins, (shirina - 140, 10))

        text_lives = self.font_small.render(f"lives: {self.cat.lives}", True, krasnyy)
        self.screen.blit(text_lives, (20, 10))

        if self.cat.victory:
            s = pygame.Surface((shirina, visota))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            self.screen.blit(s, (0, 0))

            t1 = self.font_big.render("Победа!", True, zolotoy)
            t2 = self.font_small.render("r - restart", True, belyy)

            r1 = t1.get_rect(center=(shirina // 2, visota // 2 - 30))
            r2 = t2.get_rect(center=(shirina // 2, visota // 2 + 30))

            self.screen.blit(t1, r1)
            self.screen.blit(t2, r2)

        elif self.cat.lives <= 0:
            s = pygame.Surface((shirina, visota))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            self.screen.blit(s, (0, 0))

            t1 = self.font_big.render("game over", True, krasnyy)
            t2 = self.font_small.render("r - restart", True, belyy)

            r1 = t1.get_rect(center=(shirina // 2, visota // 2 - 30))
            r2 = t2.get_rect(center=(shirina // 2, visota // 2 + 30))

            self.screen.blit(t1, r1)
            self.screen.blit(t2, r2)

    def run(self):
        running = True
        while running:
            running = self.handle_events()

            if self.cat.lives > 0 and not self.cat.victory:
                self.update()

            self.draw()
            pygame.display.flip()
            self.clock.tick(fps)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game_obj = game()
    game_obj.run()