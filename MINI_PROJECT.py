import streamlit as st
import pandas as pd
import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        host="dbdurga.crumicwkuosy.us-east-1.rds.amazonaws.com",
        port=5432,
        database="postgres",
        user="postgres",
        password="tharshan2020"
    )
    return conn

def run_query(query):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

st.title("Retail Order Dashboard")


queries_by_guvi={

        " Top 10 highest revenue products":
        'SELECT product_id,SUM(quantity * sale_price) AS revenue FROM df GROUP BY product_id ORDER BY revenue DESC LIMIT 10;',

        " Find the top 5 cities with the highest profit margins":
        'SELECT o."city", SUM(d."profit") AS Total_Profit FROM df o JOIN  df1_orders d ON  o."sub_category" = d."sub_category" GROUP BY  o."city" ORDER BY Total_Profit DESC LIMIT 5;',


        "Calculate the total discount given for each category":
         'SELECT category, SUM(discount) AS total_discount FROM df GROUP BY category;',


        " Find the average sale price per product category":
        'SELECT category, AVG(sale_price) AS average_sale_price FROM df GROUP BY category;',


        "Find the region with the highest average sale price":
        'SELECT region, AVG(sale_price) AS average_sale_price FROM df GROUP BY region ORDER BY average_sale_price DESC LIMIT 1;',

        " Find the total profit per category":
        'SELECT category, SUM(sale_price - cost_price) AS total_profit FROM df GROUP BY category;',


        "Identify the top 3 segments with the highest quantity of orders":
        'SELECT segment, SUM(quantity) AS total_quantity FROM df GROUP BY segment ORDER BY total_quantity DESC LIMIT 3;',

        "Determine the average discount percentage given per region":
        'SELECT region, AVG(discount / sale_price * 100) AS average_discount_percent FROM df GROUP BY region;',


        "Find the product category with the highest total profit":
        'SELECT category, SUM(sale_price - cost_price) AS total_profit FROM df GROUP BY category ORDER BY total_profit DESC LIMIT 1;',

        "Calculate the total revenue generated per year":
         'SELECT "year", SUM("sale_price" * "quantity") AS total_revenue FROM df GROUP BY "year" ORDER BY "year";',
}



my_own_queries= {

       "find the Products with no profit":
        'SELECT product_id FROM df GROUP BY product_id HAVING SUM(profit) = 0;',

        "Calculate total revenue per shipping mode":
         'SELECT ship_mode, SUM(quantity * sale_price) AS total_revenue FROM df GROUP BY ship_mode ORDER BY total_revenue DESC;',

        "Find the top 3 cities with the lowest total discounts":
         'SELECT city, SUM(discount) AS total_discount FROM df GROUP BY city ORDER BY total_discount ASC LIMIT 3;',


        "Identify the sub-category with the highest revenue":
         'SELECT sub_category, SUM(quantity * sale_price) AS revenue FROM df GROUP BY sub_category ORDER BY revenue DESC LIMIT 1;',


        "Find the average quantity of orders per product category":
         'SELECT category, AVG(quantity) AS average_quantity FROM df GROUP BY category ORDER BY average_quantity DESC;',


        "Find the product with the highest total quantity sold":
         'SELECT product_id, SUM(quantity) AS total_quantity_sold FROM df GROUP BY product_id ORDER BY total_quantity_sold DESC LIMIT 1;',

         "Total orders per segment": 
        'SELECT COUNT(DISTINCT "order_id") AS total_orders FROM df;',

        "Find the state with the highest number of orders":
        'SELECT state, COUNT(*) AS order_count  FROM df GROUP BY state ORDER BY order_count DESC LIMIT 1;',



        "Calculate the total revenue and profit for each region":
       'SELECT region, SUM(quantity * sale_price) AS total_revenue, SUM((sale_price - cost_price) * quantity) AS total_profit FROM df GROUP BY region ORDER BY total_revenue DESC;',



        "Calculate the percentage contribution of each region to total revenue":
        'SELECT region, SUM(quantity * sale_price) AS total_revenue FROM df GROUP BY region;',
        
 }


nav = st.radio("Select Query Section", ["queries by GUVI", "My Own Queries"])

if nav == "queries by GUVI":
         st.subheader("queries by GUVI")
         query = st.selectbox("Select a query to visualize:", list(queries_by_guvi.keys()))
         selected_query_set = queries_by_guvi
elif nav == "My Own Queries":
         st.subheader("My Own Queries")
         query = st.selectbox("Select a query to visualize:", list(my_own_queries.keys()))
         selected_query_set = my_own_queries

else:
          query = None

if query:
        result_df = run_query(selected_query_set[query])
        if result_df is not None:
          st.dataframe(result_df)
else:
           st.warning("Please select a query.")

           st.text("Thank you for using the dashboard!")
