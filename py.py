import pygame  # библиотека для создания игр
import random  # библиотека для случайных чисел
import sys     # библиотека для выхода из программы

pygame.init()  # инициализация pygame (запуск всех модулей)

# цвета в формате rgb (красный, зеленый, синий) от 0 до 255
rozoviy_fon = (255, 230, 240)      # нежно-розовый для фона
yarko_rozoviy = (255, 20, 147)      # ярко-розовый для шарика
rozoviy_platforma = (230, 180, 200) # розовый для платформ
goluboy = (180, 220, 240)           # голубой для облаков
fionetoviy = (160, 100, 160)        # фиолетовый для врагов
zolotoy = (255, 215, 0)             # золотой для монет
krasnyy = (240, 80, 80)             # красный для опасности
belyy = (255, 255, 255)             # белый
chernyy = (30, 30, 30)              # черный
temno_rozoviy = (200, 100, 150)     # темно-розовый для ушек
siniy = (100, 150, 255)             # синий для капелек
oranzhevyy = (255, 180, 100)        # оранжевый для звездочек

shirina = 800   # ширина игрового окна в пикселях
visota = 600    # высота игрового окна в пикселях
fps = 60        # количество кадров в секунду (чем больше, тем плавнее)

gravitaciya = 0.5   # сила гравитации (скорость падения увеличивается на эту величину каждый кадр)
sila_pryzhka = -14  # сила прыжка (отрицательная, потому что прыгаем вверх)
skorost = 6         # скорость движения влево-вправо

