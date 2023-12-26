import matplotlib.pyplot as plt

# Data for NVIDIA A100 PCIe 80 GB GPU
a100_tokens = [500, 400, 300, 200, 100]
a100_power_consumption = [15.3362, 14.1392, 13.1083, 12.6353, 7.0094]

# Data for NVIDIA A40 PCIe GPU
a40_tokens = [500, 400, 300, 200, 100]
a40_power_consumption = [0.6701, 0.6901, 0.5470, 0.4404, 0.2570]

# Plotting for A100
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(a100_tokens, a100_power_consumption, marker='o', label='NVIDIA A100 PCIe 80 GB GPU')
plt.title('NVIDIA A100 PCIe 80 GB GPU (LLaMA 2 70B)')
plt.xlabel('Max Tokens')
plt.ylabel('Power Consumption (W)')
plt.legend()

# Plotting for A40
plt.subplot(1, 2, 2)
plt.plot(a40_tokens, a40_power_consumption, marker='o', label='NVIDIA A40 PCIe GPU')
plt.title('NVIDIA A40 PCIe GPU (LLaMA 2 13B)')
plt.xlabel('Max Tokens')
plt.ylabel('Power Consumption (W)')
plt.legend()

plt.tight_layout()
plt.show()
