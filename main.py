import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rcParams
import matplotlib.ticker as mticker

# Create a DataFrame from the given data
data = pd.read_json("./data.json", encoding ='utf-8-sig')

df = pd.DataFrame(data)

# rcParams['font.family'] = 'a thuluth'

# Create a PDF to save all the plots
with PdfPages('Invoice_Analysis.pdf') as pdf:


    # Time-Series Graphs
    plt.figure(figsize=(12, 8))

    # Graph 1: Number of invoices over time
    plt.subplot(3, 1, 1)
    for name, group in df.groupby("emp_name"):
        plt.plot(group["month"].astype(str) + '-' + group["year"].astype(str), group["num_invoices"], label=name)
    plt.title("Number of Invoices Over Time")
    plt.xlabel("Month-Year")
    plt.ylabel("Number of Invoices")
    plt.legend()

    # Graph 2: Sum of invoices over time
    plt.subplot(3, 1, 2)
    for name, group in df.groupby("emp_name"):
        plt.plot(group["month"].astype(str) + '-' + group["year"].astype(str), group["sum_invoices"], label=name)
    plt.title("Sum of Invoices Over Time")
    plt.xlabel("Month-Year")
    plt.ylabel("Sum of Invoices")
    plt.legend()

    # Graph 3: Average invoice value over time
    plt.subplot(3, 1, 3)
    for name, group in df.groupby("emp_name"):
        plt.plot(group["month"].astype(str) + '-' + group["year"].astype(str), group["avg_invoices"], label=name)
    plt.title("Average Invoice Value Over Time")
    plt.xlabel("Month-Year")
    plt.ylabel("Average Invoice Value")
    plt.legend()

    plt.tight_layout()
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

    # Pie Charts
    # Pie Chart 1: Distribution of the number of invoices
    plt.figure(figsize=(6, 6))
    df_grouped = df.groupby("emp_name")["num_invoices"].sum()
    plt.pie(df_grouped, labels=df_grouped.index, autopct='%1.1f%%')
    plt.title("Distribution of Number of Invoices")
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

    # Pie Chart 2: Distribution of the sum of invoices
    plt.figure(figsize=(6, 6))
    df_grouped = df.groupby("emp_name")["sum_invoices"].sum()
    plt.pie(df_grouped, labels=df_grouped.index, autopct='%1.1f%%')
    plt.title("Distribution of Sum of Invoices")
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

    # Heatmaps
    # Heatmap for the monthly number of invoices
    plt.figure(figsize=(10, 8))
    heatmap_data = pd.crosstab(df["month"], df["year"], values=df["num_invoices"], aggfunc="sum").fillna(0)
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", fmt=".0f")
    plt.title("Monthly Number of Invoices")
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

    # Heatmap for the monthly average of invoices per employee
    plt.figure(figsize=(10, 8))
    heatmap_data_avg_per_emp = pd.crosstab(df["month"], [df["year"], df["emp_name"]], values=df["avg_invoices"], aggfunc="mean").fillna(0)
    sns.heatmap(heatmap_data_avg_per_emp, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Monthly Average of Invoices Per Employee")
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

    # Heatmap for the monthly total of invoices per employee
    plt.figure(figsize=(10, 8))
    heatmap_data_total_per_emp = pd.crosstab(df["month"], [df["year"], df['emp_name']], values=df["num_invoices"], aggfunc="sum").fillna(0)
    sns.heatmap(heatmap_data_total_per_emp, annot=True, cmap="coolwarm", fmt=".0f")
    plt.title("Monthly Total of Invoices Per Employee")

    # filtered_df = df[df['emp_name'].isin(specific_employees)]
    # plt.figure(figsize=(10, 8))
    # heatmap_data_total_per_emp = pd.crosstab(filtered_df["month"], [filtered_df["year"], filtered_df["emp_name"]], values=filtered_df["num_invoices"], aggfunc="sum").fillna(0)
    # sns.heatmap(heatmap_data_total_per_emp, annot=True, cmap="coolwarm", fmt=".0f")
    # plt.title("Monthly Total of Invoices for Specific Employees")
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

    # Heatmap for the monthly total of invoices
    plt.figure(figsize=(10, 8))
    heatmap_data_total = pd.crosstab(df["month"], df["year"], values=df["sum_invoices"], aggfunc="sum").fillna(0)
    sns.heatmap(heatmap_data_total, annot=True, cmap="coolwarm", fmt=".0f")
    plt.title("Monthly Total of Invoices")
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

     # Additional Heatmap for the Monthly Average of Invoices
    plt.figure(figsize=(10, 8))
    heatmap_data_avg = pd.crosstab(df["month"], df["year"], values=df["avg_invoices"], aggfunc="mean").fillna(0)
    sns.heatmap(heatmap_data_avg, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Monthly Average of Invoices")
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

        # Additional Heatmap for the Monthly Average of Invoices
    plt.figure(figsize=(10, 8))
    heatmap_data_avg = pd.crosstab(df["month"], [df["year"], df["emp_name"]], values=df["avg_invoices"], aggfunc="mean").fillna(0)
    sns.heatmap(heatmap_data_avg, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Monthly Average of Invoices Per Employee")
    pdf.savefig()  # Save the current figure to the PDF
    plt.close()

unique_emp_names = df['emp_name'].unique()

with PdfPages('Filtered_Invoice_Analysis.pdf') as pdf:
    for emp_name in unique_emp_names:
        filtered_df = df.loc[df['emp_name'] == emp_name]

        # Create heatmap for the monthly average of invoices for this specific employee
        plt.figure(figsize=(10, 8))
        heatmap_data_avg = pd.crosstab(filtered_df["month"], filtered_df["year"], values=filtered_df["avg_invoices"], aggfunc="mean").fillna(0)
        sns.heatmap(heatmap_data_avg, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(f"Monthly Average of Invoices for {emp_name}")

        pdf.savefig()  # Save the current figure to the PDF
        plt.close()