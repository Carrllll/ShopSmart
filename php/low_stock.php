<?php
include("db.php");
include("header.php");
?>

<h2>Low Stock Products</h2>
<p class="note">Products where quantity_on_hand is below reorder_level.</p>

<?php
$sql = "
    SELECT 
        p.name,
        i.quantity_on_hand,
        i.reorder_level
    FROM Inventory i
    JOIN Product p ON p.product_id = i.product_id
    WHERE i.quantity_on_hand < i.reorder_level
    ORDER BY i.quantity_on_hand ASC;
";

$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    echo "<table>";
    echo "<tr>
            <th>Product</th>
            <th>Quantity On Hand</th>
            <th>Reorder Level</th>
          </tr>";
    while ($row = $result->fetch_assoc()) {
        echo "<tr>
                <td>" . htmlspecialchars($row['name']) . "</td>
                <td>" . htmlspecialchars($row['quantity_on_hand']) . "</td>
                <td>" . htmlspecialchars($row['reorder_level']) . "</td>
              </tr>";
    }
    echo "</table>";
} else {
    echo "<p>No low stock items at the moment.</p>";
}
?>

<?php
include("footer.php");
?>
