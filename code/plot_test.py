import matplotlib.pyplot as plt

# Data for pie chart
applications = ['Social Networks', 'Routing', 'Recommendation Systems', 'Network Analysis']
distribution = [30, 25, 20, 25]

plt.pie(distribution, labels=applications, autopct='%1.1f%%')
plt.savefig('code/buffer/figures/3.png')

plt.close()