import matplotlib.pyplot as plt

# Data for plotting
methods = ['Mutex', 'Semaphore', 'Monitor', 'Message Passing']
performance = [85, 90, 80, 75]

fig, ax = plt.subplots()
ax.bar(methods, performance, color='blue')

ax.set_ylabel('Performance')
ax.set_xlabel('Synchronization Methods')

# Save the figure
plt.savefig('code/buffer/figures/1.png')
plt.close()