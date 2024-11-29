import simulation.city_generator.city_config as cc
from simulation.city_generator.city_generator import City

c = City(cc.netRows, cc.netCols, cc.seed)
c.draw()