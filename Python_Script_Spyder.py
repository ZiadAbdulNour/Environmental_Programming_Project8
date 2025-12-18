import pickle
import numpy as np
import pandas as pd
import geopandas as gpd
from pathlib import Path
import matplotlib
matplotlib.use("TkAgg") # Graphics error so use this here is spyder to ploy
import matplotlib.pyplot as plt

####### OPENING PATH AND READING FILES: #######
DATA_PATH = Path.cwd() / "Data" # [20] A general path to use for all devices, and to not encounter problems.
path_lfe = DATA_PATH / "ds_lfe_percountry.pkl" 
path_le = DATA_PATH / "ds_le_percountry.pkl"
PATH_GDF = DATA_PATH / "gdf_country_borders.pkl"

with open(path_lfe, "rb") as f:  # [8] rb because pickles reads bytes not texts.
    ds_lfe = pickle.load(f)     
with open(path_le, "rb") as f: 
    ds_le = pickle.load(f)
with open(PATH_GDF, "rb") as f: 
    gdf = pickle.load(f) 

# At this stage, gdf is just a generic object from the pickle file, not yet ready for spatial analysis or merging.
gdf = gpd.GeoDataFrame(gdf, geometry="geometry") # [11] Ensures the geometry column is called geometry. Without this step, spatial plotting and geospatial operations may fail or behave unpredictably.
gdf = gdf.reset_index()  # [12] Move country names from index to column to be able to use in a table.

# In the original dataset, country identifiers were stored in the index. Resetting the index moves them into a regular column. 
# This step ensures there is always a column called country, which is essential because all merges are performed using on="country".
if "name" in gdf.columns:
    gdf = gdf.rename(columns={"name": "country"})
elif "index" in gdf.columns:
    gdf = gdf.rename(columns={"index": "country"})


####### DEFINING YEARS THAT WE WILL USE: #######
years = 1960 + ds_lfe["time_ind"].values # [9] Convert it from an xarray object into a NumPy array because plotting operate on numerical arrays not on labeled data structures.
birth_years = ds_le["birth_year"].values 


####### ALL FUNCTIONS FOR THE OUTPUTS, TASK 3-6-8-9-10-11 #######
def plot_annual_land_fraction(ds, country): # Function with dataset ds, and country to be called.
    ds_c = ds.sel(country=country) # [3] Sel for selecting by label, not by index (e.g Belgium not 2).
    plt.figure(figsize=(8,5))
    # Define scenarios to use variables from: (mean variable, std variable, label).
    scenarios = [("mmm_15_sm", "std_15_sm", "1.5°C"), ("mmm_20_sm", "std_20_sm", "2°C"), ("mmm_NDC_sm", "std_NDC_sm", "NDC"),]
    for mean_var, std_var, label in scenarios:
        m = ds_c[mean_var].values
        s = ds_c[std_var].values 
        plt.plot(years, m, label=label)
        plt.fill_between(years, m-s, m+s, alpha=0.3) # [11] Helped us fill the Fill the area between two curves, for the uncertainty bounds (m-s, m+s).
    plt.xlabel("Year")
    plt.ylabel("Land fraction exposed (%)")
    plt.title(f"Annual land fraction exposed to heatwaves – {country}") 
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

    
def plot_lifetime_exposure(ds, country): # Function with dataset ds, and country to be called.
    ds_c = ds.sel(country=country) # [3] Sel for selecting by label, not by index (e.g Belgium not 2).
    plt.figure(figsize=(8,5))
    # Define scenarios to use variables from: (mean variable, std variable, label).
    scenarios = [("mmm_15", "std_15", "1.5°C"), ("mmm_20", "std_20", "2°C"), ("mmm_NDC", "std_NDC", "NDC"),]
    for mean_var, std_var, label in scenarios:
        m = ds_c[mean_var].values 
        s = ds_c[std_var].values 
        plt.plot(birth_years, m, label=label)
        plt.fill_between(birth_years, m-s, m+s, alpha=0.3) # [11] Helped us fill the Fill the area between two curves, for the uncertainty bounds (m-s, m+s).  
    plt.xlabel("Birth Year")
    plt.ylabel("Lifetime exposure to heatwaves")
    plt.title(f"Lifetime exposure to heatwaves – {country}")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

    
