import matplotlib.pyplot as plt

# Data for the line chart
years = [2000, 2005, 2010, 2015, 2020]
standards = [20, 40, 60, 80, 100]

# Creating the line chart
fig3, ax3 = plt.subplots()
ax3.plot(years, standards, marker='o')

# Save the figure
plt.savefig('code/buffer/figures/3.png')
plt.close()