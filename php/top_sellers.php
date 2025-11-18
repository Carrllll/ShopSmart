<?php
include("db.php");
include("header.php");
?>

<h2>Top-Selling Products</h2>
<p class="note">Based on total quantity sold across all orders.</p>

<?php
$sql = "
    SELECT 
        p.name AS product_name,
        SUM(oi.quantity) AS total_quantity,
        SUM(oi.quantity * oi.unit_price) AS total_revenue
    FROM OrderItem oi
    JOIN Product p ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.name
    ORDER BY total_quantity DESC
    LIMIT 20;
";

$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    echo "<table>";
    echo "<tr>
            <th>Product</th>
            <th>Total Quantity Sold</th>
            <th>Total Revenue</th>
          </tr>";
    while ($row = $result->fetch_assoc()) {
        echo "<tr>
                <td>" . htmlspecialchars($row['product_name']) . "</td>
                <td>" . htmlspecialchars($row['total_quantity']) . "</td>
                <td>$" . htmlspecialchars($row['total_revenue']) . "</td>
              </tr>";
    }
    echo "</table>";
} else {
    echo "<p>No sales data available.</p>";
}
?>

<?php
include("footer.php");
?>
