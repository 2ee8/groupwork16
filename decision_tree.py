# -*- coding: utf-8 -*-

__authors__ = "Group 16"
__copyright__   = "Copyright 2020, Lanzhou University"
__license__ = "GPL v3.0"
__version__ = "1.0.1"
__maintainer__ = "Group 16"
__email__ = "bfeng18@lzu.edu.cn"
__date__ = "2020/6/24"


import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt



file = open('result.csv')
filedata = list(csv.reader(file))

def organize_data():#Organize the data, compare the data in the csv file with the average, and replace the data.
    
    for i in range(1,len(filedata)):
        if float(filedata[i][1]) >= 50.6355:
            filedata[i][1] = 'more'
        else:
            filedata[i][1] = 'less'

    for i in range(1,len(filedata)):
        if float(filedata[i][2]) >= 756728:
            filedata[i][2] = 'long'
        else:
            filedata[i][2] = 'short'

    for i in range(1,len(filedata)):
        if float(filedata[i][3]) >= 53.1314:
            filedata[i][3] = 'long'
        else:
            filedata[i][3] = 'short'

    for i in range(1,len(filedata)):
        if float(filedata[i][4]) >= 0.133464:
            filedata[i][4] = "high"
        else:
            filedata[i][4] = "low"

    l1 = l2 = l3 = l4 = []

    for i in range(1,len(filedata)):
        l1.append(filedata[i][1])

    for i in range(1,len(filedata)):
        l2.append(filedata[i][2])

    for i in range(1,len(filedata)):
        l3.append(filedata[i][3])

    for i in range(1,len(filedata)):
        l4.append(filedata[i][4])

    return l1,l2,l3,l4




def createdataset():
    row_data = {'times':l1,
                'Length_of_time':l2,
                'Length_of_comment':l3,
                'fix':l4}
    dataset = pd.DataFrame(row_data)
    return dataset

#Calculate Shannon Entropy
def calent(dataset):
    n = dataset.shape[0]

    iset = dataset.iloc[:,-1].value_counts()
    p = iset/n
    ent = (-p*np.log2(p)).sum()
    return ent

#Choose the best column for segmentation
def bestsplit(dataset):
    baseEnt = calent(dataset)   #Calculate raw entropy
    bestGain = 0    #Initial information gain
    axis = -1    #Initialize the best split column, label column
    for i in range(dataset.shape[1]-1):    #Loop through each column of features
        levels= dataset.iloc[:,i].value_counts().index   #Extract all the values of the current column
        ents = 0
        for j in levels:
            childset = dataset[dataset.iloc[:,i]==j]
            ent = calent(childset)
            ents += (childset.shape[0]/dataset.shape[0])*ent   #Calculate the information entropy of the current column

        infoGain = baseEnt-ents

        if (infoGain > bestGain):
            bestGain = infoGain     #Select maximum information gain   
            axis = i     #The index of the column where the maximum information gain is
    return axis

def mysplit(dataset,axis,value):   #Divide the data set according to the given column
    col = dataset.columns[axis]
    redataset = dataset.loc[dataset[col]==value,:].drop(col,axis=1)
    return redataset


def createtree(dataset):   #Split the data set based on the maximum information gain and construct the decision tree recursively
    featlist = list(dataset.columns)   #Extract all the columns of the data set
    classlist = dataset.iloc[:,-1].value_counts()

    if classlist[0]==dataset.shape[0] or dataset.shape[1] == 1:
        return classlist.index[0]
    axis = bestsplit(dataset)       #Determine the index of the current best split column
    bestfeat = featlist[axis]       #Get the features corresponding to the index
    mytree = {bestfeat:{}}          #Store the information of the tree in the way of dictionary nesting
    del featlist[axis]
    valuelist = set(dataset.iloc[:,axis])       #Extract all attribute values of the best segmented column
    for value in valuelist:         #Recursively build each attribute value
        mytree[bestfeat][value] = createtree(mysplit(dataset,axis,value))
    return mytree

