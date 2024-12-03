from city_generator import City
import config as con

c= City(con.netRows, con.netCols, con.seed)

pos = c.generate_scale_position()

for key, val in pos.items():
    print(key, val)