# список уровней (каждый уровень - это словарь с платформами, монетками, врагами и типом)
urovni = [
    {   # уровень 1
        'platformy': [   # список платформ (каждая: x, y, ширина, тип)
            (0, 560, 800, "normal"),   # пол внизу
            (200, 500, 150, "normal"), # платформа
            (400, 400, 150, "oblako"), # облако
            (100, 300, 120, "normal"),
            (500, 250, 180, "oblako"),
            (300, 150, 100, "normal"),
            (600, 100, 120, "normal"),
            (50, 200, 100, "oblako"),
        ],
        'monetki': [   # список монеток (каждая: x, y)
            (250, 470), (450, 370), (150, 270), (550, 220),
            (350, 120), (650, 70), (100, 170), (700, 270),
        ],
        'vragi': [     # список врагов (каждый: x, y)
            (300, 470), (500, 370), (200, 250)
        ],
        'tip': 'normal'   # тип уровня (normal - обычный)
    },
    {   # уровень 2
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
    {   # уровень 3
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
    {   # уровень 4 - падают звездочки
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
        'tip': 'zvezdy'   # тип уровня - звездочки (падают с неба, дают монетки)
    },
    {   # уровень 5 - падают капельки
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
        'tip': 'kapelki'   # тип уровня - капельки (падают с неба, отнимают жизни)
    }
]

# класс героя
class kotik:
    def __init__(self, x, y):   # конструктор, вызывается при создании героя
        self.x = x              # координата x
        self.y = y              # координата y
        self.radius = 20        # радиус шарика (размер)
        self.speed_x = 0        # скорость по горизонтали
        self.speed_y = 0        # скорость по вертикали
        self.on_ground = False  # находится ли на земле (платформе)
        self.can_double_jump = True  # разрешен ли двойной прыжок
        self.jumps_made = 0     # сколько прыжков уже сделано
        self.max_jumps = 2      # максимальное количество прыжков (2 = двойной)
        self.jump_key_was_pressed = False  # флаг, чтобы прыжок не повторялся каждый кадр
        self.looking_right = True   # смотрит ли вправо (для отрисовки)
        self.invulnerable = False   # неуязвим ли после получения урона
        self.invulnerable_time = 0  # сколько кадров осталось неуязвимости
        self.coins = 0          # количество собранных монеток
        self.lives = 3          # количество жизней
        self.victory = False    # победил ли (прошел все уровни)

    def move(self, keys):   # метод движения, принимает список нажатых клавиш
        # движение влево-вправо
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:   # если нажата левая стрелка или клавиша A
            self.speed_x = -skorost   # скорость отрицательная (движение влево)
            self.looking_right = False   # смотрит влево
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:   # если нажата правая стрелка или клавиша D
            self.speed_x = skorost    # скорость положительная (движение вправо)
            self.looking_right = True   # смотрит вправо
        else:   # если ничего не нажато
            self.speed_x = 0          # стоим на месте
        # прыжок
        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]  # пробел, стрелка вверх или W
        if jump_pressed:   # если клавиша прыжка нажата
            if not self.jump_key_was_pressed:   # если в прошлый кадр она не была нажата (только что нажали)
                if self.on_ground:   # если стоим на земле
                    self.speed_y = sila_pryzhka   # задаем скорость прыжка (вверх)
                    self.on_ground = False        # больше не на земле
                    self.jumps_made = 1           # сделали 1 прыжок
                elif self.can_double_jump and self.jumps_made == 1:   # если можно двойной прыжок и сделали 1 прыжок
                    self.speed_y = sila_pryzhka * 0.9   # второй прыжок слабее
                    self.jumps_made = 2                 # сделали 2 прыжка
            self.jump_key_was_pressed = True   # запоминаем что клавиша нажата
        else:   # если клавиша не нажата
            self.jump_key_was_pressed = False   # сбрасываем флаг
        # гравитация
        self.speed_y += gravitaciya   # скорость по Y увеличивается на силу гравитации (падаем)
        self.y += self.speed_y        # изменяем координату Y на скорость
        self.x += self.speed_x        # изменяем координату X на скорость
        # границы экрана по горизонтали
        if self.x < self.radius:      # если вышли за левый край
            self.x = self.radius      # прижимаем к левому краю
        if self.x > shirina - self.radius:   # если вышли за правый край
            self.x = shirina - self.radius   # прижимаем к правому краю
        # падение вниз (за пределы экрана)
        if self.y > visota + 50:      # если упали ниже экрана
            self.lives -= 1           # теряем одну жизнь
            self.x = shirina // 2     # появляемся в центре по горизонтали
            self.y = 100              # появляемся наверху
            self.speed_y = 0          # обнуляем скорость падения
            self.invulnerable = True  # включаем неуязвимость
            self.invulnerable_time = 120  # на 120 кадров (2 секунды при 60 fps)

    def update_invulnerable(self):   # метод обновления неуязвимости
        if self.invulnerable:        # если неуязвим
            self.invulnerable_time -= 1   # уменьшаем таймер на 1
            if self.invulnerable_time <= 0:   # если таймер закончился
                self.invulnerable = False     # выключаем неуязвимость

    def draw(self, screen):   # метод рисования героя, принимает экран
        # выбор цвета (мигание если неуязвим)
        if self.invulnerable and self.invulnerable_time % 10 < 5:   # если неуязвим и таймер делится
            color = zolotoy   # золотой цвет (мигает)
        else:
            color = yarko_rozoviy   # ярко-розовый цвет
        # рисуем шарик
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)   # круг
        pygame.draw.circle(screen, chernyy, (int(self.x), int(self.y)), self.radius, 2)   # обводка
        # рисуем ушки (треугольники)
        if self.looking_right:   # если смотрит вправо
            pygame.draw.polygon(screen, temno_rozoviy, [   # правое ушко
                (self.x + 10, self.y - 18),
                (self.x + 22, self.y - 30),
                (self.x + 18, self.y - 15)
            ])
            pygame.draw.polygon(screen, temno_rozoviy, [   # левое ушко
                (self.x - 10, self.y - 18),
                (self.x - 22, self.y - 30),
                (self.x - 18, self.y - 15)
            ])
        else:   # если смотрит влево
            pygame.draw.polygon(screen, temno_rozoviy, [   # правое ушко
                (self.x + 8, self.y - 18),
                (self.x + 20, self.y - 30),
                (self.x + 16, self.y - 15)
            ])
            pygame.draw.polygon(screen, temno_rozoviy, [   # левое ушко
                (self.x - 12, self.y - 18),
                (self.x - 24, self.y - 30),
                (self.x - 20, self.y - 15)
            ])
        # рисуем глазки
        if self.looking_right:   # если смотрит вправо
            pygame.draw.circle(screen, belyy, (int(self.x + 8), int(self.y - 4)), 6)   # правый глаз белок
            pygame.draw.circle(screen, chernyy, (int(self.x + 10), int(self.y - 4)), 3)   # правый зрачок
            pygame.draw.circle(screen, belyy, (int(self.x - 8), int(self.y - 4)), 6)   # левый глаз белок
            pygame.draw.circle(screen, chernyy, (int(self.x - 6), int(self.y - 4)), 3)   # левый зрачок
        else:   # если смотрит влево
            pygame.draw.circle(screen, belyy, (int(self.x + 8), int(self.y - 4)), 6)   # правый глаз белок
            pygame.draw.circle(screen, chernyy, (int(self.x + 6), int(self.y - 4)), 3)   # правый зрачок
            pygame.draw.circle(screen, belyy, (int(self.x - 8), int(self.y - 4)), 6)   # левый глаз белок
            pygame.draw.circle(screen, chernyy, (int(self.x - 10), int(self.y - 4)), 3)   # левый зрачок
        # рисуем ротик (улыбка или грусть)
        if self.speed_y < 0:   # если летим вверх
            pygame.draw.arc(screen, krasnyy, [self.x - 8, self.y + 2, 16, 10], 3.14, 0, 2)   # улыбка вверх
        else:   # если на земле или падаем
            pygame.draw.arc(screen, krasnyy, [self.x - 8, self.y - 2, 16, 10], 0, 3.14, 2)   # улыбка вниз

