"""-------------------------------------------------------------------------------------
#Idea:---------------------------------------------------------------------------
My idea to solve sudoku is very direct and I believe also very effective: First to fill
the most “urgent” blanks, and solve the “easy” blanks later.
#Details:---------------------------------------------------------------------------
How do I define “urgent” and “easy”? The urgent blanks are those which do not
have many choices to choose, which means that its “brothers” have many fixed
numbers but not void blanks (or zero). And a blank’s brother, by the way, is other
blanks in its row, columns and the same sub-box. So, if a blank’s brothers have too
many fixed numbers but not void blanks, it could be very dangerous if you decide to
solve this blank later, because its only choice(s) may be taken by its brothers, then this
solution is failed, you have to do it again.
So in the beginning, we should calculate the choices and the number of choices
(Priority) for each void blank in the sudoku matrix, and store it to matrix C(choices)
and P(priority). So actually matrix C is a 3D(x,y,z) array, (x,y) stands for the location
of blank, and z stands for the choices that the blank have now.
Then find the minimum value in matrix P, whose coordinate stands for the most
urgent blank. And choose a number from its choices in matrix C to fill in the blank.
Then the most important part, to modify the current blank’s brothers’ choices in
matrix P and C: if the currently filled number also is included by its brother’s choices,
delete it from its choices and make the number of choices minus 1.
Then again, find the minimal value in matrix P (the second urgent one), fill in
numbers and modify its brother’s choices until there is no blanks.
#Advantages:---------------------------------------------------------------------------
I believe by using this method, we can solve the sudoku by only one try, though I
am not able to prove it in mathematics. This makes sense somehow, because every time
the solver tries to fill the blank which has only one choice, and as the solving going on,
unfilled blanks’ choice become less and less to 1, if it becomes 0, you don’t have to go
back and refill some blanks, because these blanks also have only one choice. So if one
blank’s choice becomes nothing, it means this puzzle can’t be solved.
------------------------------------------------------------------------------------------"""
import numpy as np
from time import time
import math as mt
import random as rdm

m4=np.loadtxt("4-4.txt")
m9=np.loadtxt("9-9.txt")
m16=np.loadtxt("16-16.txt")

def avlnum(m,x,y,l=0):
    if not l:
        l=len(m)
    size=int(mt.sqrt(l))
    xhead=int(x/size)*size
    yhead=int(y/size)*size
    boxset=set(np.unique(m[xhead:xhead+size,yhead:yhead+size]))
    xset=set(np.unique(m[x,:]))
    yset=set(np.unique(m[:,y]))
    nums=set([x for x in range(1,l+1)])
    nums=list(nums-boxset-xset-yset)
    return nums
  
def mod(m,prio,choices,l=0):
    for i in range(l):
        for j in range(l):
            if m[i,j]!=0:
                prio[i,j],choices[i][j]=l+1,0
            else:
                num=avlnum(m,i,j,l)
                prio[i,j],choices[i][j]=len(num),num
    
def solver(square_matrix):
    om=square_matrix
    m=square_matrix.tolist()
    m=np.array(m)
    l=len(m)
    prio=np.zeros([l,l])
    choices=np.zeros([l,l]).tolist()
    for i in range(l):
        for j in range(l):
            if m[i,j]!=0:
                prio[i,j],choices[i][j]=l+1,0
            else:
                num=avlnum(om,i,j,l)
                prio[i,j],choices[i][j]=len(num),num
    while (0 in m):
        c=prio.argmin()
        x=int(c/l);y=c%l
        m[x,y]=choices[x][y][rdm.randint(0,len(choices[x][y]))-1]
        mod(m,prio,choices,l)
    return m
m=solver(m4)
