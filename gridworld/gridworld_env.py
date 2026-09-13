import time
from collections import deque

import numpy as np
import pygame

CELL_SIZE = 100
MARGIN = 10


class GridWorldEnv:
    def __init__(self, num_rows=8, num_cols=8, num_traps=7, delay=0.05):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_traps = num_traps

        self.delay = delay

        move_up = lambda row, col: (max(row - 1, 0), col)
        move_down = lambda row, col: (min(row + 1, num_rows - 1), col)
        move_left = lambda row, col: (row, max(col - 1, 0))
        move_right = lambda row, col: (row, min(col + 1, num_cols - 1))

        self.action_defs = {0: move_up, 1: move_right, 2: move_down, 3: move_left}

        # Number of states/actions
        nS = num_cols * num_rows
        nA = len(self.action_defs)
        self.grid2state_dict = {(s // num_cols, s % num_cols): s for s in range(nS)}
        self.state2grid_dict = {s: (s // num_cols, s % num_cols) for s in range(nS)}

        self.nS = nS
        self.nA = nA
        self.rng = np.random.default_rng()
        self.terminal_states = []
        self.s = 0
        self.screen = None
        self._place_targets()
        self.reset()

    def is_terminal(self, state):
        return state in self.terminal_states

    def _place_targets(self):
        opposite_row = self.num_rows // 2
        opposite_col = self.num_cols // 2
        gold_candidates = [
            state
            for state in range(1, self.nS)
            if self.state2grid_dict[state][0] >= opposite_row
            and self.state2grid_dict[state][1] >= opposite_col
        ]

        for _ in range(1000):
            gold_state = int(self.rng.choice(gold_candidates))
            trap_candidates = [
                state for state in range(1, self.nS) if state != gold_state
            ]
            trap_states = [
                int(state)
                for state in self.rng.choice(
                    trap_candidates, size=self.num_traps, replace=False
                )
            ]
            if self._has_path_to_gold(gold_state, trap_states):
                self.terminal_states = [gold_state] + trap_states
                return

        raise RuntimeError("Could not generate a reachable GridWorld layout")

    def _has_path_to_gold(self, gold_state, trap_states):
        blocked_states = set(trap_states)
        visited_states = {0}
        states_to_visit = deque([0])

        while states_to_visit:
            state = states_to_visit.popleft()
            if state == gold_state:
                return True

            row, col = self.state2grid_dict[state]
            for move in self.action_defs.values():
                next_row, next_col = move(row, col)
                next_state = self.grid2state_dict[(next_row, next_col)]
                if (
                    next_state not in blocked_states
                    and next_state not in visited_states
                ):
                    visited_states.add(next_state)
                    states_to_visit.append(next_state)

        return False

    def reset(self, *, seed=None, options=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.s = 0
        return self.s, {}

    def step(self, action):
        if self.is_terminal(self.s):
            return self.s, 0.0, True, False, {}
        row, col = self.state2grid_dict[self.s]
        next_row, next_col = self.action_defs[int(action)](row, col)
        next_s = self.grid2state_dict[(next_row, next_col)]
        reward = 0.0
        terminated = self.is_terminal(next_s)
        if terminated:
            reward = 1.0 if next_s == self.terminal_states[0] else -1.0
        self.s = next_s
        return self.s, reward, terminated, False, {}

    def render(self, mode="human", done=False):
        if done:
            sleep_time = 1
        else:
            sleep_time = self.delay
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode(
                (self.num_cols * CELL_SIZE, self.num_rows * CELL_SIZE)
            )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return None
        background = (24, 31, 47)
        tile_a = (39, 51, 72)
        tile_b = (45, 59, 83)
        grid_color = (77, 94, 120)
        trap_color = (224, 91, 112)
        trap_shadow = (117, 42, 67)
        gold_color = (255, 201, 82)
        gold_shadow = (166, 111, 34)
        agent_color = (91, 214, 190)
        agent_highlight = (185, 255, 226)

        self.screen.fill(background)
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                rect = pygame.Rect(
                    col * CELL_SIZE + 2,
                    row * CELL_SIZE + 2,
                    CELL_SIZE - 4,
                    CELL_SIZE - 4,
                )
                tile_color = tile_a if (row + col) % 2 == 0 else tile_b
                pygame.draw.rect(self.screen, tile_color, rect, border_radius=8)
                pygame.draw.rect(self.screen, grid_color, rect, 1, border_radius=8)

        for state in self.terminal_states[1:]:
            row, col = self.state2grid_dict[state]
            center = (int((col + 0.5) * CELL_SIZE), int((row + 0.5) * CELL_SIZE))
            pygame.draw.circle(self.screen, trap_shadow, center, CELL_SIZE // 4 + 4)
            pygame.draw.circle(
                self.screen,
                trap_color,
                center,
                CELL_SIZE // 4,
            )
            pygame.draw.line(
                self.screen,
                (255, 180, 190),
                (center[0] - 12, center[1] - 12),
                (center[0] + 12, center[1] + 12),
                5,
            )
            pygame.draw.line(
                self.screen,
                (255, 180, 190),
                (center[0] + 12, center[1] - 12),
                (center[0] - 12, center[1] + 12),
                5,
            )

        row, col = self.state2grid_dict[self.terminal_states[0]]
        gold_center = (int((col + 0.5) * CELL_SIZE), int((row + 0.5) * CELL_SIZE))
        gold_points = [
            (gold_center[0], gold_center[1] - 30),
            (gold_center[0] + 30, gold_center[1]),
            (gold_center[0], gold_center[1] + 30),
            (gold_center[0] - 30, gold_center[1]),
        ]
        shadow_points = [(x + 4, y + 6) for x, y in gold_points]
        pygame.draw.polygon(
            self.screen,
            gold_shadow,
            shadow_points,
        )
        pygame.draw.polygon(self.screen, gold_color, gold_points)
        pygame.draw.line(
            self.screen,
            (255, 239, 174),
            gold_points[0],
            gold_points[2],
            4,
        )

        row, col = self.state2grid_dict[self.s]
        agent_rect = pygame.Rect(
            col * CELL_SIZE + 22,
            row * CELL_SIZE + 22,
            CELL_SIZE - 44,
            CELL_SIZE - 44,
        )
        pygame.draw.rect(
            self.screen, (17, 28, 39), agent_rect.move(4, 6), border_radius=18
        )
        pygame.draw.rect(self.screen, agent_color, agent_rect, border_radius=18)
        pygame.draw.rect(self.screen, agent_highlight, agent_rect, 3, border_radius=18)
        pygame.draw.circle(
            self.screen,
            (24, 43, 57),
            (agent_rect.centerx - 12, agent_rect.centery - 5),
            5,
        )
        pygame.draw.circle(
            self.screen,
            (24, 43, 57),
            (agent_rect.centerx + 12, agent_rect.centery - 5),
            5,
        )
        pygame.display.flip()
        time.sleep(sleep_time)
        if mode == "rgb_array":
            return np.transpose(pygame.surfarray.array3d(self.screen), (1, 0, 2))
        return None

    def close(self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()
            self.screen = None


if __name__ == "__main__":
    env = GridWorldEnv(8, 8)
    for i in range(1):
        s, _ = env.reset()
        env.render(mode="human", done=False)

        while True:
            action = np.random.choice(env.nA)
            next_s, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            print(
                "Action ",
                env.s,
                action,
                " -> ",
                (next_s, reward, terminated, truncated, info),
            )
            env.render(mode="human", done=done)
            if done:
                break

    env.close()
