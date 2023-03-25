# HM-KPIs-Capstone

## Description
This project consists on the full deployment of a simple microservice-structured application that collects data from a database through an API, calculates and displays some KPI's and allows the user to filter and modify the outputs obtained. The deployment was performed in Google Cloud's App Engine for both microservices (API and Frontend).

## REPO Content
The Repository is structured in the following way:
- API
  - API_HM.py
  - app.yaml
  - requirements.txt
- STREAMLIT
  - STREAMLIT.py
  - H&M-Logo.svg.png
  - app.yaml
  - requirements.txt

There are two folders, one for each of the microservices. Within each folder, there are all the required documents for the microservice deployment, which includes the requirements.txt and app.yaml file alongside with the python application and a logo in the case of the frontend.

## API Application
The API is responsible for retrieving and passing on the data to the front end in JSON format via HTTP GET requests. It connects to a previously created SQL database in GCP, runs the corresponding query and returns the output to the user. The application was developed with flask, and the connection with the database is established through sqlalchemy and pymysql.

There are a total of three endpoints for retrieving data, one for each of the dataframes that exist in the database. These dataframes are:
- "Articles" (information about articles in the stores; color, department, description, etc.)
- "Customers" (information about the customers; age, member status, etc.)
- "Transactions" (information about the transactions; price, sales channel, etc.)
The total number of entries to be retrieved has been limited to 1000 for each of the dataframes for performance purposes.

## Streamlit Application
The Streamlit Application is responsible for the frontend. It requests the data to the API, and afterwards processes it in order to create KPI's, charts and filters for the user to interpret and modify the data. The KPI's are organized into three different blocks, one for each of the dataframes retrieved from the API microservice:

1. Customers Dataframe:
- Number of different customer
- Number of different Club Member Status
- Average age of the customers
- Bar chart age vs count
- Pie chart Club Member Status
- Pie chart Fashion News Frequency
- Filters: You are allowed to filter by Club Member Status and by range of ages

2. Articles Dataframe:
- Article count
- Pie chart of color distribution
- Bar chart of women's categories product count
- Bar chart of men's categories product count
- Filters: You are allowed to filter by color

3. Transactions Dataframe:
- Total revenue in sales
- Average transaction value
- Pie chart of sales channel distribution
- Line chart of accumulated revenue for each channel
- Filters: You are allowed to filter by Sales Channel and number of transactions

## Deployment Link
https://frontend-dot-booming-premise-375118.oa.r.appspot.com/
