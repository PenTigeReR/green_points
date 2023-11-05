import cv2
import numpy as np
from matplotlib import pyplot as plt


image = cv2.imread('C:/coding/Untitled Folder/samples/20090101-IMG_0027.jpg')

# Преобразование изображения в формат HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Определение диапазона для зеленого цвета в HSV
lower_green = np.array([25, 100, 100])
upper_green = np.array([90, 255, 255])

# Создание бинарной маски для зеленых пикселей
mask = cv2.inRange(hsv, lower_green, upper_green)

blur = cv2.GaussianBlur(mask,(13,13), 100)

# Нахождение контуров на бинарной маске
contours, _ = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Инициализация пустого списка для хранения центров окружностей
circle_centers = []

#Пустой список отфильтрованных точек
green_points = []

angle = []

# Поиск окружностей и их центров
for contour in contours:
    # Минимальная и максимальная площадь окружности
    min_radius = 3
    max_radius = 30
    if len(contour) >= 5:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius > min_radius and radius < max_radius:

            green_points.append((x,y))
            center = (int(x), int(y))
            radius = int(radius)
            circle_centers.append((center, radius))
            
        

if len(contours) > 0:
    all_points = np.array(green_points)
    #поиск параметров описанной окружности
    (x, y), radius = cv2.minEnclosingCircle(all_points.astype(np.int32))
    center_apporxing = (int(x) , int(y))
    radius_approxing = int(radius)
    cv2.circle(image, center_apporxing, radius_approxing, (255, 0, 0), 5)
    x0, y0 = center_apporxing
    print("Координаты центра окружности:", center)
    print("Радиуса центра окружности:", radius)

    i = 1
    angle_delta = 0

    for (center_small, radius) in circle_centers:
        #рисуем маленькие окружности
        cv2.circle(image, center_small, radius, (255, 0, 0), 2)
        x, y = center_small
        #угол отклонения
        angle_unit = round(( -1*np.arctan((y-y0)/(x-x0+1)))*(180/np.pi), 1) 
        angle_delta =+ round(radius/radius_approxing * (180/np.pi), 1) #уебищный расчет погрешности
        angle.append((angle_unit, angle_delta))
        #текст около точки
        cv2.putText(image, f"{angle_unit}  {round(angle_delta,2)} {i}", (x+50, y), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 0, 0), 2)

        i+=1
            

# Вывод координат центра каждой окружности
#for i, center in enumerate(circle_centers):
#    print(f"Центр окружности {i + 1}: x = {center[0]}, y = {center[1]}")

delta_angle=[[[],[]],[[],[]]]
pogr = 0


#рассчет дельт(уебищный)
for j in range(2): 
    for i in range(j, len(angle)-2, 2):
            delta_angle_value = (angle[-1 * i][0] - angle[-1 * (i+2)][0])*(1-2*(i%2))
            if abs(delta_angle_value)<20:
                    delta_angle[j][0].append(delta_angle_value)
                    delta_angle[j][1].append(angle[-1 * i][0])
            pogr +=angle[i][1]
            

 
x0 = np.arange(0,len(delta_angle[0][0]), 1)
x1 = np.arange(0,len(delta_angle[1][0]), 1)

#вывод графиков

if 1==0:
    plt.subplot(221)
    plt.errorbar(delta_angle[0][1], delta_angle[0][0], yerr=pogr/i)
    plt.title(r'правовая разность углов отклонения')

    plt.subplot(222)
    plt.errorbar(delta_angle[1][1], delta_angle[1][0], yerr=pogr/i)
    plt.title(r'левовая разность углов отклонения')
else:
    plt.imshow(image)

plt.show()