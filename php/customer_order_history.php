<?php
include("db.php");
include("header.php");

// Fetch customers for dropdown
$customerOptions = [];
$custResult = $conn->query("SELECT customer_id, name FROM Customer ORDER BY name");
while ($row = $custResult->fetch_assoc()) {
    $customerOptions[] = $row;
}

$customer_id = isset($_GET['customer_id']) ? intval($_GET['customer_id']) : 0;
?>

<h2>Customer Order History</h2>

<form method="GET">
    <div class="form-row">
        <label for="customer_id">Select Customer:</label>
        <select id="customer_id" name="customer_id" required>
            <option value="">-- Choose --</option>
            <?php foreach ($customerOptions as $c): ?>
                <option value="<?php echo $c['customer_id']; ?>"
                    <?php if ($customer_id == $c['customer_id']) echo 'selected'; ?>>
                    <?php echo htmlspecialchars($c['name']) . " (ID " . $c['customer_id'] . ")"; ?>
                </option>
            <?php endforeach; ?>
        </select>
        <button type="submit">View Orders</button>
    </div>
</form>

<?php
if ($customer_id > 0) {
    // Orders for this customer
    $sql = "
        SELECT 
            o.order_id,
            o.order_date,
            o.status,
            o.total_amount
        FROM `Order` o
        WHERE o.customer_id = $customer_id
        ORDER BY o.order_date DESC;
    ";
    $orders = $conn->query($sql);

    if ($orders && $orders->num_rows > 0) {
        echo "<h3>Orders for Customer ID " . htmlspecialchars($customer_id) . "</h3>";
        while ($order = $orders->fetch_assoc()) {
            echo "<h4>Order #" . htmlspecialchars($order['order_id']) . 
                 " — " . htmlspecialchars($order['order_date']) . 
                 " — Status: " . htmlspecialchars($order['status']) . 
                 " — Total: $" . htmlspecialchars($order['total_amount']) . "</h4>";

            // Order items for this order
            $oid = intval($order['order_id']);
            $itemSql = "
                SELECT 
                    oi.product_id,
                    p.name AS product_name,
                    oi.quantity,
                    oi.unit_price,
                    (oi.quantity * oi.unit_price) AS line_total
                FROM OrderItem oi
                JOIN Product p ON p.product_id = oi.product_id
                WHERE oi.order_id = $oid;
            ";
            $items = $conn->query($itemSql);

            if ($items && $items->num_rows > 0) {
                echo "<table>";
                echo "<tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Unit Price</th>
                        <th>Line Total</th>
                      </tr>";
                while ($it = $items->fetch_assoc()) {
                    echo "<tr>
                            <td>" . htmlspecialchars($it['product_name']) . "</td>
                            <td>" . htmlspecialchars($it['quantity']) . "</td>
                            <td>$" . htmlspecialchars($it['unit_price']) . "</td>
                            <td>$" . htmlspecialchars($it['line_total']) . "</td>
                          </tr>";
                }
                echo "</table>";
            } else {
                echo "<p>No items found for this order.</p>";
            }
        }
    } else {
        echo "<p>No orders found for this customer.</p>";
    }
}
?>

<?php
include("footer.php");
?>