def plot_lifetime_exposure_map_with_annotations(ds_le):     
    ds_2020 = ds_le.sel(birth_year=2020) # [3] Select birth cohort 2020 in the NDC scenario
    le_mmm = ds_2020["mmm_NDC"]
    le_std = ds_2020["std_NDC"]
    
    df_le = le_mmm.to_dataframe(name="mmm").reset_index() # [12] Dataframes are better for merging, tables and other simple representations
    df_le["std"] = le_std.to_dataframe(name="std").reset_index()["std"]
    gdf_plot = gdf.merge(df_le, on="country", how="left") # [18] Merging combines two datasets based on a shared key (e.g country name), allowing attributes from different sources to be joined into a single table
    
    gdf_plot["mmm_frac"] = gdf_plot["mmm"] / 100.0  # Convert to fractions 
    gdf_plot["std_frac"] = gdf_plot["std"] / 100.0
    
    #Then select to 5 countries according to mmm values and plot them on the map
    top5 = (df_le.sort_values("mmm", ascending=False).head(5)["country"].tolist()) # [14] Sort the values to determine top 5 and convert series to list

    countries_to_annotate = top5 + ["Belgium"]
    annot_df = gdf_plot[gdf_plot["country"].isin(countries_to_annotate)] # [19] Subset GeoDataFrame for annotations filters rows by checking whether values belong to a given list, which is useful for selecting a subset of countries.

    fig, ax = plt.subplots(figsize=(14, 8))

    gdf_plot.plot(column="mmm_frac", cmap="Reds", linewidth=0.3, edgecolor="black", legend=True, ax=ax)
    ax.set_title("Lifetime Exposure to Heatwaves\nBirth cohort 2020 – NDC scenario", fontsize=14)
    ax.axis("off")

    # Put any offset to change box location on the map (Belgium and the 5 other)
    offsets = {"Belgium": (10, 10), top5[0]: (-20, 15), top5[1]: (-25, -40), top5[2]: (-25, -30), top5[3]: (-50, -40), top5[4]: (-30, 30),}

    for _, row in annot_df.iterrows(): # [20] An AI-based assistant was consulted to better understand annotation, logic and layout were adjusted manually.
        if row.geometry is None:
            continue
        x, y = row.geometry.centroid.x, row.geometry.centroid.y
        dx, dy = offsets.get(row["country"], (15, 15))

        ci_low  = row["mmm"] - 1.96 * row["std"] # 95% of values lie within +-1.96 standard deviations
        ci_high = row["mmm"] + 1.96 * row["std"]

        label = (f"{row['country']}\n" f"mmm = {row['mmm']:.1f}\n" f"95% CI: [{ci_low:.1f}, {ci_high:.1f}]")
        ax.annotate(label, xy=(x, y), xytext=(x + dx, y + dy), arrowprops=dict(arrowstyle="->", lw=1), bbox=dict(boxstyle="round", fc="white", ec="black"), fontsize=9)
    plt.show()

    
