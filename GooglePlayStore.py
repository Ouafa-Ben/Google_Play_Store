# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import dataset
df = pd.read_csv("googleplaystore.csv")

# Check the dataset first for any anomalies
print(df.head(5).T)

# # Remove Genres, last Updated, Current Ver and Android Ver
del df["Genres"]
del df["Last Updated"]
del df["Current Ver"]
del df["Android Ver"]

print(df.info())

# Remove Duplicates in App column
# Check for duplicated values
duplicates = df["App"].duplicated().sum()
print("\nThere are {} duplicates in the Apps column".format(duplicates))

# Remove duplicates
duplicates = df.drop_duplicates("App", inplace=True)
print("\nAfter we removed the duplicates we have {}".format(duplicates))

# Check for NULL values
print(df.isna().any())

# Clean dataset
# Remove special characters or replace them if needed then change data type
# Work on App column, remove weird app names and special characters
df = df.drop(df[df["App"] == "#NAME?"].index)
df = df.drop(df[df["App"] == "FP Ð Ð°Ð·Ð±Ð¸Ñ‚Ñ‹Ð¹ Ð´Ð¸ÑÐ¿Ð»ÐµÐ¹"].index)
df["App"] = df.App.str.replace("&", " and ")
df["App"] = df.App.str.replace("[@#$%-*â€ðŸä¹å±‹ç½‘·Â®âœ”ï¸„¢Ã©¥˜]", "", regex=True)

# Drop 1.9 Category
df = df.drop(df[df["Category"] == "1.9"].index)

# Work on Rating column
df["Rating"] = df["Rating"].fillna("0")
# df["Rating"] = df.Rating.str.replace("19", "1.9")
df["Rating"] = df["Rating"].astype(float)

# Work on Reviews column
df["Reviews"] = df.Reviews.str.replace("3.0M", "3000000", regex=True)
df["Reviews"] = df.Reviews.astype(int)

# Work on Size column
df["Size"] = df.Size.replace("Varies with device", np.nan)
df["Size"] = df.Size.str.replace("M", "000")
df["Size"] = df.Size.str.replace("k", "")
df["Size"] = df.Size.replace("1,000+", "1000")
df["Size"] = df["Size"].astype(float)

# Work on Installs column
df["Installs"] = df.Installs.str.replace("+", "", regex=True)
df["Installs"] = df.Installs.str.replace(",", "")
df = df.drop(df[df["Installs"] == "Free"].index)
df["Installs"] = df["Installs"].astype(int)

# Work on Type column
df["Type"] = df["Type"].fillna("0")
df["Type"] = df.Type.str.replace("0", "Free")

# Work on Price column
df["Price"] = df.Price.str.replace("$", "", regex=True)
df["Price"] = df.Price.str.replace("Everyone", "0")
df["Price"] = df.Price.astype(float)
print(df["Price"][4000:4020])

# Work on Content Rating column
df.rename(columns={'Content Rating': 'Content_Rating'}, inplace=True)
df["Content_Rating"] = df.Content_Rating.str.replace("Mature 17+", "Adults 18", regex=True)
df["Content_Rating"] = df.Content_Rating.str.replace("Adults only 18+", "Adults 18", regex=True)

print(df.info())

# End of Data Cleaning
# Start of Data insights
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

# Rating Distribution
rated_apps = df[df["Rating"] != 0]
sns.kdeplot(rated_apps.Rating, color="indianred", fill=True)
plt.title("Distribution of Rating")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.show()

# Categories count
g = sns.catplot(y="Category", data=df, kind="count", order=df["Category"].value_counts().index, palette="GnBu_r").set(title="Top Categories in Google Play Store")
g.set_axis_labels("Number of Apps", "Category")
plt.show()

# Apps Type
total_apps = df["Type"].count()
type_app = df[["App", "Type"]]
grouped_type_app = type_app.groupby("Type")
counted_type_app = grouped_type_app.count()
P_type_app = round(counted_type_app/total_apps*100)
print(P_type_app)

free_paid_data = [92, 8]
labels = ["Free", "Paid"]
color = sns.color_palette("GnBu")
plt.pie(free_paid_data, labels=labels, colors=color, autopct="%.0f%%")
plt.title("Percentage of Free and Paid apps in Google Play Store")
plt.show()

# Content Rating Pie Chart
total_content_rating = df["Content_Rating"].count()
content_rating = df[["App", "Content_Rating"]]
grouped_content_rating = content_rating.groupby("Content_Rating")
counted_content_rating = grouped_content_rating.count()
P_content_rating = round(counted_content_rating/total_content_rating*100)
print(P_content_rating)

