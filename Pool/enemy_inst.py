from Pool.enemy_pool import enemys_pool
import Sprites.enemys as enemys

class PooledEnemys:
    def __init__(self, list_anim:list, amount:int, isActivate:bool=False, type:str=None) -> None:
        self.animation = list_anim
        self.amount = amount
        self.isActivate = isActivate
        self.type = type
        self.instantiate()

    def instantiate(self):
        for i in range(0,self.amount):
            enemy_script = enemys.Enemy(self.animation,self.isActivate,self.type)
            enemys_pool.enemys_list.append(enemy_script)
