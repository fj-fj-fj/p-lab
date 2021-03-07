# Feel free to flame me for rookie mistakes in coding. Your help is greatly valued.
# 
# https://pypi.org/project/scikit-spatial/
# https://scikit-spatial.readthedocs.io/en/latest/index.html
# https://dev.to/bacchu/intersection-of-a-vector-with-a-sphere-5b5k
# https://arunrocks.com/ray-tracer-in-python-1-points-in-3d-space-show-notes/
# https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""
Task2: Sphere-Line Intersection.

Напишите программу, которая находит точки столкновения сферы и прямой линии. Если их нет, 
то выводится фраза: «Коллизий не найдено» (кириллицей, будьте внимательны), если есть, то 
выводятся координаты точек, ограниченные символом новой строки. Координаты считываются из 
файла, который имеет следующий формат:
``{sphere: {center: [0, 0, 0], radius: 10.67}, line: {[1, 0.5, 15], [43, -14.6, 0.04]}}``

Примечание: файл не будет содержать синтаксических ошибок, однако объекты и ключи могут 
находится в свободной последовательности. Координаты точек – массив [x, y, z].

Дополнительно: верх крутости – рендеринг данной сцены.

"""
import sys
import math
from ast import literal_eval
from pathlib import Path

import matplotlib.pyplot as plt
from skspatial.objects import Line
from skspatial.objects import Sphere
from skspatial.plotting import plot_3d


class _Sphere:
    # Не используется пока-что

    def __init__(self, center: tuple, radius: float) -> None:
        """initialise Shpere and set main properties."""
        self.center = center
        self.radius = radius
        self.sur_area = 4 * math.pi * radius ** 2
        self.volume = (4/3) * (math.pi * radius ** 3)

        print('Surface Area is: ', self.sur_area)
        print('Volume is: ', self.volume)


class _Line:
    # Не используется пока-что

    def __init__(self, point1: tuple, point2: tuple) -> None :
        """initialise Line and set points."""
        self.point1 = point1
        self.point2 = point2


def find_collision_points(sphere: Sphere, line: Line) -> None:
    """Find the collision poins of a sphere and a straight line."""
    try:
        point_a, point_b = sphere.intersect_line(line)
        print(point_a)
        print(point_b)

        return plot_3d(  # FIXME: Ей богу, получалось
            line.plotter(t_1=-1, c='k'),
            sphere.plotter(alpha=0.2),
            point_a.plotter(c='r', s=100),
            point_b.plotter(c='r', s=100),
        )
    except ValueError:
        print('Коллизий не найдено')


try:
    path = sys.argv[1]
except:
    path = Path(__file__).with_name('data.txt')

with path.open(encoding='utf-8') as f:
    data = f.readlines()

    for coordinates in data:
        coordinates = literal_eval(coordinates)

        sphere: Sphere = Sphere(
            coordinates['sphere']['center'],
            coordinates['sphere']['radius'],
        )
        line: Line = Line(
            coordinates['line'][0],
            coordinates['line'][1],
        )

        find_collision_points(sphere, line)