# класс платформы
class platforma:
    def __init__(self, x, y, width, tip="normal"):   # конструктор
        self.x = x                # координата x
        self.y = y                # координата y
        self.width = width        # ширина платформы
        self.height = 20          # высота платформы
        self.tip = tip            # тип (normal - обычная, oblako - облако)
        self.active = True        # активна ли платформа (не исчезла)
        self.life_time = 90       # время жизни для облаков (90 кадров)
        self.cat_on_cloud = False # стоит ли котик на этом облаке

    def update(self, cat):   # обновление платформы
        if self.tip == "oblako" and self.active:   # если облако и оно активно
            # проверяем, стоит ли котик на облаке
            if (cat.x + cat.radius > self.x and   # правая граница котика правее левого края облака
                    cat.x - cat.radius < self.x + self.width and   # левая граница котика левее правого края
                    abs(cat.y + cat.radius - self.y) < 10 and   # расстояние по вертикали маленькое
                    cat.speed_y >= 0):   # котик падает или стоит (не летит вверх)
                if not self.cat_on_cloud:   # если только что встал
                    self.cat_on_cloud = True   # отмечаем
                self.life_time -= 1   # уменьшаем время жизни
                if self.life_time <= 0:   # если время жизни кончилось
                    self.active = False   # облако исчезает
            else:   # если котик не на облаке
                self.cat_on_cloud = False   # сбрасываем флаг

    def check_collision(self, cat):   # проверка столкновения котика с платформой
        if not self.active:   # если платформа не активна
            return False      # не столкнулись
        # проверяем, касается ли котик платформы сверху
        if (cat.x + cat.radius > self.x and   # правая граница котика правее левого края
                cat.x - cat.radius < self.x + self.width and   # левая граница левее правого края
                cat.y + cat.radius <= self.y + 10 and   # низ котика выше платформы (с запасом)
                cat.y + cat.radius + cat.speed_y >= self.y):   # с учетом скорости коснется
            cat.y = self.y - cat.radius   # ставим котика на платформу
            cat.speed_y = 0               # обнуляем скорость падения
            cat.on_ground = True          # котик на земле
            cat.jumps_made = 0            # сбрасываем счетчик прыжков
            return True   # столкновение было
        return False      # столкновения не было

    def draw(self, screen):   # рисование платформы
        if not self.active:   # если не активна
            return            # не рисуем
        # выбираем цвет в зависимости от типа и времени жизни
        if self.tip == "normal":   # если обычная платформа
            color = rozoviy_platforma   # розовый цвет
        else:   # если облако
            if self.life_time < 30:   # если осталось меньше 30 кадров
                color = (255, 200, 200)   # красноватый (скоро исчезнет)
            elif self.life_time < 60:   # если осталось меньше 60
                color = (200, 220, 250)   # светло-голубой (уже тает)
            else:   # иначе
                color = goluboy   # голубой
        # рисуем прямоугольник платформы
        pygame.draw.rect(screen, color,
                         (self.x, self.y, self.width, self.height),
                         border_radius=5)   # с закругленными углами
        # рисуем обводку
        pygame.draw.rect(screen, chernyy,
                         (self.x, self.y, self.width, self.height), 1,
                         border_radius=5)

