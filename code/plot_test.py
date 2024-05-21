import matplotlib.pyplot as plt

# Data for the pie chart
techniques = ['Segmentation', 'Paging', 'Virtual Memory', 'Hybrid']
sizes = [25, 25, 30, 20]

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=techniques, autopct='%1.1f%%', startangle=140, colors=['gold', 'lightblue', 'lightgreen', 'lavender'])
plt.savefig('code/buffer/figures/3.png')
plt.close()