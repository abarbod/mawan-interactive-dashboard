import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
@st.cache  # Cache the data to speed up the app
def load_data():
    data = pd.read_json("./data_v2.json", encoding ='utf-8-sig')
    return data

df = load_data()

# Title and introduction
st.title("Invoice Analysis Dashboard")
st.write("This dashboard provides various insights into invoices.")

# Title and introduction
st.title("Invoice Analysis Dashboard")
st.write("This dashboard provides various insights into invoices.")

# Sidebar for filters
st.sidebar.header("Filters")
selected_Status = st.sidebar.multiselect("Select Status", df["status"].unique())
selected_emp = st.sidebar.multiselect("Select Employees", df["emp_name"].unique())
selected_year = st.sidebar.multiselect("Select Year", df["year"].unique())
selected_month = st.sidebar.multiselect("Select Month", df["month"].unique())
selected_branch = st.sidebar.multiselect("Select branch", df["branch"].unique())
# selected_month = st.sidebar.multiselect("Select Month", df["month"].unique())
show_per_emp = st.sidebar.checkbox("Show Heatmap Per Employee")
exclude_statuses = st.sidebar.checkbox("Exclude Canceled, Returned, RETURN/REFUND")


# Filter the data based on the sidebar inputs
df_filtered = df.copy()

if selected_emp:
    df_filtered = df_filtered[df_filtered["emp_name"].isin(selected_emp)]

if selected_year:
    df_filtered = df_filtered[df_filtered["year"].isin(selected_year)]

if selected_month:
    df_filtered = df_filtered[df_filtered["month"].isin(selected_month)]

if selected_Status:
    df_filtered = df_filtered[df_filtered["status"].isin(selected_Status)]

if exclude_statuses:  # New filtering logic
    df_filtered = df_filtered[~df_filtered['status'].isin(['Canceled', 'Returned', 'RETURN/REFUND'])]

# Time-Series Graphs
st.subheader("Time-Series Graphs")

# Graph 1: Number of invoices over time
st.write("### Number of Invoices Over Time")
fig, ax = plt.subplots(figsize=(12, 6))
for name, group in df_filtered.groupby("emp_name"):
    plt.plot(group["month"].astype(str) + '-' + group["year"].astype(str), group["num_invoices"], label=name)
plt.legend()
st.pyplot(fig)

# Graph 1: Total of invoices over time
st.write("### Total of Invoices Over Time")
fig, ax = plt.subplots(figsize=(12, 6))
for name, group in df_filtered.groupby("emp_name"):
    plt.plot(group["month"].astype(str) + '-' + group["year"].astype(str), group["sum_invoices"], label=name)
plt.legend()
st.pyplot(fig)

# Graph 2: Average invoice value over time
st.write("### Average invoice value over time")
fig, ax = plt.subplots(figsize=(12, 6))
for name, group in df_filtered.groupby("emp_name"):
    plt.plot(group["month"].astype(str) + '-' + group["year"].astype(str), group["avg_invoices"], label=name)
plt.legend()
st.pyplot(fig)


# Heatmaps
st.subheader("Heatmaps")

if show_per_emp:
    st.write("### Monthly Number of Invoices Per Employee")
    fig, ax = plt.subplots(figsize=(10, 8))
    heatmap_data = pd.crosstab(df_filtered["month"], [df_filtered["year"], df_filtered["emp_name"]], values=df_filtered["num_invoices"], aggfunc="sum").fillna(0)
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", fmt=".0f")
    st.pyplot(fig)
else:
    st.write("### Monthly Number of Invoices")
    fig, ax = plt.subplots(figsize=(10, 8))
    heatmap_data = pd.crosstab(df_filtered["month"], df_filtered["year"], values=df_filtered["num_invoices"], aggfunc="sum").fillna(0)
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", fmt=".0f")
    st.pyplot(fig)


if show_per_emp:
    st.write("### Monthly Total of Invoices Per Employee")
    fig, ax = plt.subplots(figsize=(10, 8))
    heatmap_data = pd.crosstab(df_filtered["month"], [df_filtered["year"], df_filtered["emp_name"]], values=df_filtered["sum_invoices"], aggfunc="sum").fillna(0)
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", fmt=".0f")
    st.pyplot(fig)
else:
    st.write("### Monthly Total of Invoices")
    fig, ax = plt.subplots(figsize=(10, 8))
    heatmap_data = pd.crosstab(df_filtered["month"], df_filtered["year"], values=df_filtered["sum_invoices"], aggfunc="sum").fillna(0)
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", fmt=".0f")
    st.pyplot(fig)



# Heatmap for the monthly number of invoices
st.write("### Monthly Total of Invoices")
fig, ax = plt.subplots(figsize=(10, 8))
heatmap_data = pd.crosstab(df_filtered["month"], df_filtered["year"], values=df_filtered["sum_invoices"], aggfunc="sum").fillna(0)
sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", fmt=".0f")
st.pyplot(fig)


# Additional functionalities can be added similarly

# Data Table
st.subheader("Filtered Data Table")
st.write(df_filtered)

# Download Button
import base64
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

if st.button('Download Data as Excel'):
    towrite = to_excel(df_filtered)
    b64 = base64.b64encode(towrite).decode()
    st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="filtered_data.xlsx">Download Excel File</a>', unsafe_allow_html=True)