# класс монетки
class coin:
    def __init__(self, x, y):   # конструктор
        self.x = x              # координата x
        self.y = y              # координата y
        self.radius = 8         # радиус монетки
        self.collected = False  # собрана ли монетка
        self.angle = 0          # угол для анимации вращения

    def check_collection(self, cat):   # проверка, собрал ли котик монетку
        if self.collected:   # если уже собрана
            return False     # не собираем
        # вычисляем расстояние между котиком и монеткой (теорема Пифагора)
        dist = ((cat.x - self.x) ** 2 + (cat.y - self.y) ** 2) ** 0.5
        if dist < cat.radius + self.radius:   # если расстояние меньше суммы радиусов (коснулись)
            self.collected = True   # отмечаем как собранную
            cat.coins += 1          # увеличиваем счет монеток у котика
            return True   # собрали
        return False      # не собрали

    def draw(self, screen):   # рисование монетки
        if self.collected:   # если собрана
            return           # не рисуем
        self.angle += 5      # увеличиваем угол для анимации вращения
        # рисуем золотой круг
        pygame.draw.circle(screen, zolotoy, (self.x, self.y), self.radius)
        # рисуем белую обводку
        pygame.draw.circle(screen, belyy, (self.x, self.y), self.radius, 2)
        # рисуем блик (для эффекта мерцания)
        if self.angle % 30 < 15:   # каждые 30 кадров блик появляется на 15 кадров
            pygame.draw.circle(screen, belyy, (self.x - 2, self.y - 2), 2)

