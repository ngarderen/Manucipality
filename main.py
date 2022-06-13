
import pandas as pd
import matplotlib.pyplot as plt

tables = pd.read_html("https://github.com/WincAcademy/practice_data/blob/main/data/geo/provinces.csv")
countries = tables[0]

data = countries.loc[:, ["province", "inhabitants", "surface_sq_km"]]
data2 = data.loc[data["province"] == "Friesland"]
list_pro_density = []  # lijst density per provincie

for index, row in data.iterrows():
    density = round(row["inhabitants"] / row["surface_sq_km"])
    list_pro_density.append(density)

data.insert(loc=2, column="pro_density", value=list_pro_density)
pro_df = data.drop(columns=['inhabitants', 'surface_sq_km'])
pro_df.columns = ["pro", "pro_density"]

# aantal inwonders / oppervlakte
# density of 195 people per square kilometer

provincie_data = []
provincies = pro_df["pro"]

for x in provincies:
    data = pd.read_html(f"https://github.com/WincAcademy/practice_data/blob/main/data/geo/municipalities/{x.lower()}.csv")
    provincie_data.append(data[0])

all_rovincie = pd.concat(provincie_data)
all_rovincie = all_rovincie.drop(columns=['Unnamed: 0', "CBS code"])
all_rovincie.columns = ["mun", "pro", "pop", "surface"]
list_mun_density = []

for index, row in all_rovincie.iterrows():
    density = round(row["pop"] / row["surface"])
    list_mun_density.append(density)

all_rovincie.insert(loc=1, column="mun_density", value=list_mun_density)
all_rovincie = all_rovincie.drop(columns=['pop', "surface"])

new_list = []

for index, row in all_rovincie.iterrows():
    pro = row["pro"]
    for index, row2 in pro_df.iterrows():
        if row2["pro"] == pro:
            new_list.append(row2["pro_density"])

all_rovincie.insert(loc=3, column="pro_density", value=new_list)

relative_density_list = []

for index, row in all_rovincie.iterrows():
    relative_density = round(row["mun_density"] / row["pro_density"], 2)
    relative_density_list.append(relative_density)

all_rovincie.insert(loc=4, column="relative_density", value=relative_density_list)
top_10_mun = all_rovincie.sort_values(by=['relative_density'], ascending=False).head(10)
print(top_10_mun)


fig, ax = plt.subplots()
ax.invert_yaxis()
ax.set_xlabel('Relative Density')  # horizontaal label
ax.set_ylabel('municipalities')  # verticaal label
ax.xaxis.grid()
plt.tight_layout()
ax.set_title('municipalities relative density')

mun = top_10_mun.loc[:, "mun"]
relative_data = top_10_mun.loc[:, "relative_density"]

ax.barh(mun, relative_data)
plt.show()