import city_generator
import city_generator.city_generator
from city_generator.city_generator import City

c = City(4, 4, 5134)
print(c.pos)
print(c.G.edges())

c.draw()

for e in c.edges:
    print(e)