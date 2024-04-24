import matplotlib.pyplot as plt

# Data for the pie chart
phases = ['Lexical Analysis', 'Syntax Analysis', 'Semantic Analysis', 'Code Generation']
time_spent = [20, 30, 25, 25]

plt.figure(figsize=(8, 8))
plt.pie(time_spent, labels=phases, autopct='%1.1f%%', startangle=90, colors=['red', 'green', 'blue', 'yellow'])
plt.savefig('code/buffer/figures/2.png')
plt.close()