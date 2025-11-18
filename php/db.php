<?php
// db.php - Database connection for ShopSmart

$host = "localhost";
$user = "root";
$pass = "";          // change if your MySQL has a password
$db   = "ShopSmart";

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}

// optional but good practice
$conn->set_charset("utf8mb4");
?>
