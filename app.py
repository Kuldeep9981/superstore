import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='WJ28@krhp',
    database="flipkard"
)
mycursor = conn.cursor()



menu = st.sidebar.radio('Navigation', [
    'Home',
    'Insights',
    'About'

], index=0)
if menu == "Home":
    st.markdown(
        """
        <style>
        /* Background on entire app (including sidebar) */
        .stApp {
            background-image:
                linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
                url("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1470&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }

        /* Sidebar background with some transparency for readability */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.5) !important;
            color: white;
        }

        /* Optional: style sidebar links/text for better visibility */
        [data-testid="stSidebar"] .css-1d391kg, 
        [data-testid="stSidebar"] .css-1y4p8pa {
            color: white !important;
        }

        /* Title styling */
        .title-bg {
            background-color: rgba(0, 0, 0, 0.5);
            padding: 15px;
            border-radius: 12px;
            display: inline-block;
            margin-bottom: 15px;
        }

        /* Subtitle styling */
        .subtitle-bg {
            background-color: rgba(0, 0, 0, 0.4);
            padding: 10px;
            border-radius: 10px;
            display: inline-block;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center;">
            <h2 class="title-bg" style="color: white; font-weight: bold;">
                🛍️ Welcome to Super Market Data Analytics Project 📊
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center;">
            <h4 class="subtitle-bg" style="color: white; font-weight: normal;">
                🚀 Your Gateway to Business Insights
            </h4>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    ---
    👋 **Hello and welcome!**  
    This interactive dashboard is designed to help you:

    - 📈 **Explore customer and sales trends**  
    - 💰 **Track business performance in real-time**  
    - 🛒 **Identify top-performing products and regions**  
    - 🎯 **Make smarter, data-driven decisions**

    👉 Use the **sidebar** to navigate through different insights and visualizations.

    ---
    """)



    st.markdown("""

        This dashboard is designed to help you explore and understand Supermarket sales data with ease.
        Navigate through the sidebar to access different features:

        - **Overview:** Get a summary of sales trends, customer behavior, and key performance indicators.
        - **Insights:** Dive deeper into product performance, regional sales, profitability analysis, and more through detailed tables and interactive charts.
        - **Custom Queries:** (Future feature) Run your own SQL queries to tailor data analysis to your specific needs.

        Use this tool to make data-driven decisions, identify opportunities, and monitor business health in real-time.

        If you’re new here, start with the **Overview** tab to get familiar with the core metrics.

        Happy analyzing! 🎉
        """)

elif menu == 'About':
    st.markdown("""
    # About This Project

    Welcome to the **Super Market Data Analytics Dashboard**, designed to provide deep insights into sales performance, customer behavior, and product profitability using real business data.

    ### Key Features:
    - **Data Exploration:** View raw data and summary statistics to understand the dataset and its structure.
    - **Business Performance Metrics:** Track core KPIs such as total sales, profit, and unique customers for quick health checks.
    - **Geographical Analysis:** Identify cities and regions generating the highest revenue to support targeted marketing and expansion.
    - **Category & Product Insights:** Analyze sales and profit by product category and sub-category to find high-performing segments and potential growth areas.
    - **Trend Analysis:** Monitor monthly sales trends and customer segment performance over time to spot seasonality and changing behaviors.
    - **Customer Insights:** Highlight top customers by sales volume to enable personalized marketing and retention strategies.
    - **Profitability Analysis:** Detect products with high sales but low profits, as well as those generating losses, for better pricing and cost management.
    - **Granular Breakdown:** Explore sales and profit by region and customer segment for focused business strategies.

    This dashboard is built using Streamlit, connecting to a MySQL database, and leverages SQL queries combined with Python data visualization libraries to deliver actionable insights for business stakeholders.

    Feel free to navigate through the sidebar to explore the different sections and unlock valuable insights from the data!
    """)


