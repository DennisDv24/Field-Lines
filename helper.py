import math
import matplotlib.pyplot as plt
import matplotlib.collections as collections
import sys

Q_CONSTANT = 1.602 * 10 ** (-19)
MAGNITUDE_TO_RADIUS_FACTOR = 0.2 / Q_CONSTANT
SIZE_OF_GRAPH = [10,5]


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def get_angle(self):
        return math.atan2(self.y, self.x)

    def get_tuple(self):
        return self.x, self.y

    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)

    def subtract(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y)

    @staticmethod
    def create(magnitude, angle):
        return Vector(magnitude * math.cos(angle), magnitude * math.sin(angle))

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Item: #Def a charge
    def __init__(self, repels: bool, magnitude, position: Vector):
        self.repels = repels
        self.magnitude = magnitude
        self.position = position

    def get_radius(self):
        return self.magnitude * MAGNITUDE_TO_RADIUS_FACTOR #radius proportional to charge value

    def is_position_inside_item(self, position: Vector) -> bool:
        return self.position.subtract(position).get_magnitude() < self.get_radius()


class Graph:
    axis = plt.gca()
    axis.set_xticks([])
    axis.set_yticks([])
    @staticmethod
    def is_within_borders(end_vector: Vector):
        return -SIZE_OF_GRAPH[0] < end_vector.x < SIZE_OF_GRAPH[0] and -SIZE_OF_GRAPH[0] < end_vector.y < SIZE_OF_GRAPH[0]
                    #^Condition equiv to: return True if a<b<c
    @staticmethod
    def setup():
        axis = plt.gca()
        axis.set_xlim((-SIZE_OF_GRAPH[0], SIZE_OF_GRAPH[0]))
        axis.set_ylim((-SIZE_OF_GRAPH[1], SIZE_OF_GRAPH[1]))
        axis.set_aspect('equal')

    @staticmethod
    def draw_lines(lines_to_draw, colors=None):
        line_collection = collections.LineCollection(lines_to_draw, colors='b')
        Graph.axis.add_collection(line_collection)

    @staticmethod
    def draw_item(item):
        circle = plt.Circle(item.position.get_tuple(), 1,
                            color="b")

        Graph.axis.add_artist(circle)

    @staticmethod
    def show_graph():
        plt.show()


def convert_to_rgba(minval, maxval, val, colors):
    
    """""

    # Modified from:
    # https://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map
    # "colors" is a series of RGB colors delineating a series of
    # adjacent linear color gradients between each pair.
    # Determine where the given value falls proportionality within
    # the range from minval->maxval and scale that fractional value
    # by the total number in the "colors" pallette.
    i_f = float(val - minval) / float(maxval - minval) * (len(colors) - 1)
    # Determine the lower index of the pair of color indices this
    # value corresponds and its fractional distance between the lower
    # and the upper colors.
    i, f = int(i_f // 1), i_f % 1  # Split into whole & fractional parts.
    # Does it fall exactly on one of the color points?
    if f < sys.float_info.epsilon:
        (r, g, b) = colors[i]
        return r / 255, g / 255, b / 255, 1
    else:  # Otherwise return a color within the range between them.
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i + 1]
        return int(r1 + f * (r2 - r1)) / 255, int(g1 + f * (g2 - g1)) / 255, int(b1 + f * (b2 - b1)) / 255, 1
    """""
    pass 

def convert_magnitudes_to_colors(magnitudes):
    def magnitude_to_radius(magnitude_to_convert):
        return math.sqrt(1 / magnitude_to_convert)

    max_radius = magnitude_to_radius(min(magnitudes))
    min_radius = magnitude_to_radius(max(magnitudes))

    color_code = [(255, 0, 0), (0, 0, 255), (0, 255, 0)]
    colors = []
    for magnitude in magnitudes:
        colors.append(convert_to_rgba(min_radius, max_radius, magnitude_to_radius(magnitude), color_code))
    return colors
