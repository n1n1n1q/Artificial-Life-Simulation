"""
Main
"""
from map import Grid
gr = Grid(5, 5, 1)
# print(gr._map)
gr.update_grid()
# print(gr._map)
print(gr.to_arr_colors())
print(gr._map)
