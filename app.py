import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="E-Commerce Business Analytics Dashboard",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

st.markdown("""
<style>
.block-container {
    padding-top: 3rem;
}
.metric-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #374151;
}
.insight-box {
    background-color: #111827;
    padding: 18px;
    border-left: 4px solid #3b82f6;
    border-radius: 8px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    orders = pd.read_csv(DATA_DIR / "Orders.csv")
    customers = pd.read_csv(DATA_DIR / "Customers.csv")
    products = pd.read_csv(DATA_DIR / "Products.csv")
    categories = pd.read_csv(DATA_DIR / "Categories.csv")
    monthly_sales = pd.read_csv(DATA_DIR / "Monthly_Sales.csv")
    return orders, customers, products, categories, monthly_sales


orders, customers, products, categories, monthly_sales = load_data()


def find_col(df, possible_names):
    for col in df.columns:
        clean_col = col.lower().replace("_", "").replace(" ", "")
        if clean_col in possible_names:
            return col
    return None


order_id_col = find_col(orders, ["orderid", "id"])
customer_id_col = find_col(orders, ["customerid", "customer"])
product_id_col = find_col(orders, ["productid", "product"])
amount_col = find_col(orders, ["totalamount", "amount", "sales", "revenue", "total"])
date_col_orders = find_col(orders, ["orderdate", "date"])

monthly_date_col = monthly_sales.columns[0]
monthly_sales_col = monthly_sales.columns[-1]

if date_col_orders:
    orders[date_col_orders] = pd.to_datetime(orders[date_col_orders], errors="coerce")

monthly_sales[monthly_date_col] = pd.to_datetime(monthly_sales[monthly_date_col], errors="coerce")

st.title("E-Commerce Business Analytics Dashboard")
st.markdown(
    "An interactive business intelligence dashboard focused on revenue performance, customer value, product contribution, and growth opportunities."
)

st.divider()

# Sidebar filters
st.sidebar.title("Dashboard Controls")

section = st.sidebar.radio(
    "Select Section",
    [
        "Executive Overview",
        "Revenue Analysis",
        "Customer Pareto Analysis",
        "Product Performance",
        "Data Quality",
        "Raw Data"
    ]
)

filtered_orders = orders.copy()
# KPIs
total_orders = len(filtered_orders)
total_customers = filtered_orders[customer_id_col].nunique() if customer_id_col else customers.shape[0]
total_products = filtered_orders[product_id_col].nunique() if product_id_col else products.shape[0]

if amount_col:
    total_revenue = filtered_orders[amount_col].sum()
else:
    total_revenue = monthly_sales[monthly_sales_col].sum()

avg_order_value = total_revenue / total_orders if total_orders else 0

if section == "Executive Overview":
    st.subheader("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"{total_revenue:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Active Customers", f"{total_customers:,}")
    col4.metric("Average Order Value", f"{avg_order_value:,.2f}")

    st.divider()

    monthly_sales["Revenue Growth %"] = monthly_sales[monthly_sales_col].pct_change() * 100
    monthly_sales["Cumulative Revenue"] = monthly_sales[monthly_sales_col].cumsum()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            monthly_sales,
            x=monthly_date_col,
            y=monthly_sales_col,
            markers=True,
            title="Revenue Growth Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            monthly_sales,
            x=monthly_date_col,
            y="Revenue Growth %",
            title="Month-over-Month Revenue Growth"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Business Insights")

    best_month = monthly_sales.loc[monthly_sales[monthly_sales_col].idxmax()]
    worst_month = monthly_sales.loc[monthly_sales[monthly_sales_col].idxmin()]

    st.markdown(f"""
    <div class="insight-box">
    <b>Revenue Performance:</b> Total revenue is {total_revenue:,.0f}, with an average order value of {avg_order_value:,.2f}.
    </div>

    <div class="insight-box">
    <b>Best Sales Month:</b> {best_month[monthly_date_col].date()} generated the highest monthly revenue.
    </div>

    <div class="insight-box">
    <b>Business Opportunity:</b> Improving average order value through bundles, upsells, and loyalty offers can directly increase revenue.
    </div>
    """, unsafe_allow_html=True)


elif section == "Revenue Analysis":
    st.subheader("Revenue Analysis")

    monthly_sales["Revenue Growth %"] = monthly_sales[monthly_sales_col].pct_change() * 100
    monthly_sales["Cumulative Revenue"] = monthly_sales[monthly_sales_col].cumsum()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            monthly_sales,
            x=monthly_date_col,
            y=monthly_sales_col,
            markers=True,
            title="Monthly Revenue Trend"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.line(
            monthly_sales,
            x=monthly_date_col,
            y="Cumulative Revenue",
            markers=True,
            title="Cumulative Revenue Growth"
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig = px.bar(
            monthly_sales,
            x=monthly_date_col,
            y="Revenue Growth %",
            title="Monthly Revenue Growth Rate"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.box(
            monthly_sales,
            y=monthly_sales_col,
            title="Monthly Revenue Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    avg_monthly_revenue = monthly_sales[monthly_sales_col].mean()
    latest_revenue = monthly_sales[monthly_sales_col].iloc[-1]
    first_revenue = monthly_sales[monthly_sales_col].iloc[0]
    total_growth = ((latest_revenue - first_revenue) / first_revenue) * 100 if first_revenue else 0

    st.subheader("Revenue Insights")
    st.markdown(f"""
    <div class="insight-box">
    <b>Average Monthly Revenue:</b> {avg_monthly_revenue:,.0f}
    </div>

    <div class="insight-box">
    <b>Overall Revenue Change:</b> Revenue changed by {total_growth:,.2f}% from the first month to the latest month.
    </div>

    <div class="insight-box">
    <b>Analyst Recommendation:</b> Investigate low-growth months and compare them with campaigns, product availability, and customer activity.
    </div>
    """, unsafe_allow_html=True)


elif section == "Customer Pareto Analysis":
    st.subheader("Customer Pareto Analysis")

    if customer_id_col and amount_col:
        customer_revenue = (
            filtered_orders.groupby(customer_id_col)[amount_col]
            .sum()
            .reset_index()
            .sort_values(amount_col, ascending=False)
        )

        customer_revenue["Revenue Share %"] = (
            customer_revenue[amount_col] / customer_revenue[amount_col].sum()
        ) * 100

        customer_revenue["Cumulative Revenue Share %"] = customer_revenue["Revenue Share %"].cumsum()

        total_customer_count = customer_revenue.shape[0]
        top_20_count = max(int(total_customer_count * 0.2), 1)

        top_20_revenue_share = customer_revenue.head(top_20_count)[amount_col].sum() / customer_revenue[amount_col].sum() * 100
        top_10_customers = customer_revenue.head(10)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                top_10_customers,
                x=customer_id_col,
                y=amount_col,
                title="Top 10 Customers by Revenue"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.line(
                customer_revenue.head(100),
                x=customer_id_col,
                y="Cumulative Revenue Share %",
                markers=True,
                title="Customer Revenue Pareto Curve"
            )
            st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            fig = px.histogram(
                customer_revenue,
                x=amount_col,
                nbins=30,
                title="Customer Spending Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            customer_revenue["Customer Segment"] = pd.qcut(
                customer_revenue[amount_col],
                q=3,
                labels=["Low Value", "Medium Value", "High Value"]
            )

            segment_summary = (
                customer_revenue.groupby("Customer Segment", observed=True)[amount_col]
                .sum()
                .reset_index()
            )

            fig = px.pie(
                segment_summary,
                names="Customer Segment",
                values=amount_col,
                title="Revenue by Customer Segment"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Customer Insights")

        st.markdown(f"""
        <div class="insight-box">
        <b>Pareto Finding:</b> The top 20% of customers generate {top_20_revenue_share:,.2f}% of total revenue.
        </div>

        <div class="insight-box">
        <b>Customer Concentration:</b> A small group of high-value customers has a major impact on revenue.
        </div>

        <div class="insight-box">
        <b>Business Recommendation:</b> Prioritize retention campaigns, loyalty rewards, and personalized offers for high-value customers.
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(customer_revenue.head(30), use_container_width=True)

    else:
        st.warning("Customer analysis requires customer ID and revenue columns in Orders.csv.")


elif section == "Product Performance":
    st.subheader("Product Performance Analysis")

    if product_id_col and amount_col:
        product_revenue = (
            filtered_orders.groupby(product_id_col)[amount_col]
            .sum()
            .reset_index()
            .sort_values(amount_col, ascending=False)
        )

        product_orders = (
            filtered_orders.groupby(product_id_col)
            .size()
            .reset_index(name="Order Count")
            .sort_values("Order Count", ascending=False)
        )

        product_revenue["Revenue Share %"] = (
            product_revenue[amount_col] / product_revenue[amount_col].sum()
        ) * 100

        product_revenue["Cumulative Revenue Share %"] = product_revenue["Revenue Share %"].cumsum()

        top_10_products = product_revenue.head(10)
        top_20_product_count = max(int(product_revenue.shape[0] * 0.2), 1)
        top_20_product_share = product_revenue.head(top_20_product_count)[amount_col].sum() / product_revenue[amount_col].sum() * 100

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                top_10_products,
                x=product_id_col,
                y=amount_col,
                title="Top 10 Products by Revenue"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                product_orders.head(10),
                x=product_id_col,
                y="Order Count",
                title="Top 10 Products by Order Count"
            )
            st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            fig = px.line(
                product_revenue.head(100),
                x=product_id_col,
                y="Cumulative Revenue Share %",
                markers=True,
                title="Product Revenue Pareto Curve"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            fig = px.pie(
                top_10_products,
                names=product_id_col,
                values=amount_col,
                title="Revenue Share of Top 10 Products"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Product Insights")

        st.markdown(f"""
        <div class="insight-box">
        <b>Product Concentration:</b> The top 20% of products generate {top_20_product_share:,.2f}% of total product revenue.
        </div>

        <div class="insight-box">
        <b>Business Meaning:</b> Revenue is concentrated among a limited number of products.
        </div>

        <div class="insight-box">
        <b>Recommendation:</b> Increase visibility of top products and review pricing, bundling, or promotion strategy for low-performing products.
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(product_revenue.head(30), use_container_width=True)

    else:
        st.warning("Product analysis requires product ID and revenue columns in Orders.csv.")


elif section == "Data Quality":
    st.subheader("Data Quality Report")

    datasets = {
        "Orders": orders,
        "Customers": customers,
        "Products": products,
        "Categories": categories,
        "Monthly Sales": monthly_sales
    }

    quality_summary = []

    for name, df in datasets.items():
        quality_summary.append({
            "Dataset": name,
            "Rows": df.shape[0],
            "Columns": df.shape[1],
            "Missing Values": int(df.isnull().sum().sum()),
            "Duplicate Rows": int(df.duplicated().sum())
        })

    quality_df = pd.DataFrame(quality_summary)

    st.dataframe(quality_df, use_container_width=True)

    selected_dataset = st.selectbox("Select Dataset for Missing Value Review", list(datasets.keys()))
    selected_df = datasets[selected_dataset]

    missing_df = (
        selected_df.isnull()
        .sum()
        .reset_index()
        .rename(columns={"index": "Column", 0: "Missing Values"})
    )

    fig = px.bar(
        missing_df,
        x="Column",
        y="Missing Values",
        title=f"Missing Values by Column: {selected_dataset}"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <b>Data Quality Note:</b> Missing values and duplicate records can affect revenue calculations, customer segmentation, and product performance analysis.
    </div>
    """, unsafe_allow_html=True)


elif section == "Raw Data":
    st.subheader("Raw Data Explorer")

    dataset_choice = st.selectbox(
        "Choose Dataset",
        ["Orders", "Customers", "Products", "Categories", "Monthly Sales"]
    )

    if dataset_choice == "Orders":
        df = orders
    elif dataset_choice == "Customers":
        df = customers
    elif dataset_choice == "Products":
        df = products
    elif dataset_choice == "Categories":
        df = categories
    else:
        df = monthly_sales

    st.write("Dataset Shape:", df.shape)
    st.write("Columns:", list(df.columns))
    st.dataframe(df, use_container_width=True)