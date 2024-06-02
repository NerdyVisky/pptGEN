import matplotlib.pyplot as plt

# Data
market_shares = [25, 25, 20, 15, 15]
labels = ['Company A', 'Company B', 'Company C', 'Company D', 'Others']

# Creating the pie chart
plt.figure()
plt.pie(market_shares, labels=labels, autopct='%1.1f%%')
plt.savefig('code/buffer/figures/4.png')
plt.close()