elif menu == 'Insights':
    st.markdown(
        """
        <h2 style='text-align: center; color: #2F4F4F;'>
            📈 Sales & Customer Insights Overview
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.subheader("The top 5 customers by total sales")

    query = """SELECT customer_id,MAX(customer_name) AS 'customer_name',ROUND(SUM(Sales),2) AS Total_sales FROM superstore
          GROUP BY customer_id
         ORDER BY SUM(Sales) DESC LIMIT 5;"""
    df = pd.read_sql_query(query,conn)
    st.dataframe(df)
    st.markdown("""
        - These customers contribute the most to overall sales.
        - Consider loyalty programs or exclusive offers for them.
        """)


    st.subheader("Business Performance Summary: Sales, Profit & Unique Customers")

    query = "SELECT SUM(Sales), SUM(Profit), COUNT(DISTINCT Customer_Name) FROM superstore"
    mycursor.execute(query)
    sales, profit, unique_customers = mycursor.fetchone()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Sales", f"{sales:,.2f}")

    with col2:
        st.metric("Total Profit", f"{profit:,.2f}")

    with col3:
        st.metric("Unique Customers", unique_customers)
    st.markdown("""
    This section highlights the core financial indicators of the business. 
    Tracking total sales and profit alongside the number of unique customers offers a snapshot of overall business health and customer engagement. 
    These metrics are crucial for identifying trends, measuring performance, and making informed strategic decisions.""" )


    st.subheader("Top 10 cities generating the highest revenue")

    query = """SELECT City,SUM(Sales) AS 'Total_sales' FROM superstore
             GROUP BY City
             ORDER BY SUM(Sales) DESC
             LIMIT 10;"""
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    st.markdown("Analyzing revenue by city helps identify top-performing markets and emerging opportunities. This data supports geographic performance benchmarking and enables location-specific growth strategies")

    st.subheader(
        " Compares sales and profit across product categories to find high-performing segments")

    query = """SELECT Category,Sub_Category,
              ROUND(SUM(Sales),2) AS 'Total_sales',
              ROUND(SUM(Profit),2) AS 'Total_profit'  FROM superstore
              GROUP BY Category,Sub_Category
              ORDER BY Total_sales DESC;"""
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    st.markdown("""
    
    This table provides a comparative view of total sales and profit across product categories and sub-categories. 
    By analyzing these metrics side by side, businesses can identify which segments are driving the most revenue and profitability, enabling better product strategy and inventory decisions.""")

    st.subheader("Total Sales by Category")
    fig = px.bar(df, 'Category', 'Total_sales', color='Category')
    st.plotly_chart(fig)
    print()
    st.subheader("Total Sales by Sub-Category (Grouped by Category)")
    fig = px.bar(df, 'Sub_Category', 'Total_sales', color='Category')
    st.plotly_chart(fig)
    st.markdown("""
    This bar chart presents the total sales generated by each product category. 
    It provides a quick comparison of overall performance across high-level segments, helping identify which category contributes the most to revenue.
    """)

    print()
    st.markdown("Monthly Sales Trend Overview")

    query = """SELECT MIN(MONTHNAME(STR_TO_DATE(order_date,'%m/%d/%Y'))) AS month_name, 
               ROUND(SUM(Sales),2) As total_sales FROM superstore
               GROUP BY MONTH(STR_TO_DATE(order_date,'%m/%d/%Y'))
               ORDER BY total_sales DESC;
"""
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    st.markdown("""
    This table presents a month-wise summary of total sales, sorted by performance. 
    Analyzing monthly sales trends helps identify seasonality, peak revenue periods, and potential low-performing months. 
    This information is valuable for forecasting, inventory planning, and aligning marketing strategies with sales cycles.""")

    print()
    st.subheader("Sales Performance by Month")
    fig = px.line(df,'month_name','total_sales')
    st.plotly_chart(fig)

    print()
    st.subheader("Reveals the 5 most sold products, indicating popular demand items")
    query = """SELECT MIN(product_name) AS 'product_name' , SUM(Quantity) AS 'quantity' FROM superstore
              GROUP BY product_id 
              ORDER BY SUM(Quantity)  DESC LIMIT 5;
    """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)

    print()
    st.markdown("""
    This table lists the top 5 products based on the total quantity sold. 
    These high-demand items indicate strong customer preference and can be leveraged for promotions, bulk stocking, and revenue optimization strategies.
    """)

    st.subheader("Breaks down profit and sales based on both region and customer segment for deeper targeting.")
    query = """SELECT Region, Segment,
         ROUND(SUM(Sales),2) AS 'Total_sales', 
         SUM(Profit) AS 'Total_profit' FROM superstore 
         GROUP BY Region, Segment
         ORDER BY 'Total_sales' DESC;
        """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    st.markdown("""
    <p style='font-size:16px;'>
    This table breaks down total sales and profit by both region and customer segment, providing a granular view of business performance. 
    Understanding these dimensions helps tailor marketing efforts and resource allocation to the most lucrative customer groups within specific regions.
    </p>
    """, unsafe_allow_html=True)

    st.subheader("Shows most profitable products within each category to identify key profit drivers.")
    query = """WITH Ranked_product AS 
(SELECT Category, MIN(product_name) AS 'product_name',
SUM(Profit) AS 'Total_profit',
RANK() OVER(PARTITION BY Category ORDER BY SUM(Profit) DESC) AS 'rnk'
FROM superstore
GROUP BY Category , product_id
ORDER BY SUM(Profit) DESC)
SELECT Category,product_name,Total_profit FROM Ranked_product
WHERE rnk <= 3
ORDER BY rnk;
            """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    st.markdown("""
    <p style='font-size:16px;'>
    This analysis highlights the top three most profitable products within each category, pinpointing the key profit drivers. 
    Focusing on these products can help optimize inventory, marketing efforts, and pricing strategies to maximize overall profitability.
    </p>
    """, unsafe_allow_html=True)

    st.subheader("Highlights products or categories with good sales but poor profitability to reassess pricing or costs.")
    query = """SELECT product_name,ROUND(SUM(Sales),2) AS 'Total_sales',
           ROUND(SUM(Profit),2) AS 'Total_profit',
           ROUND((SUM(Profit) / SUM(Sales))*100,2) AS "Profit_Margins"
           FROM superstore
           GROUP BY product_id, product_name
           HAVING Profit_Margins<5 AND Total_sales>5000
           ORDER BY Total_sales DESC;
                """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    st.markdown("""
    <p style='font-size:16px;'>
    This table identifies products with strong sales volumes but low profit margins, highlighting potential issues in pricing, cost structure, or operational efficiency. 
    Addressing these areas can improve overall profitability without sacrificing sales performance.
    </p>
    """, unsafe_allow_html=True)

    st.subheader("Analyzes how different customer segments are performing over time for targeting strategy.")
    query = """SELECT YEAR(STR_TO_DATE(order_date,'%d/%m/%Y')) AS 'Year', Segment,
ROUND(SUM(Sales),2) AS 'Total_sales'
FROM superstore
GROUP BY YEAR(STR_TO_DATE(order_date,'%d/%m/%Y')), Segment
ORDER BY Year LIMIT 3,50;
                    """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    st.markdown("""
    <p style='font-size:16px;'>
    This analysis tracks sales trends over multiple years across different customer segments. 
    Monitoring segment performance over time helps identify growth opportunities, shifts in customer behavior, and informs targeted marketing strategies to maximize engagement and revenue.
    </p>
    """, unsafe_allow_html=True)

    st.subheader("Identifies products or orders that resulted in negative profit to take corrective action.")
    query = """SELECT product_name,
ROUND(SUM(SALES),2) AS 'Total_sales',
ROUND(SUM(Profit),2)  AS 'Total_profit'
FROM superstore
GROUP BY product_id, product_name
HAVING Total_profit < 0 ;
                        """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    st.markdown("""
    <p style='font-size:16px;'>
    This table highlights products with negative total profit, indicating potential loss-makers. 
    Identifying these products enables targeted review of pricing, costs, or sales strategies to mitigate losses and improve overall profitability.
    </p>
    """, unsafe_allow_html=True)

    st.subheader("Filters regions whose total sales exceed the average, indicating top-performing markets.")
    query = """SELECT Region, ROUND(SUM(Sales),2) AS 'Total_sales' FROM superstore
GROUP BY Region
HAVING SUM(Sales) > (
SELECT AVG(Total_sales) FROM (
SELECT Region,SUM(Sales) AS 'Total_sales' FROM superstore
GROUP BY Region ) AS Total_sales_region)
ORDER BY Total_sales DESC;"""


    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    st.markdown("""
    <p style='font-size:16px;'>
    This table highlights regions with total sales exceeding the average, identifying top-performing markets. 
    Focusing resources and marketing efforts on these high-revenue regions can drive further growth and profitability.
    </p>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <h2 style='text-align: center; color: green;'>THANK YOU</h2>
        <hr style='border:1px solid #ccc'/>
        """,
        unsafe_allow_html=True
    )


