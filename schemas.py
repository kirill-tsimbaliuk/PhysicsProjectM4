from pydantic import BaseModel

class Vector(BaseModel):
    x: float
    y: float

class Ball(BaseModel):
    position: Vector
    linear_velocity: float
    angular_velocity: float
    weight: float
    radius: float

    @property
    def inertia(self) -> float:
        return 2 / 5 * self.weight * self.radius * self.radius

class Environment(BaseModel):
    friction: float
    alpha: float
    gravity: float


class WrongStartValueError(Exception):
    pass