def getnumleafs(mytree):  #Number of leaf nodes in initialization tree
    numleafs = 0
    firststr = list(mytree.keys())[0]
    seconddict = mytree[firststrfor key in seconddict.keys():    #Determine whether the key is a dictionary, the key name 1 and its value form a dictionary, if it is a dictionary, continue to traverse through recursion, looking for leaf nodes
                        
        if type(seconddict[key]).__name__ == 'dict':
            numleafs += getnumleafs(seconddict[key])  
        else:
            numleafs += 1   #If it is not a dictionary, the number of leaf nodes is increased by 1.
    return numleafs


def gettreedepth(mytree):
    #Initialization tree depth
    maxdepth = 0
    #Get the first key name of the tree
    firststr = list(mytree.keys())[0]
    #Get the value corresponding to the key name
    seconddict = mytree[firststr]
    for key in seconddict.keys():
        #If the obtained key is a dictionary, the depth of the tree is increased by 1.
        if type(seconddict[key]).__name__ == 'dict':
            thisdepth = 1 + gettreedepth(seconddict[key])
        else:
            thisdepth = 1
        if thisdepth > maxdepth:
            maxdepth = thisdepth
    return maxdepth


decisionnode = dict(boxstyle = "sawtooth",fc="0.8")
leafnode = dict(boxstyle = "round4",fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotnode(nodetxt,centerpt,parentpt,nodetype):
    """
    nodetxt is to add a comment to the data point xy, xy is the starting point of the data point, located in the middle of the node
    xycoords sets the coordinate type of the specified point xy, xytext is the coordinate of the middle point of the annotation, and textcoords sets the coordinate style of the annotation point
    bbox sets the style of the annotation box, and arrowprops sets the style of the arrow
    """
    createplot.ax1.annotate(nodetxt, xy=parentpt,\
                            xycoords = 'axes fraction', xytext = centerpt, textcoords = 'axes fraction',\
                                                                va = "center", ha = "center", bbox = nodetype, arrowprops = arrow_args)
#Draw the text in the middle of the line
def plotmidtext(cntrpt, parentpt, txtstring):


    
    xmid = (parentpt[0] - cntrpt[0]) / 2.0 + cntrpt[0]

    ymid = (parentpt[1] - cntrpt[1]) / 2.0 + cntrpt[1]
    createplot.ax1.text(xmid, ymid, txtstring)


#Draw tree
def plottree(mytree,parentpt,nodetxt):
    #Get the leaf nodes of the tree
    numleafs = getnumleafs(mytree)
    #Get the depth of the tree
    depth = gettreedepth(mytree)
    firststr = (mytree.keys())[0]
    #Calculate the coordinates of child nodes
    cntrpt = (plottree.xoff + (1.0 + float(numleafs)) / 2.0 / plottree.totalW, \
              plottree.yoff)
    #Draw text on line
    plotmidtext(cntrpt, parentpt, nodetxt)
    #Draw node
    plotnode(firststr, cntrpt, parentpt, decisionnode)
    seconddict = mytree[firststr]
    #According to the depth of the tree, calculate the offset of the node in the y direction
    plottree.yoff = plottree.yoff - 1.0 / plottree.totald
    for key in seconddict.keys():
        if type(seconddict[key]).__name__ == 'dict':
            #Draw tree recursively
            plottree(seconddict[key], cntrpt, str(key))
        else:
            plottree.xoff = plottree.xoff + 1.0 / plottree.totalW
            #Draw non-leaf nodes
            plotnode(seconddict[key], (plottree.xoff, plottree.yoff), \
                     cntrpt, leafnode)
            #Draw the sign on the arrow
            plotmidtext((plottree.xoff, plottree.yoff), cntrpt, str(key))
    plottree.yoff = plottree.yoff + 1.0 / plottree.totald

#Draw decision tree
def createplot(intree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[],yticks=[])

     '''
     Create a figure with 1 row and 1 column,and return the Axes instance of the first figure
     in the grid to ax1 as the attribute of the function createPlot().
     This attribute ax1 is equivalent to a global variable and can be used by the plotNode function
     '''
    createplot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plottree.totalW = float(getnumleafs(intree))
    #Get the depth of the tree
    plottree.totald = float(gettreedepth(intree))
   
      '''
      The x-axis offset of the node is -1/plottree.totlaW/2, 1 is the length of the x-axis,
      divided by 2 to ensure that the distance between the x-axis of each node is
      1/plottree.totlaW*2 plottree.xoff = -0.5/plottree.totalW plottree.yoff = 1.0
      '''
    plottree.xoff = -0.5/plottree.totalW
    plottree.yoff = 1.0
    plottree(intree,(0.5,1.0),'')
    plt.show()


if __name__ == "__main__":
    l1,l2,l3,l4 = organize_data()
    dataset = createdataset()
    mytree = createtree(dataset)
    ent = calent(dataset)
    x = gettreedepth(mytree)
    numleafs = getnumleafs(mytree)
    createplot(mytree)





