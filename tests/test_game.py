import unittest
from unittest.mock import patch
import pygame
from src.ball import Ball
from src.tile import Tile
from src.spike import Spike, InvertedSpike
from src.gravity_portal import GravityPortal
from src.finish_line import FinishLine
from src.jump_orb import JumpOrb
from src.constants import *

class TestGameMechanics(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(100, 100)
        self.platform = Tile(100, 150)
        self.spike = Spike(150, 150)
        self.gravity_portal = GravityPortal(200, 150)
        self.finish_line = FinishLine(300, 150)
    
    def test_ball_moves_right(self):
        initial_x = self.ball.x
        self.ball.update([], [self.finish_line])
        self.assertGreater(self.ball.x, initial_x, "Ball should move to the right.")
    
    def test_ball_falls_due_to_gravity(self):
        initial_y = self.ball.y
        self.ball.update([], [self.finish_line])
        self.assertGreater(self.ball.y, initial_y, "Ball should fall due to gravity.")
    
    def test_ball_stops_on_platform(self):
        self.ball.y = 140 
        self.ball.update([self.platform], [self.finish_line])
        self.assertTrue(self.ball.on_ground, "Ball should land on the platform.")
    
    def test_ball_dies_on_spike(self):
        self.ball.x = 150
        self.ball.y = 150
        result = self.ball.update([], [self.spike, self.finish_line])
        self.assertEqual(result, "death", "Ball should die upon hitting a spike.")
    
    def test_gravity_reverses_in_portal(self):
        initial_gravity = self.ball.gravity
        self.ball.x = 200
        self.ball.y = 150
        self.gravity_portal.check_collision(self.ball)
        self.assertEqual(self.ball.gravity, -initial_gravity, "Gravity should be reversed upon entering portal.")
    
    def test_ball_reaches_finish(self):
        self.ball.x = 300
        self.ball.y = 150
        result = self.ball.update([], [self.finish_line])
        self.assertEqual(result, "finish", "Ball should trigger level completion upon reaching finish line.")

    def test_fast_fall_still_lands(self):
        self.ball.y = self.platform.y - 20 * TILE_SIZE
        self.ball.x = self.platform.x + TILE_SIZE // 2
        for _ in range(200):
            self.ball.velocity_x = 0
            self.ball.update([self.platform], [])
            if self.ball.on_ground:
                break
        self.assertTrue(self.ball.on_ground, "Ball should land even after a long fall.")

    def test_fall_speed_is_limited(self):
        for _ in range(100):
            self.ball.update([], [])
        self.assertLessEqual(self.ball.velocity_y, MAX_FALL, "Fall speed should not grow forever.")

    def test_ball_dies_on_inverted_spike(self):
        spike = InvertedSpike(150, 150)
        self.ball.gravity = -GRAVITY
        self.ball.x = 150 + TILE_SIZE // 2
        self.ball.y = 150 + TILE_SIZE // 2
        result = self.ball.update([], [spike])
        self.assertEqual(result, "death", "Ball should die upon hitting an inverted spike.")

    def test_ball_survives_next_to_spike(self):
        self.ball.x = 150 - BALL_RADIUS - 5
        self.ball.y = 150 + TILE_SIZE - BALL_RADIUS
        self.ball.velocity_x = 0
        self.ball.gravity = 0
        self.assertIsNone(self.spike.check_collision(self.ball), "Ball should not die before touching the spike.")

    def test_jump_orb_works_once(self):
        orb = JumpOrb(100, 100)
        with patch("pygame.key.get_pressed", return_value={pygame.K_SPACE: True}):
            orb.check_collision(self.ball)
            self.assertEqual(self.ball.velocity_y, -JUMP, "Orb should make the ball jump.")
            self.ball.velocity_y = 0
            orb.check_collision(self.ball)
        self.assertEqual(self.ball.velocity_y, 0, "Orb should not work twice in one pass.")

if __name__ == "__main__":
    unittest.main()
