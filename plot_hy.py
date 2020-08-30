# Import our modules that we are using
import matplotlib.pyplot as plt
import numpy as np

#A = 84372/17405
#B = -1064/295
#q = 49/590
#A=13714008/160205
#B = -30103/3580
#q = -27969/1790
#A = 103.257
#B = 24.12
#q = 6.105
A=55.68
B = -62.8
q = 2.13
print(A,B,q)
# Create the vectors X and Y
x = np.array(range(-10,30))
y = -A/(x+B) + q

fp=open('data.txt','w')
for (x1,y1) in zip(x,y):
    fp.write(str(x1)+' '+str(y1)+'\n')

fp.close()

# Create the plot
plt.plot(x,y)

# Show the plot
plt.show()