P_content_rating = [4, 82, 3, 11]
labels = ["Adults 18+", "Everyone", "Everyone 10+", "Teen"]
color = sns.color_palette("Oranges")
plt.pie(P_content_rating, labels=labels, colors=color, autopct="%.0f%%")
plt.title("Percentage of Apps Content Rating")
plt.show()

# Category vs Reviews
Category_by_reviews = df[["Category", "Reviews"]]
total_reviews = Category_by_reviews["Reviews"].sum()
Category_by_reviews = df.groupby("Category")["Reviews"].sum()
Category_by_reviews = Category_by_reviews/total_reviews * 100
Category_by_reviews = Category_by_reviews.sort_values(ascending=False)
g = sns.barplot(x=Category_by_reviews, y=Category_by_reviews.index, data=df, palette="Blues_r").set(title="Percentage of Reviews per Category")
plt.xlim(0, 100)
plt.show()

# Category vs Rating
g = sns.catplot(x="Category", y="Rating", data=df[df["Rating"] != 0], kind="box", palette="BuGn").set(title="Distribution of Ratings across Categories")
g.despine(left=True)
g.set(xticks=range(0, 33))
g.set_ylabels("Rating")
g.set_xticklabels(rotation=90)
plt.show()

# Category vs Installs
total_num_downloads = df["Installs"].sum()
installed_apps_cat = df[["Category", "Installs"]]
installed_apps_cat_grouped = df.groupby("Category")["Installs"]
installed_apps_cat_counted = installed_apps_cat_grouped.sum()
installed_apps_cat_counted = installed_apps_cat_counted/total_num_downloads * 100
installed_apps_cat_counted = installed_apps_cat_counted.sort_values(ascending=False)
print(installed_apps_cat_counted)
print(total_num_downloads)

# Type vs Installs
total_num_downloads = df["Installs"].sum()
installed_type = df[["Type", "Installs"]]
installed_type_grouped = df.groupby("Type")["Installs"]
installed_type_counted = installed_type_grouped.sum()/total_num_downloads * 100
print(installed_type_counted)

# Find popular categories among paid apps
new_df = df[["Type", "Category"]]
new_df = df[df["Type"] == "Paid"]
g = sns.catplot(y="Category", data=new_df, kind="count", order=new_df["Category"].value_counts().index, palette="RdBu").set(title="Number of Paid Apps in Each Category")
g.set_axis_labels("Number of Paid Apps", "Category")
plt.show()

# Find percentage of installed paid apps categories
new_df = df[["Type", "Category", "Installs"]]
new_df = new_df[new_df["Type"] == "Paid"]
total_installed_cat = new_df["Installs"].sum()
installed_cat = new_df.groupby("Category")["Installs"].sum()
installed_cat = installed_cat/total_installed_cat * 100
installed_cat = installed_cat.sort_values(ascending=False)
g = sns.barplot(x=installed_cat, y=installed_cat.index, data=new_df, palette="BuGn_r").set(title="Percentage of Paid Installed Apps in Each Category")
plt.xlim(0, 100)
plt.show()

# Free and Paid Apps Content rating
new_df = df[["Type", "Content_Rating"]]
new_df = new_df[new_df["Type"] == "Paid"]
palette = "BuPu"
g = sns.catplot(x="Content_Rating", data=new_df, kind="count", order=new_df["Content_Rating"].value_counts().index, palette=palette).set(title="Number of Paid Apps Across Different Content Ratings")
g.set_axis_labels("Content Rating", "Number of Paid Apps")
g.set_xticklabels(rotation=90)
plt.show()

# Paid Apps content rating vs installs
new_df = df[["Type", "Content_Rating", "Installs"]]
new_df = new_df[new_df["Type"] == "Paid"]
total_installed_cat = new_df["Installs"].sum()
grouped_installed_cat = new_df.groupby("Content_Rating")["Installs"]
installed_cat = grouped_installed_cat.sum()
installed_cat = installed_cat/total_installed_cat * 100
installed_cat = installed_cat.sort_values(ascending=False)
color = ["indianred", "lightsalmon", "rosybrown", "darksalmon"]
installed_cat.plot(kind="bar", title="Percentage of Paid Installed Apps in Each Content Rating", color=color)
plt.ylabel("Installed Apps (%)")
plt.ylim(0, 100)
plt.show()

# Find mean, max, min app prices
app_prices_info = df[["App", "Category", "Price"]]
app_prices_info = app_prices_info[app_prices_info["Price"] != 0]
print(app_prices_info["Price"].describe())

# Find everything about the top 10 paid apps
top10_paid_apps = df[df["Type"] == "Paid"]
top10_paid_apps = top10_paid_apps.sort_values(by='Price', ascending=False)
print(top10_paid_apps.head(10))

# END
print("\nThis is my first python project I hope you enjoyed reading my code :)")
# END
