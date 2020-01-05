import taichi as ti
import numpy as np
from mpm_solver import MPMSolver

write_to_disk = False

# Try to run on GPU
ti.cfg.arch = ti.cuda

gui = ti.GUI("Taichi MLS-MPM-99", res=512, background_color=0x112F41)

mpm = MPMSolver(res=(64, 64, 64), size=10)

mpm.add_cube(lower_corner=[2, 4, 3], cube_size=[1, 1, 3], material=MPMSolver.material_elastic)

mpm.set_gravity((0, -50, 0))

for frame in range(500):
  mpm.step(4e-3)
  colors = np.array([0x068587, 0xED553B, 0xEEEEF0], dtype=np.uint32)
  np_x, np_v, np_material = mpm.particle_info()
  np_x = np_x / 10.0

  # simple camera transform
  screen_x = ((np_x[:, 0] + np_x[:, 2]) / 2 ** 0.5) - 0.2
  screen_y = (np_x[:, 1])

  screen_pos = np.stack([screen_x, screen_y], axis=-1)

  gui.circles(screen_pos, radius=1.5, color=colors[np_material])
  gui.show(f'{frame:06d}.png' if write_to_disk else None)
