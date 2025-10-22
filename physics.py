from numpy import sin, cos

from schemas import *

EPS = 0.05

def get_time_when_finish_slippage(ball: Ball, env: Environment):
    angular_acceleration = env.friction * env.gravity * ball.radius * ball.weight / ball.inertia * cos(env.alpha)
    linear_acceleration = env.gravity * (sin(env.alpha) - env.friction * cos(env.alpha))

    time = ball.linear_velocity / (angular_acceleration * ball.radius - linear_acceleration)
    return time

class Processer:

    def __init__(self, ball: Ball, env: Environment):
        self.ball = ball
        self.env = env

        self.angular_acceleration = self.env.friction * self.env.gravity * self.ball.radius * self.ball.weight / self.ball.inertia * cos(self.env.alpha)
        self.linear_acceleration = self.env.gravity * (sin(self.env.alpha) - self.env.friction * cos(self.env.alpha))

        if self.linear_acceleration < 0:
            raise WrongStartValueError("The movement will not start")

        self.time = 0.0
        self.slippage = get_time_when_finish_slippage(self.ball, self.env) > 0

    def process(self, time_delta: float) -> None:
        if self.slippage:
            delta_angular = self.angular_acceleration * time_delta
            delta_linear = self.linear_acceleration * time_delta

            if abs(self.ball.linear_velocity - self.ball.angular_velocity * self.ball.radius) < EPS:
                self.slippage = False
                delta_angular = delta_linear / self.ball.radius
        else:
            delta_linear = self.linear_acceleration * time_delta
            delta_angular = delta_linear / self.ball.radius

        self.ball.linear_velocity += delta_linear
        self.ball.angular_velocity += delta_angular

        self.ball.position.x += self.ball.linear_velocity * cos(self.env.alpha) * time_delta
        self.ball.position.y -= self.ball.linear_velocity * sin(self.env.alpha) * time_delta

        self.time += time_delta

    def get_info(self) -> dict:
        data = {
            "time": self.time,
            "position_x": self.ball.position.x,
            "position_y": self.ball.position.y,
            "angular_velocity": self.ball.angular_velocity,
            "linear_velocity": self.ball.linear_velocity,
        }
        return data
