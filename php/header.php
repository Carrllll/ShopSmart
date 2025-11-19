<?php
// header.php 
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ShopSmart DB Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0 0 40px 0;
            background-color: #fafafa;
        }
        header {
            background-color: #222;
            color: #fff;
            padding: 15px 20px;
        }
        header h1 {
            margin: 0;
            font-size: 20px;
        }
        nav {
            background-color: #333;
            padding: 8px 20px;
        }
        nav a {
            color: #ddd;
            margin-right: 15px;
            text-decoration: none;
            font-size: 14px;
        }
        nav a:hover {
            color: #fff;
            text-decoration: underline;
        }
        .container {
            padding: 20px;
        }
        h2 {
            margin-top: 0;
        }
        table {
            border-collapse: collapse;
            margin-top: 15px;
            background-color: #fff;
        }
        table th, table td {
            padding: 8px 10px;
            border: 1px solid #ccc;
            font-size: 14px;
        }
        table th {
            background-color: #f5f5f5;
        }
        .form-row {
            margin: 10px 0;
        }
        .form-row label {
            margin-right: 8px;
        }
        .form-row input, .form-row select {
            padding: 4px 6px;
        }
        .note {
            font-size: 13px;
            color: #666;
        }
    </style>
</head>
<body>
<header>
    <h1>ShopSmart Database Interface (PHP)</h1>
</header>
<nav>
    <a href="index.php">Home</a>
    <a href="orders_by_date.php">Orders by Date</a>
    <a href="customer_order_history.php">Customer Order History</a>
    <a href="low_stock.php">Low Stock</a>
    <a href="revenue_by_category.php">Revenue by Category</a>
    <a href="product_ratings.php">Product Ratings</a>
    <a href="top_sellers.php">Top Sellers</a>
    <a href="low_ratings.php">Low Ratings</a>
</nav>
<div class="container">
