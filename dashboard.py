import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_users_df(df):
    # day_2012_df = day_df.sort_values(by="instant", ascending=True).iloc[366:732]
    daily_user_df = all_df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })

    daily_user_df = daily_user_df.reset_index()

    daily_user_df.rename(columns={
        "instant": "user_count",
        "cnt": "total_user"
    }, inplace=True)

    return daily_user_df

def create_byweather_df(df):
    byweather_df = df
    byweather_df.rename(columns={
        "cnt": "total_user"
    }, inplace=True)
    
    return byweather_df

def create_byseason_df(df):
    byseason_df = df
    byseason_df.rename(columns={
        "cnt": "total_user"
    }, inplace=True)
    
    return byseason_df

def create_corr_df(df):
    corr_df = df
    corr_df.rename(columns={
        "cnt": "total_user"
    }, inplace=True)
    
    return corr_df

all_df = pd.read_csv("main_data.csv")

all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://static.vecteezy.com/system/resources/thumbnails/009/568/188/small_2x/bike-rental-station-terminal-on-modern-cityscape-street-bicycle-rent-location-city-map-on-self-service-counter-screen-public-cycle-transport-sharing-urban-eco-transportation-banner-vector.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

daily_users_df = create_daily_users_df(main_df)
byweather_df = create_byweather_df(main_df)
byseason_df = create_byseason_df(main_df)
corr_df = create_corr_df(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Daily Users')

col1, col2 = st.columns(2)
 
with col1:
    total_users = daily_users_df.total_user.sum()
    st.metric("Total users", value=total_users)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_users_df["dteday"],
    daily_users_df["total_user"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Weather")

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]


fig, ax = plt.subplots(figsize=(20, 10))
 
sns.barplot(
    y="total_user", 
    x="weathersit_str",
    data=byweather_df.sort_values(by='total_user', ascending=False),
    palette=colors,
    ax=ax,
    errorbar=None
)
ax.set_title("Number of Customer by Weather", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', rotation=10, labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader("Season")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    y="total_user", 
    x="season_str",
    data=byseason_df.sort_values(by='total_user', ascending=False),
    palette=colors,
    ax=ax,
    errorbar=None
)
ax.set_title("Number of Customer by Season", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader("Correlation Between Variables")

fig, ax = plt.subplots(figsize=(20, 10))

sns.regplot(
    x=corr_df['temp'], 
    y=corr_df['total_user']
)
ax.set_title("Correlation Between Temperatur and Customer", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel("Temperature (Normalized)", size=35)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)
