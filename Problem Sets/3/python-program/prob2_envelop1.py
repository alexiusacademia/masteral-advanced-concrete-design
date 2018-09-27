import matplotlib.pyplot as plt

x = [0, 0, 3, 3, 6, 6, 0]
y = [0, 233.8, 17.95, -17.95, -233.81, 0, 0]

y_d = [0, 192.8]
x_d = [.57, .57]

plt.figure(figsize=(10,8))
plt.title("Max. Shear Envelop")
plt.xlabel('x')
plt.ylabel('Shear, Vu')
plt.grid()

plt.plot(x, y, '-')
plt.plot(x_d, y_d, '--')

plt.text(.57, y_d[1]/2, 'Vu = ' + str(y_d[1]))
plt.text(3, 17.95, 'Vu (envelop) = ' + str('1.2LL'))
plt.text(0, 233.8, 'Vu (max) = ' + str('4.8LL + 162'))

plt.show()
