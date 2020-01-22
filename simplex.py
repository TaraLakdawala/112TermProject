import numpy as np

#for this part of the project, I took a lot of help from the following websites:
#https://jeremykun.com/2014/12/01/linear-programming-and-the-simplex-algorithm/
#https://medium.com/@jacob.d.moore1/coding-the-simplex-algorithm-from-scratch-using-python-and-numpy-93e3813e6e70
 
def generateMatrix(variables, constraints):
    # num of variables is num days left
    # constraints are set to be: User achieves goals and suggested net isn't too low
    matrix=np.zeros((constraints+1, variables+constraints+2))
    return matrix

#find and return pivots
def checkRtColPivots(matrix):
    rows,cols=matrix.shape
    rColMin=min(matrix[:1,cols-1])
    if rColMin<0:
        p= np.where(matrix[:-1,cols-1]==rColMin)[0][0]
        return p
    return None

def checkBRowPivots(matrix):
    rows,cols=matrix.shape
    bRowMin=min(matrix[rows-1,:-1])
    if bRowMin<0:
        p=np.where(matrix[rows-1,:-1]==bRowMin)[0][0]
        return p
    return None

# find piv elem in right col
def getPivotLocationRtCol(matrix):
    default=999999999
    L=[]
    p=checkRtColPivots(matrix)
    row=matrix[p,:-1]
    rowMin=min(row)
    colNum=np.where(row==rowMin)[0][0]
    col=matrix[:-1,colNum]
    z=zip(col,matrix[:-1,-1])
    print('entering for loop')
    for i, j in z:
        if i!=0 and j/i>0:
            L.append(j/i)
        else:
            L.append(default)
    ind=L.index(min(L))
    return (ind,colNum)

#find piv elem in bottom row
def getPivotLocationBRow(matrix):
    default=9999999999
    if checkBRowPivots(matrix)!=None:
        L=[]
        a=checkBRowPivots(matrix)
        for i,j in zip(matrix[:-1,a], matrix[:-1,-1]):
            if j/i>0 and i!=0:
                L.append(j/i)
            else:
                L.append(default)
        index=L.index(min(L))
        return (index,a)

def pivot(matrix, row, col):
    pivotRow = matrix[row,:]
    rows,cols=matrix.shape
    table=np.zeros((rows, cols))
    if matrix[row,col]!=0:
        inv=1/matrix[row,col]
        currRow=pivotRow*inv
        for i in range(len(matrix[:,col])):
            k=matrix[i,:]
            c=matrix[i,col]
            if list(k)==list(pivotRow):
                continue
            else:
                table[i,:]=list(k-currRow*c)
        table[row,:]=list(currRow)
        return table
    else:
        return 'can\'t pivot'

def makeVars(matrix):
    rows,cols=matrix.shape
    variableCount=cols-rows-1
    var=[]
    for i in range(variableCount):
        var.append(f'x{i+1}')
    return var
    
def canAddConstraints(matrix):
    rows,cols=matrix.shape
    L=[]
    for i in range(rows):
        if not 0 not in matrix[i,:]:
            L.append(i)
    if len(L)<=1:
        return False
    return True

def addConstraints(matrix, ineq):
    if canAddConstraints(matrix)==True:
        rows, cols=matrix.shape
        numVars=cols-rows-1
        i=0
        while i<rows:
            rowToCheck=matrix[i,:]
            if not 0 not in rowToCheck:
                row=rowToCheck
                break
            i+=1
        for j in range(len(ineq)-1):
            row[j]=ineq[j]
        row[-1]=ineq[-1]
        row[numVars+i]=1
    else:
        print('Cannot add constraint')

def canAddObjective(matrix):
    rows,cols=matrix.shape
    L=[]
    for i in range(rows):
        if not 0 not in matrix[i,:]:
            L.append(i)
    if len(L)!=1:
        return False
    return True

def addObjective(matrix, equation):
    if canAddObjective(matrix)==True:
        rows,cols=matrix.shape
        currRow=matrix[rows-1,:]
        for i in range(len(equation)-1):
            row[i]=equation[i]*-1
        currRow[-2]=1
        currRow[-1]=equation[-1]
    else:
        print('add all constraints first')

def standardizeForMin(matrix):
    matrix[-1,-1]*=-1
    matrix[-1,:-2]*=-1
    return matrix

def minimize(matrix, initialGuess):
    print('standardizing matrix')
    matrix=standardizeForMin(matrix)
    rows,cols=matrix.shape
    print('first while loop')
    while checkRtColPivots==None:
        matrix=pivot(matrix, getPivotLocationRtCol(matrix)[0], getPivotLocationRtCol(matrix)[1])
    print('second while loop')
    while checkBRowPivots==None:
        matrix=pivot(matrix, getPivotLocationBRow(matrix)[0], getPivotLocationBRow(matrix)[1])
    numVars=cols-rows-1
    values={}
    print('entering this for loop')
    for i in range(numVars):
        currCol=matrix[:,i]
        currColSum=sum(currCol)
        currColMax=max(currCol)
        if currColSum==currColMax:
            position=np.where(currCol==currColMax)[0][0]
            values[makeVars(matrix)[i]]=matrix[position,-1]
        else:
            values[makeVars(matrix)[i]]=initialGuess
            values['minimum']=matrix[-1,-1]*-1
    return values

def generateIneq(daysLeft):
    L=[]
    for i in range(daysLeft):
        L.append(-1)
    return L

def initialGuess(daysLeft, calsLeft, matrix):
    vals=makeVars(matrix)
    vals={}
    for i in range(daysLeft):
        vals[f'x{i+1}']=calsLeft/daysLeft
    return vals

def simplex(daysLeft, calsLeft):
    matrix=generateMatrix(daysLeft, 2)
    ineq1=generateIneq(daysLeft)
    ineq1.append(10000)
    addConstraints(matrix, ineq1)
    ineq2=generateIneq(daysLeft)
    ineq2.append(daysLeft*1000)
    addConstraints(matrix, ineq2)
    initialGuess(daysLeft, calsLeft, matrix)
    initGuess=calsLeft/daysLeft
    print('minimizing')
    return (minimize(matrix, initGuess))

