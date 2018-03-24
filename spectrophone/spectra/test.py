from matplotlib import pyplot as plt

from spectrophone.spectra import harmonic


x_axis = []
y_axis = []


for i in range(5):
    frequencies = harmonic.fractal(2, i, 5)
    for f in frequencies:
        x_axis.append(i)
        y_axis.append(f)

print(len(y_axis))


plt.hexbin(x_axis, y_axis)
plt.show()
