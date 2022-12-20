import pandas as pd
def search_hotel(cityname):
    cityname=cityname.upper()
    data_main = pd.read_csv('static/cities.csv', encoding='latin-1', index_col=False)
    data_main["CityName"] = data_main["CityName"].str.upper()
    data1 = pd.concat([data_main['CityName'], data_main['HotelName'], data_main["StarRating"], data_main["HotelAddress"]], axis=1)
    data1.head()
    data1.CityName.nunique()
    

    l = data1["CityName"] == cityname
    type(l)
    l = list(l)
    len(l)

    data2 = data1[l]
    data2 = data2[["CityName", "HotelName", 'HotelAddress', "StarRating"]].drop_duplicates()
    df = data2.sort_values('StarRating', ascending=False).head(10)
    df = df.drop(['CityName'], axis=1)
    return df.head(10)
    # df.columns= ['']*len(df.columns)
    # print(type(df))
    # return render_template("index.html", destination=destination[0], tables=[df.to_html(classes='data', index=False)],
    # titles=df.columns.values)