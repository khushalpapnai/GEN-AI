import pandas as pd
import matplotlib.pyplot as pyl
from pandas import DataFrame as dfm
from sklearn.linear_model import LinearRegression as LR

if __name__ =="__main__":
    reg = LR()
    moviesColl = pd.read_excel("MoviesCollections.xlsx")

    X = dfm(moviesColl,columns = ["Production Budget ($)"] )
    y = dfm(moviesColl,columns = ["Worldwide Gross ($)"])

    # from linear regression using fit for predict
    reg.fit(X,y)

    # # slope coefficient
    # coef = reg.coef_
    # print(coef)
    #
    # intercept = reg.intercept_
    # print(intercept)

    print(moviesColl.describe())
    pyl.figure(figsize=(12,10))
    pyl.scatter(X,y, alpha=0.4)
    pyl.title("film cost Vs global revenue")
    pyl.xlabel("Production Budget ($)")
    pyl.ylabel("Worldwide Gross ($)")
    pyl.xlim(0,5*10**8)
    pyl.ylim(0,3*10**9)

    pyl.plot(X,reg.predict(X),color = 'green',linewidth = 2)

    # score define how much our prediction is closer to actual
    print(reg.score(X,y))
    pyl.show()






