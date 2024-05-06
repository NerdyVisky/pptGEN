from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# Data for the 3D plot
x = np.random.standard_normal(10)
y = np.random.standard_normal(10)
z = np.random.standard_normal(10)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z)
ax.set_xlabel('Research Area X')
ax.set_ylabel('Research Area Y')
ax.set_zlabel('Impact Factor')
plt.savefig('code/buffer/figures/5.png')
plt.close()