# класс врага
class enemy:
    def __init__(self, x, y):   # конструктор
        self.x = x              # координата x
        self.y = y              # координата y
        self.width = 30         # ширина врага
        self.height = 25        # высота врага
        self.speed_x = random.choice([-2, -1, 1, 2])   # случайная скорость по x
        self.speed_y = random.choice([-1, 1]) if random.random() < 0.3 else 0   # скорость по y (30% что движется)
        self.active = True      # активен ли враг (не убит)

    def move(self):   # движение врага
        self.x += self.speed_x   # изменяем x на скорость
        self.y += self.speed_y   # изменяем y на скорость
        # отскок от краев экрана
        if self.x < 0 or self.x > shirina - self.width:   # если вышел за левый или правый край
            self.speed_x *= -1   # разворачиваемся по x
        if self.y < 50 or self.y > 550 - self.height:   # если вышел за верхний или нижний край
            self.speed_y *= -1   # разворачиваемся по y

    def check_collision(self, cat):   # проверка столкновения с котиком
        if not self.active or cat.invulnerable:   # если враг не активен или котик неуязвим
            return False   # не проверяем
        # расстояние до центра врага
        dist_x = abs(cat.x - (self.x + self.width // 2))   # расстояние по x
        dist_y = abs(cat.y - (self.y + self.height // 2))   # расстояние по y
        # если расстояния меньше суммы радиусов (половины размеров)
        if dist_x < cat.radius + self.width // 2 and dist_y < cat.radius + self.height // 2:
            # если котик прыгает сверху
            if cat.speed_y > 0 and cat.y + cat.radius < self.y + 10:
                self.active = False   # враг исчезает
                cat.speed_y = sila_pryzhka * 0.7   # котик отскакивает
                return "killed"   # враг убит
            else:   # если просто столкнулись
                cat.lives -= 1   # котик теряет жизнь
                cat.x = shirina // 2   # появляется в центре
                cat.y = 100            # наверху
                cat.invulnerable = True   # включаем неуязвимость
                cat.invulnerable_time = 120   # на 120 кадров
                return "hurt"   # котик пострадал
        return False   # не столкнулись

    def draw(self, screen):   # рисование врага
        if not self.active:   # если не активен
            return            # не рисуем
        # рисуем тело (тучка)
        pygame.draw.ellipse(screen, fionetoviy,
                            (self.x, self.y, self.width, self.height))
        # рисуем левый глаз
        pygame.draw.circle(screen, chernyy, (int(self.x + 8), int(self.y + 8)), 3)
        # рисуем правый глаз
        pygame.draw.circle(screen, chernyy, (int(self.x + 22), int(self.y + 8)), 3)
        # рисуем красный зрачок левого глаза
        pygame.draw.circle(screen, krasnyy, (int(self.x + 7), int(self.y + 7)), 1)
        # рисуем красный зрачок правого глаза
        pygame.draw.circle(screen, krasnyy, (int(self.x + 21), int(self.y + 7)), 1)

# класс звезды (падает с неба, дает монетку)
class star:
    def __init__(self):   # конструктор
        self.x = random.randint(20, shirina - 20)   # случайная x
        self.y = random.randint(-100, -20)          # над экраном
        self.radius = 8        # радиус
        self.speed = random.randint(3, 6)   # скорость падения
        self.active = True     # активна ли

    def update(self):   # обновление
        self.y += self.speed   # падаем вниз
        if self.y > visota + 20:   # если упали за экран
            self.active = False    # деактивируем

    def check_collection(self, cat):   # проверка сбора
        if not self.active:   # если не активна
            return False      # не собираем
        dist = ((cat.x - self.x) ** 2 + (cat.y - self.y) ** 2) ** 0.5   # расстояние
        if dist < cat.radius + self.radius:   # если коснулись
            self.active = False   # звезда исчезает
            cat.coins += 1        # даем монетку
            return True   # собрали
        return False      # не собрали

    def draw(self, screen):   # рисование звезды
        if not self.active:   # если не активна
            return            # не рисуем
        # рисуем круг
        pygame.draw.circle(screen, oranzhevyy, (self.x, self.y), self.radius)
        # рисуем 4 луча
        for i in range(4):   # 4 луча (вверх, вниз, влево, вправо)
            angle = i * 3.14 / 2   # угол: 0, 90, 180, 270 градусов
            # вычисляем конец луча
            x2 = self.x + (self.radius + 4) * pygame.math.Vector2(1, 0).rotate_rad(angle).x
            y2 = self.y + (self.radius + 4) * pygame.math.Vector2(1, 0).rotate_rad(angle).y
            pygame.draw.line(screen, zolotoy, (self.x, self.y), (x2, y2), 2)   # рисуем луч

# класс капельки (падает с неба, отнимает жизнь)
class drop:
    def __init__(self):   # конструктор
        self.x = random.randint(20, shirina - 20)   # случайная x
        self.y = random.randint(-100, -20)          # над экраном
        self.radius = 8        # радиус
        self.speed = random.randint(4, 7)   # скорость падения
        self.active = True     # активна ли

    def update(self):   # обновление
        self.y += self.speed   # падаем вниз
        if self.y > visota + 20:   # если упали за экран
            self.active = False    # деактивируем

    def check_collision(self, cat):   # проверка столкновения
        if not self.active or cat.invulnerable:   # если не активна или котик неуязвим
            return False   # не проверяем
        dist = ((cat.x - self.x) ** 2 + (cat.y - self.y) ** 2) ** 0.5   # расстояние
        if dist < cat.radius + self.radius:   # если коснулись
            self.active = False   # капля исчезает
            cat.lives -= 1        # котик теряет жизнь
            cat.invulnerable = True   # включаем неуязвимость
            cat.invulnerable_time = 120   # на 120 кадров
            return True   # столкнулись
        return False      # не столкнулись

    def draw(self, screen):   # рисование капли
        if not self.active:   # если не активна
            return            # не рисуем
        # рисуем синий круг
        pygame.draw.circle(screen, siniy, (self.x, self.y), self.radius)
        # рисуем блик
        pygame.draw.circle(screen, belyy, (self.x - 2, self.y - 2), 2)

# класс игры
class game:
    def __init__(self):   # конструктор
        self.screen = pygame.display.set_mode((shirina, visota))   # создаем окно
        pygame.display.set_caption("game 1")   # заголовок окна
        self.clock = pygame.time.Clock()   # часы для контроля fps
        self.font_big = pygame.font.Font(None, 72)   # большой шрифт
        self.font_medium = pygame.font.Font(None, 48)   # средний шрифт
        self.font_small = pygame.font.Font(None, 24)   # маленький шрифт
        self.start_game()   # запускаем игру

    def start_game(self):   # начать новую игру
        self.cat = kotik(shirina // 2, 500)   # создаем котика в центре
        self.level = 0        # начинаем с первого уровня (0 индекс)
        self.coins_needed = 5 # нужно 5 монет для перехода на следующий уровень
        self.falling_objects = []   # список падающих объектов (звезды и капли)
        self.create_time = 0  # счетчик для создания падающих объектов
        self.load_level()     # загружаем текущий уровень

    def load_level(self):   # загрузка уровня
        if self.level >= len(urovni):   # если прошли все уровни
            self.cat.victory = True   # победа
            return
        level_data = urovni[self.level]   # данные текущего уровня
        # создаем платформы
        self.platforms = []   # список платформ
        for x, y, w, tip in level_data['platformy']:   # для каждой платформы
            self.platforms.append(platforma(x, y, w, tip))   # создаем платформу
        # создаем монетки
        self.coins = []   # список монеток
        for x, y in level_data['monetki']:   # для каждой монетки
            self.coins.append(coin(x, y))   # создаем монетку
        # создаем врагов
        self.enemies = []   # список врагов
        for x, y in level_data['vragi']:   # для каждого врага
            self.enemies.append(enemy(x, y))   # создаем врага
        self.cat.coins = 0   # обнуляем монетки котика
        self.coins_needed = 5 + self.level * 2   # сколько нужно собрать (5, 7, 9...)
        self.level_type = level_data.get('tip', 'normal')   # тип уровня

    def handle_events(self):   # обработка событий (нажатия клавиш, закрытие окна)
        for event in pygame.event.get():   # для каждого события
            if event.type == pygame.QUIT:   # если нажали крестик
                return False   # выходим из игры
            if event.type == pygame.KEYDOWN:   # если нажали клавишу
                if event.key == pygame.K_ESCAPE:   # если нажали esc
                    return False   # выходим
                if event.key == pygame.K_r and (self.cat.lives <= 0 or self.cat.victory):   # если r и игра кончилась
                    self.start_game()   # начинаем заново
        return True   # продолжаем игру

    def update(self):   # обновление игровой логики
        keys = pygame.key.get_pressed()   # получаем список нажатых клавиш
        self.cat.move(keys)   # двигаем котика
        self.cat.update_invulnerable()   # обновляем неуязвимость
        # проверяем столкновения с платформами
        self.cat.on_ground = False   # сначала считаем что не на земле
        for platform in self.platforms:   # для каждой платформы
            platform.update(self.cat)   # обновляем платформу
            platform.check_collision(self.cat)   # проверяем столкновение
        # проверяем сбор монеток
        for coin in self.coins:   # для каждой монетки
            coin.check_collection(self.cat)   # проверяем, собрал ли котик
        # обновляем врагов
        for enemy in self.enemies:   # для каждого врага
            enemy.move()   # двигаем врага
            enemy.check_collision(self.cat)   # проверяем столкновение
        # удаляем убитых врагов
        self.enemies = [e for e in self.enemies if e.active]
        # удаляем исчезнувшие платформы
        self.platforms = [p for p in self.platforms if p.active]
        # обновляем падающие объекты
        for obj in self.falling_objects:   # для каждого объекта
            obj.update()   # обновляем
            if self.level_type == 'zvezdy' and hasattr(obj, 'check_collection'):   # если звезды
                obj.check_collection(self.cat)   # проверяем сбор
            elif self.level_type == 'kapelki' and hasattr(obj, 'check_collision'):   # если капли
                obj.check_collision(self.cat)   # проверяем столкновение
        # удаляем объекты, которые упали за экран
        self.falling_objects = [obj for obj in self.falling_objects if obj.active]
        # создаем новые падающие объекты
        if self.level_type in ['zvezdy', 'kapelki']:   # если уровень со звездами или каплями
            self.create_time += 1   # увеличиваем таймер
            if self.create_time > random.randint(15, 30):   # если пришло время
                if self.level_type == 'zvezdy':   # если звезды
                    self.falling_objects.append(star())   # добавляем звезду
                else:   # если капли
                    self.falling_objects.append(drop())   # добавляем каплю
                self.create_time = 0   # сбрасываем таймер
        # проверяем, можно ли перейти на следующий уровень
        all_coins_collected = all(c.collected for c in self.coins)   # все ли монетки собраны
        if all_coins_collected or self.cat.coins >= self.coins_needed:   # если все собраны или достаточно
            self.level += 1   # переходим на следующий уровень
            if self.level < len(urovni):   # если есть еще уровни
                self.load_level()   # загружаем следующий
            else:   # если это был последний уровень
                self.cat.victory = True   # победа

    def draw(self):   # отрисовка всего на экране
        self.screen.fill(rozoviy_fon)   # заливаем фон розовым
        # рисуем все платформы
        for platform in self.platforms:
            platform.draw(self.screen)
        # рисуем все монетки
        for coin in self.coins:
            coin.draw(self.screen)
        # рисуем всех врагов
        for enemy in self.enemies:
            enemy.draw(self.screen)
        # рисуем все падающие объекты
        for obj in self.falling_objects:
            obj.draw(self.screen)
        # рисуем котика
        self.cat.draw(self.screen)
        # рисуем интерфейс (текст)
        level_name = f"level: {self.level + 1}"   # номер уровня (плюс 1 так как счет с 0)
        if self.level_type == 'zvezdy':   # если звезды
            level_name += " *"   # добавляем звездочку
        elif self.level_type == 'kapelki':   # если капли
            level_name += " v"   # добавляем v
        text_level = self.font_small.render(level_name, True, fionetoviy)   # создаем текст уровня
        self.screen.blit(text_level, (shirina // 2 - 40, 10))   # рисуем в центре сверху
        # текст с монетками
        text_coins = self.font_small.render(f"coins: {self.cat.coins}/{self.coins_needed}", True, zolotoy)
        self.screen.blit(text_coins, (shirina - 140, 10))   # справа вверху
        # текст с жизнями
        text_lives = self.font_small.render(f"lives: {self.cat.lives}", True, krasnyy)
        self.screen.blit(text_lives, (20, 10))   # слева вверху
        # экран победы
        if self.cat.victory:
            s = pygame.Surface((shirina, visota))   # создаем полупрозрачный слой
            s.set_alpha(180)   # прозрачность 180 (0-255)
            s.fill((0, 0, 0))   # черный
            self.screen.blit(s, (0, 0))   # затемняем экран
            t1 = self.font_big.render("Победа!", True, zolotoy)   # текст победы
            t2 = self.font_small.render("r - restart", True, belyy)   # текст рестарта
            r1 = t1.get_rect(center=(shirina // 2, visota // 2 - 30))   # позиция по центру
            r2 = t2.get_rect(center=(shirina // 2, visota // 2 + 30))
            self.screen.blit(t1, r1)   # рисуем
            self.screen.blit(t2, r2)
        # экран проигрыша
        elif self.cat.lives <= 0:
            s = pygame.Surface((shirina, visota))   # создаем полупрозрачный слой
            s.set_alpha(180)   # прозрачность
            s.fill((0, 0, 0))   # черный
            self.screen.blit(s, (0, 0))   # затемняем экран
            t1 = self.font_big.render("game over", True, krasnyy)   # текст game over
            t2 = self.font_small.render("r - restart", True, belyy)   # текст рестарта
            r1 = t1.get_rect(center=(shirina // 2, visota // 2 - 30))
            r2 = t2.get_rect(center=(shirina // 2, visota // 2 + 30))
            self.screen.blit(t1, r1)
            self.screen.blit(t2, r2)

    def run(self):   # главный игровой цикл
        running = True   # флаг работы игры
        while running:   # пока игра работает
            running = self.handle_events()   # обрабатываем события
            if self.cat.lives > 0 and not self.cat.victory:   # если котик жив и не победил
                self.update()   # обновляем игру
            self.draw()   # рисуем все
            pygame.display.flip()   # обновляем экран
            self.clock.tick(fps)   # ждем до следующего кадра (60 раз в секунду)
        pygame.quit()   # закрываем pygame
        sys.exit()      # выходим из программы

# точка входа
if __name__ == "__main__":
    game_obj = game()   # создаем объект игры
    game_obj.run()      # запускаем игру
