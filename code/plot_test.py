import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
aes_implementations = ['Impl 1', 'Impl 2', 'Impl 3', 'Impl 4']
performance = [1.2, 0.8, 1.5, 1.1]

plt.figure()
plt.bar(aes_implementations, performance)
plt.xlabel('AES Implementations')
plt.ylabel('Performance (Gbps)')
plt.savefig('code/buffer/figures/2.png')
plt.close()