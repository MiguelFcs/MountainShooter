from code.Const import WIN_WIDTH
from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Player import Player
from code.PlayerShot import PlayerShot


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy) and ent.rect.right <= 0:
            ent.health = 0
        elif isinstance(ent, PlayerShot) and ent.rect.left >= WIN_WIDTH:
            ent.health = 0
        elif isinstance(ent, EnemyShot) and ent.rect.right <= 0:
            ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1: Entity, ent2: Entity, ent3: Entity = None):
        if ent1.rect.colliderect(ent2.rect):  # Verifica colisão entre ent1 e ent2
            if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
                ent1.health -= ent2.damage
                ent2.health = 0  # Tiro é destruído após colisão
                ent1.last_dmg = ent2.name
            elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
                ent1.health -= ent2.damage
                ent2.health = 0
            elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
                ent2.health -= ent1.damage
                ent1.health = 0
                ent2.last_dmg = ent1.name
            elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
                ent2.health -= ent1.damage
                ent1.health = 0

        # Verifica colisão com ent3, caso exista
        if ent3 and ent1.rect.colliderect(ent3.rect):
            if isinstance(ent1, Enemy) and isinstance(ent3, PlayerShot):
                ent1.health -= ent3.damage
                ent3.health = 0
                ent1.last_dmg = ent3.name
            elif isinstance(ent1, PlayerShot) and isinstance(ent3, Enemy):
                ent3.health -= ent1.damage
                ent1.health = 0
                ent3.last_dmg = ent1.name
            elif isinstance(ent1, Player) and isinstance(ent3, EnemyShot):
                ent1.health -= ent3.damage
                ent3.health = 0
            elif isinstance(ent1, EnemyShot) and isinstance(ent3, Player):
                ent3.health -= ent1.damage
                ent1.health = 0

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        for ent in entity_list:
            if ent.name == 'Player1' and enemy.last_dmg == 'Player1Shot':
                ent.score += enemy.score
            elif ent.name == 'Player2' and enemy.last_dmg == 'Player2Shot':
                ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                for k in range(j + 1, len(entity_list)):  # Adiciona o terceiro elemento para colisões
                    entity3 = entity_list[k]
                    EntityMediator.__verify_collision_entity(entity1, entity2, entity3)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list[:]:  # Cria uma cópia da lista para evitar erros de modificação
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                entity_list.remove(ent)
