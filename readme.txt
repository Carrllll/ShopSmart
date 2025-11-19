ShopSmart E-Commerce Database Project

Project Title: ShopSmart — E-Commerce Database System
Course: Database Management (Final Project)
Authors: Carl Simon, Donald Okonkwo
Creation Date: November 2025

1. Overview

ShopSmart is a complete e-commerce database and web system built using MySQL, PHP, and a Python Dash analytics dashboard.
The system supports merchant operations (product and inventory management, sales analytics, review monitoring) and customer operations (searching, ordering, reviewing).

This project package includes:

A PDF project paper

All SQL files (schema, triggers, procedures, sample data)

All PHP source code

The Dash analytics application

This readme.txt file

2. Authors

Carl Simon

Donald Okonkwo

Rory Samuels

3. Creation Timeline

Database & ERD Design — October 2025

SQL Implementation — October–November 2025

PHP Interface — November 2025

Dash Analytics App — November 2025

Final Packaging — November 2025

4. Project File Structure
ShopSmart_Final_Project/
│
├── paper/
│   └── ShopSmart_Project_Report.pdf
│
├── sql/
│   ├── shopsmart_schema.sql
│   ├── shopsmart_constraints.sql
│   ├── shopsmart_triggers.sql
│   ├── shopsmart_procedures_functions.sql
│   ├── shopsmart_sample_data.sql
│   └── shopsmart_full_dump.sql
│
├── php/
│   ├── db.php
│   ├── header.php
│   ├── footer.php
│   ├── index.php
│   │
│   ├── orders_by_date.php
│   ├── customer_order_history.php
│   ├── low_stock.php
│   ├── revenue_by_category.php
│   ├── top_sellers.php
│   ├── low_ratings.php
│   ├── product_ratings.php
│   └── (assets: css, images if used)
│
├── ShopSmartDash/
│   ├── interactiveApp.py
│
└── readme.txt

5. Description of Major Components
A. SQL Files

shopsmart_schema.sql – Creates all tables: Customer, Category, Product, Inventory, Order, OrderItem, Review, Payment

shopsmart_constraints.sql – Contains CHECK and UNIQUE constraints

shopsmart_triggers.sql – Inventory deduction, order total recalculation, rating aggregation

shopsmart_procedures_functions.sql – Stored procedures and function

shopsmart_sample_data.sql – Inserts ≥10 rows per table

shopsmart_full_dump.sql – Complete database export

B. PHP Files

Merchant and customer-facing interface pages:

index.php – Home navigation

db.php – Database connection

header.php, footer.php – Shared layout

Business Query Pages:

orders_by_date.php

customer_order_history.php

low_stock.php

revenue_by_category.php

top_sellers.php

low_ratings.php

product_ratings.php

C. Dash Analytics App

Located in /dash/:

interactiveApp.py – Multi-tab analytics dashboard

Tabs include: Overview, Sales, Products, Inventory

Supports write actions: create demo orders, add reviews, restock inventory

Fully connected to the same MySQL database as PHP

6. How to Run the Project
MySQL Setup

Open phpMyAdmin via XAMPP

Create a database named shopsmart

Import shopsmart_full_dump.sql
(or run schema + data files in order)

PHP Interface

Copy the php/ folder to:
/Applications/XAMPP/xamppfiles/htdocs/ShopSmart/php/

Start Apache + MySQL in XAMPP

Open in browser:
http://localhost/ShopSmart/php/

Dash App

Navigate to /dash

Install dependencies:
pip install -r requirements.txt

Run:
python interactiveApp.py

Open in browser:
http://127.0.0.1:8050/

7. Notes

All project requirements are met: triggers, procedures, constraints, multi-table queries, and 10+ rows per table.

PHP and Dash applications both read from and write to the same MySQL database.

The Dash app is an optional enhancement demonstrating advanced analytics.

8. Contact

For questions:
Carl Simon & Donald Okonkwo