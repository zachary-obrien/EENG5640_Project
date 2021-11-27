import math

x_1 = 3
x_2 = 5
y_1= 8
y_2= 9

b= 6
f= 4

def disparity(x_1,y_1,x_2,y_2):
    d = math.sqrt(((x_2-x_1)^2)+((y_2-y_1)^2))
    return d

def depth (f,b,d):
    z = (f*b)/d
    return z


d = disparity(x_1,y_1,x_2,y_2)
z = depth(f,b,d)

print(z)
