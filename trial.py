import os
from PIL import Image, ImageDraw
import random
import math
import numpy as np
import time

class circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.growing = 1

    def draw(self, img, color=255):
        draw = ImageDraw.Draw(img)
        top_x = self.x-self.r
        top_y = self.y-self.r
        down_x = self.x+self.r
        down_y = self.y+self.r
        draw.ellipse((top_x, top_y, down_x, down_y), fill=(0), outline=(0))

time1 = time.time()  # note initial time

# Reference- https://ehmatthes.github.io/pcc_2e/beyond_pcc/pillow/
image = Image.open("pics/horse.jpg").convert("L")
pixel_map = image.load()#this is inverted, kindof weird
width, height = image.size
hist = image.histogram()

# Creating a list that contains all the pixels corresponding   
pixels=np.asarray(image)
histogram_list=[]
for i in range(256):
	result=np.where(pixels==i)
	histogram_list.append(list(zip(result[0],result[1])))
	print("hi",i)
x = int( histogram_list[20][20][0])
y = int (histogram_list[20][20][1])
print(histogram_list[20][20], ",",pixel_map[y,x])

circles_matrix=np.full((height,width),-1,dtype=float)

blank_image = Image.new("L", (width, height), color=255)
pixel_map2 = blank_image.load()
print("Blank : ", blank_image.format, blank_image.size, blank_image.mode)

# print(histogram_list[20][0])
# print(np.where(histogram_list[20]==(90,555)))
# x=100
# y=100
# circles_matrix[75][100]=20
# circles_matrix[90][139]=40
# circles_matrix[129][60]=10
# rect = np.copy(circles_matrix[(x-50, 0)[x-50 > 0]:(x+50, width-1)
#                               [x+50 < width], (y-50, 0)[y-50 > 0]:(y+50, height-1)[y+50 < height]])
# result = np.where(rect > -1)
# check = list(zip(result[0], result[1]))
# if not check:
# 		pass
# else:
# 	for res in check:
# 		i = int(res[0])
# 		j = int(res[1])
# 		print(f"{i},{j}-{circles_matrix[i][j]}")

failed_attempts = -1
num = 0
space = 0  # space between circles
color = 0
single_fail = 0
radius = color//20 + 13

attempts = (len(histogram_list[color])//1,
            0)[len(histogram_list[color]) > 0]
# attempts = ((3000, 1000)[len(histogram_list[color]) > 3000], 500)[len(histogram_list[color]) > 1000]


while color <250:
	if failed_attempts > 100:
		failed_attempts=0
		color += 1
		radius=color//20 + 13
	if not histogram_list[color]: #skipping if no pixel of that color exists
		color += 1
		radius=color//20 + 13
		continue
	x,y = random.choice(histogram_list[color])
	r = pixel_map[int(y), int(x)]/20
	found_space = True
	# checking if x,y is inside any other circle
	rect = np.copy(circles_matrix[(x-radius, 0)[x-radius > 0]:(x+radius, width-1)[x+radius < width], (y-radius, 0)[y-radius > 0]:(y+radius, height-1)[y+radius < height]])
	result = np.where(rect > -1)
	check = list(zip(result[0], result[1]))
	if not check:
		pass
	else:
		for res in check:
			i = int(res[0])
			j = int(res[1])
			if math.sqrt((x - i)**2 + (y - j)**2) < circles_matrix[i][j] + r:
				# print(f"{x},{y}-{r}vs{i},{j}-{circles_matrix[i][j]}")
				found_space = False
				break

	if not found_space:
		failed_attempts += 1
		continue
	else:
		circles_matrix[x][y]= float(r)
		print(num," , Color =",color)
		num += 1

np.save("results/res",circles_matrix)
print((time.time()-time1)/60, "min")
print("No.Circes:", num)
for i in range(width):
	for j in range(height):
		if circles_matrix[j][i]>-1:
			pixel_map2[i,j] = 0

blank_image.show()
blank_image.save(f"results/horsenew2.jpeg")
