import unittest
import pygame
from src.GD_ball import Ball
from src.GD_tile import Tile
from src.GD_spike import Spike
from src.GD_gravity_portal import Gravity_portal
from src.GD_finish_line import FinishLine
from src.GD_constants import *

class TestGameMechanics(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(100, 100)
        self.platform = Tile(100, 150)
        self.spike = Spike(150, 150)
        self.gravity_portal = Gravity_portal(200, 150)
        self.finish_line = FinishLine(300, 150)
    
    def test_ball_moves_right(self):
        initial_x = self.ball.x
        self.ball.update([], [], [], [], [], [], self.finish_line)
        self.assertGreater(self.ball.x, initial_x, "Ball should move to the right.")
    
    def test_ball_falls_due_to_gravity(self):
        initial_y = self.ball.y
        self.ball.update([], [], [], [], [], [], self.finish_line)
        self.assertGreater(self.ball.y, initial_y, "Ball should fall due to gravity.")
    
    def test_ball_stops_on_platform(self):
        self.ball.y = 140 
        self.ball.update([self.platform], [], [], [], [], [], self.finish_line)
        self.assertTrue(self.ball.on_ground, "Ball should land on the platform.")
    
    def test_ball_dies_on_spike(self):
        self.ball.x = 150
        self.ball.y = 150
        result = self.ball.update([], [], [], [], [self.spike], [], self.finish_line)
        self.assertTrue(result, "Ball should die upon hitting a spike.")
    
    def test_gravity_reverses_in_portal(self):
        initial_gravity = self.ball.gravity
        self.ball.x = 200
        self.ball.y = 150
        self.gravity_portal.check_collision(self.ball)
        self.assertEqual(self.ball.gravity, -initial_gravity, "Gravity should be reversed upon entering portal.")
    
    def test_ball_reaches_finish(self):
        self.ball.x = 300
        self.ball.y = 150
        result = self.ball.update([], [], [], [], [], [], self.finish_line)
        self.assertEqual(result, "finish", "Ball should trigger level completion upon reaching finish line.")

if __name__ == "__main__":
    unittest.main()
