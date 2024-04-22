import matplotlib.pyplot as plt

# Data for the line chart
algorithms = ['DFS', 'BFS', 'Dijkstra', 'Bellman-Ford', 'Floyd-Warshall']
complexities = [0.1, 0.1, 0.3, 0.35, 0.5]

plt.plot(algorithms, complexities, marker='o')
plt.xlabel('Algorithms')
plt.ylabel('Complexity')

plt.savefig('code/buffer/figures/5.png')
plt.close()