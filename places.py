import pandas as pd
def search_places(cityname):
    data = pd.read_csv("static/Review_db.csv", encoding='latin-1')
    data["City"] = data["City"].str.upper()
    # cityname = "ghaziabad".upper()
    cityname = cityname.upper()

    l = data["City"] == cityname
    data = data[list(l)]
    df = data.groupby(['Place', 'Rating']).sum().reset_index().groupby('Place').mean().round(0).sort_values('Rating',
                                                                                                            ascending=False)
    df.columns = [''] * len(df.columns)
    if len(df) != 0:
        return (df.head(20))
    else:
        print("Sorry this city is not present in our database")