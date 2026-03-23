import pandas as pd
import matplotlib.pyplot as pyl
from pandas import DataFrame as dfm

if __name__ =="__main__":
    moviesColl = pd.read_excel("MoviesCollections.xlsx")

    X = dfm(moviesColl,columns = ["Production Budget ($)"] )
    y = dfm(moviesColl,columns = ["Worldwide Gross ($)"])

    pyl.figure(figsize=(12,10))
    pyl.scatter(X,y, alpha=0.4)
    pyl.title("film cost Vs global revenue")
    pyl.xlabel("Production Budget ($)")
    pyl.ylabel("Worldwide Gross ($)")
    pyl.xlim(0,5*10**8)
    pyl.ylim(0,3*10**9)

    pyl.show()
    # print(moviesColl.describe())

