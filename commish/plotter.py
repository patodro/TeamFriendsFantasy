import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
import os, sys, glob

# read in payouts as dataFrame
df = pd.read_csv("payouts.csv")

# Function to calculate net values for a year
def calculate_net_values(row):
    net_values = {}
    for column in row.index:
        if column not in ['Year', 'Buy-in']:
            if pd.notna(row[column]):
                net_values[column] = row[column] - row['Buy-in']
            else:
                net_values[column] = np.nan
    return net_values

# Calculate the net values for each year
net_values_list = df.apply(lambda row: calculate_net_values(row), axis=1)

net_values_df = pd.DataFrame(net_values_list.tolist())
net_values_df.insert(0, 'Year', df['Year'])

# Compute the cumulative sum for each manager
df_netcum = net_values_df.set_index('Year').cumsum().reset_index()
# forward-fill NaN values to persist the last known value
df_netcum.fillna(method='ffill', inplace=True)

# Melt the DataFrame to a long format
df_melt = df_netcum.melt(id_vars=["Year"], var_name="Name", value_name="Value")
#filter out rows where Name column is NaN
df_melt = df_melt.dropna(subset=['Name'])

# separate out buy-in data
otherDF = df_melt[df_melt["Name"] != "Buy-in"]

# setup plotly template
pay_templ = pio.templates["plotly_dark"]
fig = px.line(otherDF, x="Year", y="Value", color="Name", template=pay_templ)

#export plot to html
pio.write_html(fig, file='NetEarnings.html', auto_open=True)

# Generate HTML string to embed in a webpage
html_str = pio.to_html(fig, include_plotlyjs='cdn')

print("Generating HTML snippet for embedding NetEarnings graph...")
# Save HTML string to a file (for embedding)
with open('plot_embed.html', 'w') as f:
    f.write(html_str) 