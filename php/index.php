<?php
include("db.php");
include("header.php");
?>

<h2>Welcome to ShopSmart PHP Interface</h2>
<p>This web interface connects to the <strong>ShopSmart</strong> MySQL database and runs key business queries using PHP and MySQLi.</p>

<ul>
    <li><a href="orders_by_date.php">View orders by specific date</a></li>
    <li><a href="customer_order_history.php">View a customer&apos;s full order history</a></li>
    <li><a href="low_stock.php">View low stock inventory</a></li>
    <li><a href="revenue_by_category.php">View revenue by product category</a></li>
    <li><a href="product_ratings.php">View product ratings and review counts</a></li>
    <li><a href="top_sellers.php">View top-selling products</a></li>
    <li><a href="low_ratings.php">View low-rated products and reviews</a></li>
</ul>

<p class="note">
Each page uses SQL queries involving multiple tables (combinational queries) and displays the results in HTML table format, satisfying the course PHP web interface requirement.
</p>

<?php
include("footer.php");
?>
