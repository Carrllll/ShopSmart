<?php
include("db.php");
include("header.php");
?>

<h2>Revenue by Category</h2>

<?php
$sql = "
    SELECT 
        c.name AS category,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM `Order` o
    JOIN OrderItem oi ON oi.order_id = o.order_id
    JOIN Product p ON p.product_id = oi.product_id
    JOIN Category c ON c.category_id = p.category_id
    GROUP BY c.name
    ORDER BY revenue DESC;
";

$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    echo "<table>";
    echo "<tr>
            <th>Category</th>
            <th>Total Revenue</th>
          </tr>";
    while ($row = $result->fetch_assoc()) {
        echo "<tr>
                <td>" . htmlspecialchars($row['category']) . "</td>
                <td>$" . htmlspecialchars($row['revenue']) . "</td>
              </tr>";
    }
    echo "</table>";
} else {
    echo "<p>No revenue data available.</p>";
}
?>

<?php
include("footer.php");
?>
