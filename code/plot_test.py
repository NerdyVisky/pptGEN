import matplotlib.pyplot as plt

# Data for the efficiency comparison of divide-and-conquer algorithms
algorithms = ['Merge Sort', 'Quick Sort', 'Binary Search', 'Strassen’s Matrix Multiplication']
efficiencies = [90, 85, 95, 80]

fig, ax = plt.subplots()
ax.bar(algorithms, efficiencies, color='skyblue')
plt.savefig('code/buffer/figures/2.png')
plt.close()