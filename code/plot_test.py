import matplotlib.pyplot as plt

# Data for pie chart summarizing key concepts
labels = ['Random Variables', 'Distributions', 'Randomized Algorithms', 'Deterministic Algorithms']
sizes = [25, 25, 25, 25]

# Creating pie chart
plt.figure()
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.savefig('code/buffer/figures/5.png')
plt.close()