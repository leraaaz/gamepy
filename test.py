import unittest
import pygame
import os

# 1. Исправляем импорт: используем Main (как в вашем проекте)
try:
   from Main import Kotik, Platforma, Vrag, Monetka
except ImportError:
   print("Ошибка: Не удалось найти файл Main.py. Проверьте имя файла!")


# Специальный класс-заглушка для клавиш, чтобы избежать IndexError
class MockKeys:
   def __init__(self, pressed_keys=None):
       self.pressed_keys = pressed_keys or []

   def __getitem__(self, key):
       # Если клавиша есть в списке нажатых - возвращаем True, иначе False
       return key in self.pressed_keys


class TestGame(unittest.TestCase):

   @classmethod
   def setUpClass(cls):
       # Инициализация Pygame в режиме без окна
       os.environ['SDL_VIDEODRIVER'] = 'dummy'
       pygame.init()
       pygame.display.set_mode((1, 1))

   def setUp(self):
       self.kotik = Kotik(400, 300)

   def test_gravity_application(self):
       """Проверка, что гравитация тянет котика вниз"""
       initial_y = self.kotik.y
       # Передаем пустой объект клавиш
       self.kotik.dvigatsya(MockKeys())
       self.assertTrue(self.kotik.y > initial_y, "Котик должен падать вниз")

   def test_coin_collection(self):
       """Проверка сбора монет"""
       # Здесь была ошибка импорта, теперь всё должно быть Ок
       monetka = Monetka(400, 300)
       self.kotik.monetki = 0

       monetka.proverka_sbora(self.kotik)
       self.assertEqual(self.kotik.monetki, 1)
       self.assertTrue(monetka.sobrana)

   def test_movement_left(self):
       """Проверка движения влево"""
       initial_x = self.kotik.x
       # Эмулируем нажатие клавиши 'A' (влево)
       keys = MockKeys(pressed_keys=[pygame.K_a])
       self.kotik.dvigatsya(keys)
       self.assertTrue(self.kotik.x < initial_x, "Котик должен сдвинуться влево")

   def test_jump_limit(self):
       """Проверка лимита прыжков"""
       self.kotik.na_zemle = False
       self.kotik.skolko_pryzhkov_sdelal = 2

       # Пытаемся прыгнуть в третий раз (Space)
       keys = MockKeys(pressed_keys=[pygame.K_SPACE])
       self.kotik.dvigatsya(keys)

       # Счётчик не должен стать 3
       self.assertEqual(self.kotik.skolko_pryzhkov_sdelal, 2)


if __name__ == '__main__':
   unittest.main()
 