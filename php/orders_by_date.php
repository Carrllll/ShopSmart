<?php
include("db.php");
include("header.php");

$date = $_GET['date'] ?? "";
?>

<h2>Orders by Date</h2>

<form method="GET">
    <div class="form-row">
        <label for="date">Select Date:</label>
        <input type="date" id="date" name="date" required value="<?php echo htmlspecialchars($date); ?>">
        <button type="submit">Search</button>
    </div>
</form>

<?php
if ($date) {
    $safeDate = $conn->real_escape_string($date);
    $sql = "
        SELECT 
            o.order_id,
            o.order_date,
            c.name AS customer_name,
            o.status,
            o.total_amount
        FROM `Order` o
        JOIN Customer c ON c.customer_id = o.customer_id
        WHERE DATE(o.order_date) = '$safeDate'
        ORDER BY o.order_id;
    ";

    $result = $conn->query($sql);

    echo "<h3>Orders on " . htmlspecialchars($date) . "</h3>";

    if ($result && $result->num_rows > 0) {
        echo "<table>";
        echo "<tr>
                <th>Order ID</th>
                <th>Order Date</th>
                <th>Customer</th>
                <th>Status</th>
                <th>Total Amount</th>
              </tr>";
        while ($row = $result->fetch_assoc()) {
            echo "<tr>
                    <td>" . htmlspecialchars($row['order_id']) . "</td>
                    <td>" . htmlspecialchars($row['order_date']) . "</td>
                    <td>" . htmlspecialchars($row['customer_name']) . "</td>
                    <td>" . htmlspecialchars($row['status']) . "</td>
                    <td>$" . htmlspecialchars($row['total_amount']) . "</td>
                  </tr>";
        }
        echo "</table>";
    } else {
        echo "<p>No orders found for this date.</p>";
    }
}
?>

<?php
include("footer.php");
?>
