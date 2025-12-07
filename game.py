import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    DERECHA = 1
    IZQUIERDA = 2
    ARRIBA = 3
    ABAJO = 4

Point = namedtuple('Point', 'x, y')

BLANCO = (255, 255, 255)
ROJO = (200, 0, 0)
AZUL1 = (0, 0, 255)
AZUL2 = (0, 100, 255)
NEGRO = (0, 0, 0)

BLOQUE_TAMANIO = 20
VELOCIDAD = 20

class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake IA - Dilan Salas')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        
        self.direction = Direction.DERECHA

        
        self.head = Point(self.w/2, self.h/2)
        
        self.snake = [self.head,
                      Point(self.head.x-BLOQUE_TAMANIO, self.head.y),
                      Point(self.head.x-(2*BLOQUE_TAMANIO), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        
        x = random.randint(0, (self.w-BLOQUE_TAMANIO )//BLOQUE_TAMANIO )*BLOQUE_TAMANIO
        y = random.randint(0, (self.h-BLOQUE_TAMANIO )//BLOQUE_TAMANIO )*BLOQUE_TAMANIO
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self._move(action)
        self.snake.insert(0, self.head)
        
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10 
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        
        self._update_ui()
        self.clock.tick(VELOCIDAD)
        
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        
        if pt.x > self.w - BLOQUE_TAMANIO or pt.x < 0 or pt.y > self.h - BLOQUE_TAMANIO or pt.y < 0:
            return True
        
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(NEGRO)

        for pt in self.snake:
            pygame.draw.rect(self.display, AZUL1, pygame.Rect(pt.x, pt.y, BLOQUE_TAMANIO, BLOQUE_TAMANIO))
            pygame.draw.rect(self.display, AZUL2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, ROJO, pygame.Rect(self.food.x, self.food.y, BLOQUE_TAMANIO, BLOQUE_TAMANIO))

        text = font.render("Score: " + str(self.score), True, BLANCO)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):

        clock_wise = [Direction.DERECHA, Direction.ABAJO, Direction.IZQUIERDA, Direction.ARRIBA]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.DERECHA:
            x += BLOQUE_TAMANIO
        elif self.direction == Direction.IZQUIERDA:
            x -= BLOQUE_TAMANIO
        elif self.direction == Direction.ABAJO:
            y += BLOQUE_TAMANIO
        elif self.direction == Direction.ARRIBA:
            y -= BLOQUE_TAMANIO

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGameAI()
    
    while True:
        reward, game_over, score = game.play_step([1, 0, 0])
        
        if game_over:
            game.reset()