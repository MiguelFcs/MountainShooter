#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY, WIN_HEIGHT, ENTITY_MOVE_SPEED
from code.EnemyShot import EnemyShot
from code.Entity import Entity

class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.sin_wave_offset = 0  # Offset para o movimento sinusoidal
        self.moving_down = True

    def move(self):
        if self.name == 'Enemy3':
            # Movimento no eixo horizontal (X) - da direita para a esquerda
            self.rect.centerx -= ENTITY_MOVE_SPEED[self.name]

            # Movimento no eixo vertical (Y) - sobe e desce com comportamento especial
            move_speed = ENTITY_MOVE_SPEED[self.name]
            if self.moving_down:  # Checa a direção do movimento
                self.rect.centery += move_speed  # Movimento para baixo
            else:
                self.rect.centery -= move_speed  # Movimento para cima

            # Detecta bordas da tela para inverter o movimento
            if self.rect.bottom >= WIN_HEIGHT:  # Se atingir a borda inferior
                self.moving_down = False  # Começa a subir
            elif self.rect.top <= 0:  # Se atingir a borda superior
                self.moving_down = True  # Começa a descer
                move_speed *= 2  # Dobra a velocidade de descida

            if self.moving_down:
                self.rect.centery += move_speed  # Movimento para baixo com velocidade dobrada

        else:
            # Movimento padrão para outros inimigos
            self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
