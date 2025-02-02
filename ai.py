import gym
from gym import spaces
import numpy as np
from constants import Constants
from pygame.math import Vector2

MAX_ENEMIES = 50
MAX_PROJECTILES = 50


class BulletHellEnv(gym.Env):
    def __init__(self, game):
        super(BulletHellEnv, self).__init__()
        self.game = game
        self.action_space = spaces.Discrete(6)  # 6 actions
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(MAX_ENEMIES * 4 + 2,), dtype=np.float32
        )
        self.prev_player_health = self.game.player.health
        self.prev_enemy_count = len(self.game.enemies)
        self.prev_enemy_health_sum = sum(
            enemy.curr_health for enemy in self.game.enemies
        )

    def reset(self):
        return self._get_state()

    def seed(self, seed=None):
        """Sets the seed for reproducibility."""
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def step(self, action):
        # Perform action in the game
        state = self._get_state()
        reward = self._calculate_reward()
        done = self.game.over
        return state, reward, done, {}

    def _get_state(self):
        player = self.game.player
        enemies = self.game.enemies[:MAX_ENEMIES]  # Limit to max enemies
        projectiles = self.game.projectiles[
            :MAX_PROJECTILES
        ]  # Limit to max projectiles

        # Player position (2 values)
        player_pos = np.array(
            [
                player.get_hitbox().x / Constants.WINDOW_WIDTH,
                player.get_hitbox().y / Constants.WINDOW_HEIGHT,
            ]
        )

        # Enemy positions (pad with -1 if fewer than MAX_ENEMIES)
        enemy_pos = np.full((MAX_ENEMIES * 2,), -1.0)
        for i, e in enumerate(enemies):
            enemy_pos[i * 2 : i * 2 + 2] = [
                e.get_hitbox().x / Constants.WINDOW_WIDTH,
                e.get_hitbox().y / Constants.WINDOW_HEIGHT,
            ]

        # Projectile positions (pad with -1 if fewer than MAX_PROJECTILES)
        projectile_pos = np.full((MAX_PROJECTILES * 2,), -1.0)
        for i, p in enumerate(projectiles):
            projectile_pos[i * 2 : i * 2 + 2] = [
                p.drect.x / Constants.WINDOW_WIDTH,
                p.drect.y / Constants.WINDOW_HEIGHT,
            ]

        # Concatenate to a fixed-size array
        state = np.concatenate([player_pos, enemy_pos, projectile_pos])

        return state.astype(np.float32)

    def _calculate_reward(self) -> None:
        reward = 1.0
        if self.game.player.health > 0:
            reward += 0.1
        if self.game.player.health == 0:
            reward -= 100.0
        if self.game.player.health < self.prev_player_health:
            reward -= 10.0
        enemy_health_sum = sum(enemy.curr_health for enemy in self.game.enemies)
        if len(self.game.enemies) == 0 or self.prev_enemy_count == 0:
            pass
        else:
            if (
                enemy_health_sum / len(self.game.enemies)
                < self.prev_enemy_health_sum / self.prev_enemy_count
            ):
                reward += 10.0
        reward -= len(self.game.projectiles)

        self.prev_enemy_count = len(self.game.enemies)
        self.prev_enemy_health_sum = enemy_health_sum
        if self.game.player.vel.magnitude() < 0.1:
            reward -= 1.0
        return reward
