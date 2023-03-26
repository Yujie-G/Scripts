import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_excel(io='D:\A-WORKS\个人荣誉材料\前五学期学分绩\GPA.xlsx', header=None)


def Convert2GPA(score):
    if score >= 90:
        s4 = 4
    elif score >= 85:
        s4 = 3.7
    elif score >= 82:
        s4 = 3.3
    elif score >= 78:
        s4 = 3.0
    elif score >= 75:
        s4 = 2.7
    elif score >= 72:
        s4 = 2.3
    elif score >= 68:
        s4 = 2.0
    elif score >= 64:
        s4 = 1.5
    return s4


GPAhis = []
ABCDHis = []
sumHis_abcd = []
sumHis_all = []

allSum = 0
ABCDsum = 0

ABCDScore = 0
gpa = 0

curTerm_allClass = []
curTerm_abcd = []
prev = 1

for i in range(data.shape[0]):
    term = int(data.iloc[i, 0][-1])
    Type = data.iloc[i, 1][0:4]
    value = float(data.iloc[i, 5])
    name = data.iloc[i,3]

    # is pass_or_no class
    try:
        score = float(data.iloc[i, 6])
    except:
        continue
    # new term
    if(term != prev):
        GPAhis.append(curTerm_allClass)
        ABCDHis.append(curTerm_abcd)
        curTerm_allClass = []
        curTerm_abcd = []
        prev = term
        sumHis_abcd.append(ABCDsum)
        sumHis_all.append(allSum)
        print(f"cur credit at term{term} : {allSum}, ABCD sum: {ABCDsum}")
    allSum += value

    # gpa convert
    s4 = Convert2GPA(score)
    gpa += s4*value
    curTerm_allClass.append(gpa/allSum)

    if Type != 'UPEC':
        # print(name,' ',value,' ',score)
        ABCDsum += value
        ABCDScore += score*value
        curTerm_abcd.append(ABCDScore/ABCDsum)
    # ABCDsum += value
    # ABCDScore += score*value
    # curTerm_abcd.append(ABCDScore/ABCDsum)

GPAhis.append(curTerm_allClass)
ABCDHis.append(curTerm_abcd)
sumHis_abcd.append(ABCDsum)
sumHis_all.append(allSum)
print(f"cur credit at term{term} : {allSum}, ABCD sum: {ABCDsum}")



cm = ['r','b','g','y','']
curGPA = GPAhis[-1][-1]
curScore = ABCDHis[-1][-1]


plt.figure(1)
print('curGPA: ',curGPA)
plt.title(f'gpa history, curGPA={curGPA:.2f}')
plt.ylim(3,4)
x=[]
y=[]
xpos=0
for term in GPAhis:
    xpos+=len(term)
    x.append(xpos)
    y.append(term[-1])
plt.plot(x,y,marker = "o",markersize=8,linestyle='--',linewidth=2)
for i in range(len(GPAhis)):
    if(i==0): xx = np.arange(1,x[i]+1)
    else: xx = np.arange(x[i-1]+1,x[i]+1)
    plt.plot(xx,GPAhis[i],c=cm[i],label=f'term: {i+1}',marker = "+",markersize=8)
plt.xlim(0, xpos+2)


# DRAW ABCD SCORE
plt.figure(2)
plt.ylim(80,100)
print('curScore: ',curScore)
plt.title(f'ABCD history, curScore={curScore:.2f}')
x=[]
y=[]
yy=[]
xpos=0;prev=0
for i in range(len(ABCDHis)):
    term = ABCDHis[i]
    print(f"Total score add {term[-1]-prev:.2f} , compare to last term: {prev:.2f}",end=';')
    prev = term[-1]
    xpos+=len(term)
    x.append(xpos)
    y.append(term[-1])
    sc1 = term[-1]*sumHis_abcd[i]
    sc0 = 0
    if(i>0): sc0 = ABCDHis[i-1][-1]*sumHis_abcd[i-1]
    ans = sc1/sumHis_abcd[i]
    if(i>0):
        ans = (sc1-sc0)/(sumHis_abcd[i]-sumHis_abcd[i-1])
    print(f"score at this term is {ans:.2f}")
    yy.append(ans)

# draw end point
plt.plot(x,y,marker = "o",markersize=8,linestyle='--',linewidth=2)
plt.bar(x,yy,color='orange')

#draw each class
for i in range(len(ABCDHis)):
    if(i==0): xx = np.arange(1,x[i]+1)
    else: xx = np.arange(x[i-1]+1,x[i]+1)
    plt.plot(xx,ABCDHis[i],c=cm[i],label=f'term{i+1}',marker = "+",markersize=8)


plt.xlim(0, xpos+2)

# draw range line
xx = np.linspace(0, xpos+10, 1000)
y1 = 90*np.ones(xx.shape)
y2 = 85*np.ones(xx.shape)
plt.fill_between(xx, y1,y2, color='dodgerblue', alpha=0.3)

plt.show()

