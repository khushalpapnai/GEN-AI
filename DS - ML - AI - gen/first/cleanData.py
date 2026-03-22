import pandas as pd

if __name__ == "__main__":
    CollMovie = pd.read_csv("collection of movies.csv")

    columns = ["Production Budget ($)","Worldwide Gross ($)"]

    for c in columns:
        CollMovie[c] = CollMovie[c].replace("[\\$,]","",regex=True)
        CollMovie[c] = pd.to_numeric(CollMovie[c])

    CollMovie.to_excel("MoviesCollections.xlsx",index=False )