"""
H&M KPI's FRONTEND IN STREAMLIT
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import requests
from PIL import Image

# Define API server url
server_url = ""

@st.experimental_memo
def load_data(url):
    try:
        response_json = requests.get(url).json()
        data = pd.json_normalize(response_json, "result")
    except Exception as e:
        print(e)
    return data 

st.title("H&M KPI's")

# Display image logo in the sidebar
logo = Image.open('STREAMLIT/H&M-Logo.svg.png')
st.sidebar.image(logo)

# ---------------------------------------------------
# FOR THE CUSTOMERS DATABASE
# ---------------------------------------------------

st.subheader("Customers Database")

# Load customers dataframe from API
customers_df = load_data(f"{server_url}api/v1/customers")

## GENERATE FILTERS

# Generate different status list
status_lst = customers_df['club_member_status'].unique()

st.sidebar.write("FILTERS")

# Create status multiselect filter
status_filter = st.sidebar.multiselect(
    label = "CLUB MEMBER STATUS",
    options = status_lst,
    default = status_lst,
    key = "multiselect_status"
)

# Create age range filter
age_filter = st.sidebar.slider(
    'Select a range of ages',
    0, 100, (20, 80))

## Apply filters to customer dataframe
customers_df = customers_df[(customers_df['age']>=age_filter[0]) & (customers_df['age']<=age_filter[1])]
customers_df = customers_df[customers_df['club_member_status'].isin(status_filter)]

## GENERATE KPIS

num_customers = len(customers_df["customer_id"])#.nunique()
avg_age = np.mean(customers_df["age"])
num_status = customers_df["club_member_status"].nunique()

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    label = "Number of different customers",
    value = num_customers,
    delta = num_customers,
)

kpi2.metric(
    label = "Number of different member status",
    value = num_status,
    delta = num_status,
)
        
kpi3.metric(
    label = "Average age",
    value = round(avg_age, 2),
    delta = -10 + avg_age,
)

st.caption("Customer age count")
st.bar_chart(customers_df.groupby(["age"])["customer_id"].count())

# Percentages of the distribution of club member status (active, pre-create, left club)
club_member_status = customers_df.groupby('club_member_status').count()
club_member_status = club_member_status[['customer_id']]
club_member_status.rename(columns={'customer_id': 'count'}, inplace=True)
club_member_status['percentage'] = (club_member_status['count'] / num_customers) * 100

# Fashion News frequency percentages
fashion_news = customers_df.groupby('fashion_news_frequency').mean()
fashion_news = fashion_news[['age']]
fashion_news.rename(columns={'age': 'average_customer_age'}, inplace=True)
fashion_news['total_count'] = customers_df.groupby('fashion_news_frequency').count().age
fashion_news['percentage'] = (fashion_news['total_count'] / num_customers) * 100

# Plot both pieplots of percentages
cols = st.columns([1, 1])

with cols[0]:
    fig_status = px.pie(club_member_status, values='percentage', names=club_member_status.index,
                title='Club Member Status Percentages')
    st.plotly_chart(fig_status, use_container_width=True)

with cols[1]:
    fig_news = px.pie(fashion_news, values='percentage', names=fashion_news.index,
                title='Fashion News Frequency Percentages')
    st.plotly_chart(fig_news, use_container_width=True)



# ---------------------------------------------------
# FOR THE ARTICLES DATABASE
# ---------------------------------------------------

st.subheader("Articles Database")

# Load articles dataframe from API
articles_df = load_data(f"{server_url}api/v1/articles")

## GENERATE FILTERS

# Generate different colors list
colors_lst = ['Beige', 'Black', 'Blue', 'Green',
              'Grey', 'Orange', 'Pink', 'Purple',
              'Red', 'Yellow', 'Gold', 'Turquoise',
              'White', 'Silver', 'Transparent', 'Other']
colors_lst.sort()

# Generate color filter
colors_filter = st.sidebar.multiselect(
    label = "PRODUCT COLORS",
    options = colors_lst,
    default = colors_lst,
    key = "multiselect_colors"
)    


## FILTER DATASET

articles_df = articles_df[articles_df['colour_group_name'].str.contains('|'.join(colors_filter))]

## GENERATE KPIS

num_articles = len(articles_df["article_id"])#.nunique()

st.metric(
    label = "Number of total articles",
    value = num_articles,
    delta = num_articles,
)

# Color percentage distribution
colors = pd.DataFrame()
colors['name'] = colors_filter
color_count = []
for color in colors['name']:
    color_count.append(len(articles_df[articles_df['colour_group_name'].str.contains(color)]))
colors['count'] = color_count
colors['percentage'] = (colors['count']/num_articles)*100


# Total article count in womens sections
women = articles_df[articles_df.section_name.str.contains("Women")]
women_prod = women.groupby('section_name').count()
women_prod = women_prod[['article_id']]
women_prod.rename(columns={'article_id': 'count'}, inplace=True)

# Total article count in mens sections
men = articles_df[articles_df.section_name.str.contains("Men")]
men_prod = men.groupby('section_name').count()
men_prod = men_prod[['article_id']]
men_prod.rename(columns={'article_id': 'count'}, inplace=True)

# Plot color distribution pieplot
fig_colors = px.pie(colors, values='percentage', names='name',
            title='Color percentages')
st.plotly_chart(fig_colors, use_container_width=True)

# Plot womens products barchart
st.caption("Women's products count")
st.bar_chart(women_prod['count'])

# Plot mens products barchart
st.caption("Men's products count")
st.bar_chart(men_prod['count'])


# ---------------------------------------------------
# FOR THE TRANSACTIONS DATABASE
# ---------------------------------------------------

st.subheader("Transactions Database")

# Load transactions dataframe from API
transactions_df = load_data(f"{server_url}api/v1/transactions")

## GENERATE FILTERS

# Generate sales channel id list
sales_channel_lst = transactions_df['sales_channel_id'].unique()
sales_channel_lst.sort()

# Create channel id filter
sales_channel_filter = st.sidebar.multiselect(
    label = "SALES CHANNEL",
    options = sales_channel_lst,
    default = sales_channel_lst,
    key = "multiselect_sales_channel"
)    

# Create a filter for number of transactions
num_transactions_filter = st.sidebar.slider(
    'Select the number of transactions',
    0, 1000, 500)

## FILTER  TRANSACTIONS DATASET

transactions_df = transactions_df.iloc[:num_transactions_filter]
transactions_df = transactions_df[transactions_df['sales_channel_id'].isin(sales_channel_filter)]

## GENERATE KPIS

kpi5, kpi6 = st.columns(2)

total_revenue = sum(transactions_df['price'])
average_transaction_value = total_revenue / len(transactions_df['price'])

kpi5.metric(
    label = "Total revenue in sales",
    value = total_revenue,
    delta = total_revenue,
)

kpi6.metric(
    label = "Average transaction value",
    value = average_transaction_value,
    delta = average_transaction_value,
)

# Sales percentage that took place online vs on the physical store
total_sales_channel_1 = len(transactions_df[transactions_df['sales_channel_id'] == 1])
total_sales_channel_2 = len(transactions_df[transactions_df['sales_channel_id'] == 2])

percentage_channel_1 = (total_sales_channel_1 / len(transactions_df['sales_channel_id'])) * 100
percentage_channel_2 = (total_sales_channel_2 / len(transactions_df['sales_channel_id'])) * 100

sales_channel_df = pd.DataFrame()
sales_channel_df['channel'] = sales_channel_lst
sales_channel_df['percentage'] = [percentage_channel_1, percentage_channel_2]

# Plot pieplot
fig_channel = px.pie(sales_channel_df, values='percentage', names='channel',
            title='Sales Channel Percentage')
st.plotly_chart(fig_channel, use_container_width=True)

# Acum sales overtime
acum_sales_df = transactions_df[['price', 'sales_channel_id']]
acum_sales_df['acum_revenue_channel_1'] = acum_sales_df[acum_sales_df["sales_channel_id"] == 1]['price']
acum_sales_df['acum_revenue_channel_2'] = acum_sales_df[acum_sales_df["sales_channel_id"] == 2]['price']
acum_sales_df = acum_sales_df.fillna(0)
acum_sales_df = acum_sales_df.cumsum()
acum_sales_df = acum_sales_df[['acum_revenue_channel_1', 'acum_revenue_channel_2']]

# Plot linechart
st.line_chart(acum_sales_df)