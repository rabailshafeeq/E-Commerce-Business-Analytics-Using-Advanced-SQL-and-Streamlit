# E-Commerce Business Analysis Using Advanced SQL

## Project Overview

This project performs an in-depth analysis of an e-commerce dataset using advanced SQL techniques to extract meaningful business insights. The objective is to simulate real-world analytical tasks by answering critical business questions related to revenue performance, customer behavior, and product contribution.

The project demonstrates how structured data can be transformed into actionable insights using SQL as the core analytical tool, supported by an interactive dashboard built with Streamlit.

---

## Objectives

* Analyze revenue trends over time
* Identify high-value customers
* Evaluate product performance
* Perform Pareto (80/20) analysis
* Demonstrate advanced SQL for business problem solving

---

## Dataset Description

The dataset represents a typical e-commerce system with relational tables:

| Table         | Description                                                     |
| ------------- | --------------------------------------------------------------- |
| Orders        | Transaction-level data including customer, product, and revenue |
| Customers     | Customer information                                            |
| Products      | Product catalog                                                 |
| Categories    | Product categorization                                          |
| Monthly_Sales | Aggregated monthly revenue                                      |

---

## SQL Techniques Used

### Joins

Combining multiple tables to build a complete analytical view:

```sql
SELECT *
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID;
```

---

### Aggregations

Calculating business metrics:

```sql
SELECT CustomerID, SUM(TotalAmount) AS total_spent
FROM Orders
GROUP BY CustomerID;
```

---

### Common Table Expressions (CTEs)

Breaking complex queries into logical steps:

```sql
WITH customer_revenue AS (
    SELECT CustomerID, SUM(TotalAmount) AS revenue
    FROM Orders
    GROUP BY CustomerID
)
SELECT * FROM customer_revenue;
```

---

### Window Functions

Enabling ranking and advanced calculations:

```sql
SELECT 
    CustomerID,
    SUM(TotalAmount) AS total_spent,
    RANK() OVER (ORDER BY SUM(TotalAmount) DESC) AS rank
FROM Orders
GROUP BY CustomerID;
```

---

### Pareto Analysis (Key Feature)

Identifying revenue concentration:

```sql
SELECT 
    CustomerID,
    SUM(TotalAmount) AS revenue,
    SUM(SUM(TotalAmount)) OVER (ORDER BY SUM(TotalAmount) DESC) 
    / SUM(SUM(TotalAmount)) OVER () * 100 AS cumulative_share
FROM Orders
GROUP BY CustomerID;
```

---

## Key Analysis and Insights

### Revenue Trends

* Revenue shows an overall growth pattern over time
* Month-over-month variation indicates seasonal or demand-driven changes

---

### Customer Analysis

* A small percentage of customers contributes a large portion of revenue
* High-value customers play a critical role in overall business performance

---

### Pareto Insight

* Approximately 20% of customers generate the majority of revenue
* Indicates strong revenue concentration and dependency on top customers

---

### Product Performance

* A limited number of products dominate total sales
* High-performing products should be prioritized for marketing and inventory

---

## Dashboard

The project includes an interactive dashboard built with Streamlit that presents:

* Executive KPIs (Revenue, Orders, Customers, Average Order Value)
* Revenue trend and growth analysis
* Customer Pareto analysis
* Product performance insights
* Data quality assessment

---

## Recommended Visuals for README

To strengthen this project, include screenshots of:

1. Executive Overview (KPIs and revenue trend)
2. Customer Pareto Analysis (cumulative revenue curve)
3. Product Performance (top products and distribution)
4. Revenue Analysis (monthly and cumulative growth)

---

## Recommended SQL Output Tables

Include sample outputs from your SQL queries:

### Top Customers

| CustomerID | Total_Spent |

### Top Products

| ProductID | Revenue |

### Revenue Trend

| Month | Revenue |

### Pareto Analysis Output

| CustomerID | Revenue | Cumulative Percentage |

---

## Project Structure

```
ecommerce-sql-dashboard/
│
├── data/
├── sql/
├── app.py
├── requirements.txt
└── README.md
```

---

## Tools and Technologies

* SQL (core analysis)
* SQLite
* Python (Pandas)
* Streamlit
* Plotly

---

## How to Run

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

---

## Conclusion

This project demonstrates how SQL can be used as a powerful tool for solving real business problems. By analyzing structured data, it provides insights into customer behavior, revenue distribution, and product performance.

The findings highlight the importance of:

* Customer retention strategies
* Revenue concentration awareness
* Product optimization

---
