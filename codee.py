import cv2
import numpy as np


# открыли изо 
image = cv2.imread('in.png')


# так оно выглядит в оригинале
cv2.imshow('original', image)
#Ожидание вашей реакции (закрытия окна или любой клавищи)
cv2.waitKey(0)


# Преобразовываем изображение
# Размытие
image_blur = cv2.blur(image, (20,20) )
# Посмотрели и поверили мне
cv2.imshow('blur', image_blur)

cv2.waitKey(0) 


# перевели в HSV
image_HSV = cv2.cvtColor( image_blur, cv2.COLOR_BGR2HSV )
# Так оно выглядит в HSV, сv2  пытается преобразовать это в BGR, потому так красиво 
cv2.imshow('HSV', image_HSV)

cv2.waitKey(0) 

#Теперь выбираем цвет, пусть будет зеленый
color_low = (35, 170, 50)
color_high = (90,255,255)

# Находим маску по нашему цвету
mask = cv2.inRange(image_HSV, color_low, color_high)
# так выглядит маска. она - двумерный массив по размеру изображения
cv2.imshow('mask', mask)

cv2.waitKey(0)

# Теперь нам с этой маской нужно что-то сделать
# найдем все контуры по этому цвету

conts, h = cv2.findContours( mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
# нас интересует conts , всё остальное оставим как есть 
# conts - это массив массивов точек
# теперь мы хотим применить наши контуры к изображению
# для этого есть специальная функция

# мы будем рисовать на оригинальном изображении image, но сделаем копию
image_copy = image.copy()
# conts - наши контуры
# -1 - говорит о том, что рисуем все (если другое число, то конкретный по номеру этого числа)
# clr - цвет контура в формате BGR 
clr = (0, 0, 255) # красненький
# толщина контура. Если Толщина будет равна -1, то контур закрашивается
thicknes = 2
cv2.drawContours(image_copy, conts, -1, clr, 2)
# Посмотрим на наше изо с контурами
cv2.imshow('contours', image_copy)

cv2.waitKey(0)

# Уже неплохо, но у нас есть маленькие сопельки-контуры, которые нам явно не нужны
# Давайте мы их уберем
# И в этом нам поможет сортировка

conts_sorted = sorted( conts ,key=cv2.contourArea, reverse=True)

# отрисуем теперь так, чтобы показать, что за сопельки

image_copy2= image.copy()

# Проверяем, что у нас есть контуры (чтобы не сломалось)
if len(conts_sorted)> 0:
    # Проходимся по всем контурам
    for cont_idx , contour in enumerate(conts_sorted):
        # Если размер контура нас удовлетворяет по площади
        if cv2.contourArea(contour) > 100:
            # тут я задаю значения напрямую
            cv2.drawContours(image_copy2, conts_sorted, cont_idx, (0,0,255), 2)
        else:
            # сопельки я покажу синим цветом
            cv2.drawContours(image_copy2, conts_sorted, cont_idx, (255,0,125), 2)

cv2.imshow('contours with sopelkas', image_copy2)

cv2.waitKey(0)

# Мы можем не отрисовывать сопельки
# По сути, всё тоже самое, но без else

# контуры у нас уже отсортированы

image_copy3= image.copy()

# Проверяем, что у нас есть контуры (чтобы не сломалось)
if len(conts_sorted)> 0:
    # Проходимся по всем контурам
    for cont_idx , contour in enumerate(conts_sorted):
        # Если размер контура нас удовлетворяет по площади
        if cv2.contourArea(contour) > 100:
            # тут я задаю значения напрямую
            cv2.drawContours(image_copy3, conts_sorted, cont_idx, (0,0,255), 2)

cv2.imshow('contours without sopelkas', image_copy3)

cv2.waitKey(0)
# Окей, сопелек нет)

cv2.destroyAllWindows()
