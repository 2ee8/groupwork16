import numpy as np
from sklearn import linear_model
import csv


__authors__ = "Group 16"
__copyright__   = "Copyright 2020, Lanzhou University"
__license__ = "GPL v3.0"
__version__ = "1.0.1"
__maintainer__ = "Group 16"
__email__ = "bfeng18@lzu.edu.cn"
__date__ = "2020/6/24"

"""
This module calculate the regression with the data_collection.py file.
This will print the R square and coffcients to evalute the fitness of the data.
"""

class Regression():
    def __init__(self,dataset):
        self.dataset = dataset
          
    def function_regression(self):
        x = np.array(self.dataset)
        X = x[:,:-1]
        Y = x[:,-1]
        regr = linear_model.LinearRegression()    
        regr.fit(X,Y)
        print("Function coeffcient is" , regr.coef_[0] , 'times ' , regr.coef_[1] ,' distance ' , regr.coef_[2] , ' notes ' )

    def get_R_square(self):
        use_dataset = np.array(self.dataset)
        X = self.dataset[:,:-1]
        Y = self.dataset[:,-1]
        regr = linear_model.LinearRegression()    
        regr.fit(X,Y)
        print(regr.score(X, Y))

def main():
    x = []
    with open('result.csv', 'r') as f:
        reader = csv.reader(f)
    for row in reader:
        a = []
        for i in row:
            a.append(float(i))
        x.append(a)    
    reg = Regression(x)
    reg.function_regression()
    reg.get_R_square()
    
if __name__ == '__main__':
    main()
