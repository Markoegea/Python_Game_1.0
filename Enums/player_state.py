from enum import Enum

class PlayerState(Enum):
    IDLE = 0,
    WALKING = 1,
    JUMP = 2,
    JUMPING = 3,
    