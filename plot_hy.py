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
A= -42.41
B = -60.60
q = 0.48
print(A,B,q)
# Create the vectors X and Y
def hyper(A,B,q, xfrom, xto):
    x = np.array(range(xfrom,xto))
    y = A/(x+B) + q

    fp=open('data.txt','w')
    for (x1,y1) in zip(x,y):
        fp.write(str(x1)+' '+str(y1)+'\n')

    fp.close()

    # Create the plot
    plt.plot(x,y)

    # Show the plot
    plt.show()
hyper(A,B,q,-10,40)

def hyper(A,B,q, Tstart, Tend):
    x = [-i+Tstart for i  in range(0,int(Tstart-Tend+1))]
    B = A/q+Tstart
    y = [A/(i+B) + q for i in x]
    print(A,B,q)

    fp=open('data.txt','w')
    for (x1,y1) in zip(x,y):
        fp.write(str(x1)+' '+str(y1)+'\n')
        print(str(x1)+' '+str(y1)+'\n')

    fp.close()

    # Create the plot
    plt.plot(x,y)

    # Show the plot
    plt.show()
hyper(13381.1, 39.66, -218.045, 21.7, -10)
