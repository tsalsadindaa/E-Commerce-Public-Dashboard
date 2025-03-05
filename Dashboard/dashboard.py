import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_data = pd.read_csv('https://raw.githubusercontent.com/tsalsadindaa/E-Commerce-Public-Dashboard/refs/heads/main/Dashboard/all_data.csv')

st.header('E-Commerce Public Dashboard')

st.subheader("Produk Teratas dan Terendah")

sum_order_items_df = all_data.groupby("product_category_name_english").order_item_id.sum().sort_values(ascending=False).reset_index()
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#728CD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_item_id", y="product_category_name_english", 
            data=sum_order_items_df.sort_values(by="order_item_id", ascending=False).head(5),
            palette=colors, ax=ax[0], hue="product_category_name_english", legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Produk Teratas", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x="order_item_id", y="product_category_name_english",
            data=sum_order_items_df.head(5),
            palette=colors, ax=ax[1], hue="product_category_name_english", legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk Terendah", loc="center", fontsize=30)
st.pyplot(fig)

st.subheader("Demografi Pelanggan")

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    bystate_df = all_data.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    bystate_df = bystate_df.sort_values(by="customer_count", ascending=False).head(5)
    colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="customer_count",
        y="customer_state",
        data=bystate_df,
        palette=colors_,
        hue="customer_state",
        legend=False
    )
    plt.title("Jumlah Pelanggan Berdasarkan Provinsi", loc="center", fontsize=30)
    plt.ylabel(None)
    plt.xlabel(None)    
    plt.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    bycity_df = all_data.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    bycity_df = bycity_df.sort_values(by="customer_count", ascending=False).head(5)

    colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="customer_count",
        y="customer_city",
        data=bycity_df,
        palette=colors_,
        hue="customer_city",
        legend=False
    )
    plt.title("Jumlah Pelanggan Berdasarkan Kota", loc="center", fontsize=30)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)


st.subheader("Pelanggan Terbaik Berdasarkan Parameter RFM (customer_zip_code_prefix)")

# Pastikan kolom order_purchase_timestamp dalam format datetime
all_data["order_purchase_timestamp"] = pd.to_datetime(all_data["order_purchase_timestamp"])

rfm_df = all_data.groupby(by="customer_zip_code_prefix", as_index=False).agg({
    "order_purchase_timestamp": "max",
    "order_id": "nunique",
    "price": "sum"
})

rfm_df.columns = ["customer_zip_code_prefix", "max_order_timestamp", "frequency", "monetary"]

# Pastikan kolom max_order_timestamp dalam format datetime
rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"])

# Konversi ke format date dan hitung recency
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
recent_date = all_data["order_purchase_timestamp"].dt.date.max()
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
rfm_df.head()

col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer_zip_code_prefix", data=rfm_df.sort_values(by="recency", ascending=True).head(5), hue="customer_zip_code_prefix", palette=colors, ax=ax[0], legend=False)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)

sns.barplot(y="frequency", x="customer_zip_code_prefix", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), hue="customer_zip_code_prefix", palette=colors, ax=ax[1], legend=False)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

sns.barplot(y="monetary", x="customer_zip_code_prefix", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), hue="customer_zip_code_prefix", palette=colors, ax=ax[2], legend=False)
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.caption('Copyright (c) Tsalsa Dinda')