def plot_scenario_difference_maps_2020(ds_le, gdf): # gdf denotes the Geodataframe containing country geometries, which is merged with scenario-based exposure differences to enable spatial visualization
    ds_2020 = ds_le.sel(birth_year=2020) # [3] Selection of birth cohort 2020
    df_diff = ds_2020[["mmm_15", "mmm_20", "mmm_NDC"]].to_dataframe().reset_index() # [12] Dataframes are better for merging, tables and other simple representations

    # Compute differences between heatwaves
    df_diff["add_20_vs_15"]  = df_diff["mmm_20"]  - df_diff["mmm_15"]
    df_diff["add_NDC_vs_15"] = df_diff["mmm_NDC"] - df_diff["mmm_15"]
    df_diff["add_NDC_vs_20"] = df_diff["mmm_NDC"] - df_diff["mmm_20"]

    gdf_diff = gdf.merge(df_diff, on="country", how="left")  # [18] Merge computed difference with country geometries  

    maps = {"add_20_vs_15": "Additional lifetime heatwaves (2°C − 1.5°C)", "add_NDC_vs_15": "Additional lifetime heatwaves (NDC − 1.5°C)", "add_NDC_vs_20": "Additional lifetime heatwaves (NDC − 2°C)",}

    fig, axes = plt.subplots(1, 3, figsize=(19, 4)) 

    for ax, (col, title) in zip(axes, maps.items()):
        gdf_diff.plot(column=col, cmap="Reds", legend=True, ax=ax, edgecolor="black", linewidth=0.2)
        ax.set_title(title, fontsize=12)
        ax.axis("off")
    
    plt.suptitle("Additional lifetime heatwaves for birth cohort 2020\nDifferences between emission scenarios", fontsize=14)
    plt.show()


def plot_top10_countries_bar_2020(ds_le):
    ds_2020 = ds_le.sel(birth_year=2020)    # [3] Selection of birth cohort 2020
    df_2020 = (ds_2020["mmm_NDC"].to_dataframe(name="mmm").reset_index()) # [12] Dataframes are better for merging, tables and other simple representations

    #Then select to 10 countries according to mmm values and plot them on the map
    top10 = (df_2020.sort_values("mmm", ascending=False).head(10)) # [14] Sort the values to determine top 5, no need for list here like before

    fig, ax = plt.subplots(figsize=(10, 6)) 
    ax.barh(top10["country"],top10["mmm"],color="coral")

    ax.set_xlabel("Lifetime number of heatwaves (mmm)")
    ax.set_ylabel("Country")
    ax.set_title("Top 10 countries by lifetime heatwave exposure\nBirth cohort 2020 – NDC scenario", fontsize=14)
    ax.invert_yaxis()    # Show highest value on top
    plt.tight_layout()
    plt.show()


def plot_generational_difference_map(ds_le, gdf):
    ds_2020 = ds_le.sel(birth_year=2020) # [3] To select thee data for the year we wan
    ds_1960 = ds_le.sel(birth_year=1960) 

    dfs = {}
    for year, ds in zip([2020, 1960], [ds_2020, ds_1960]):
        df = ds["mmm_NDC"].to_dataframe().reset_index()
        df = df.rename(columns={"mmm_NDC": f"mmm_{year}"})
        dfs[year] = df

    df_2020 = dfs[2020]
    df_1960 = dfs[1960]

    df_gen = df_2020.merge(df_1960, on="country") # [18] Merge the two dataframes using country
    df_gen["diff_2020_1960"] = df_gen["mmm_2020"] - df_gen["mmm_1960"] # Calculate the difference between generations
    gdf_gen = gdf.merge(df_gen, on="country", how="left") # [18] Merge with the world map data

    fig, ax = plt.subplots(figsize=(14, 7))
    gdf_gen.plot(column="diff_2020_1960", cmap="Reds", legend=True, ax=ax, edgecolor="black", linewidth=0.2) # [17] Geodataframe plot
    ax.set_title("Increase in lifetime heatwave exposure\n" "Children born in 2020 vs grandparents born in 1960 (NDC scenario)")
    plt.show()


####### CALLING ALL FUNCTIONS TO GET OUTPUTS #######
for c in ["Belgium", "China", "Nigeria", "Germany", "Ethiopia", "Lebanon"]: # Plotted some additional countries, but compared the needed ones
    plot_annual_land_fraction(ds_lfe, c)
    
for c in ["Belgium", "China", "Nigeria", "Germany", "Ethiopia", "Lebanon"]:
    plot_lifetime_exposure(ds_le, c)

plot_lifetime_exposure_map_with_annotations(ds_le)

plot_scenario_difference_maps_2020(ds_le, gdf)

plot_top10_countries_bar_2020(ds_le)

plot_generational_difference_map(ds_le, gdf)