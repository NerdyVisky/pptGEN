import matplotlib.pyplot as plt

# Data for the line chart
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
efficiency = [0.75, 0.78, 0.80, 0.83, 0.85, 0.87, 0.90, 0.92]

fig, ax = plt.subplots()
ax.plot(years, efficiency, marker='o')

ax.set_xlabel('Year')
ax.set_ylabel('Efficiency')
ax.set_title('Line chart summarizing the efficiency of A* algorithm')

plt.savefig('code/buffer/figures/3.png')
plt.close()