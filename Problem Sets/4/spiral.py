import math

class Spiral:
    h = 1.0

    def __init__(self):
        pass

    def set_fc_prime(self, fc_prime):
        self.fc_prime = fc_prime
    def set_fy(self, fy):
        self.fy = fy
    def set_gamma(self, gamma):
        self.gamma = gamma
    def set_bar_qty(self, bar_qty):
        self.bar_qty = bar_qty
    def set_rho(self, rho):
        self.rho = rho

    def initialize(self):
        r = self.h / 2
        self.gross_area = math.pi * r**2

    def get_area(self):
        return self.gross_area
