<?php
include("db.php");
include("header.php");
?>

<h2>Low-Rated Products and Reviews</h2>
<p class="note">Shows reviews with rating 3 or below.</p>

<?php
$sql = "
    SELECT 
        r.review_id,
        p.name AS product_name,
        c.name AS customer_name,
        r.rating,
        r.comment
    FROM Review r
    JOIN Product p ON p.product_id = r.product_id
    JOIN Customer c ON c.customer_id = r.customer_id
    WHERE r.rating <= 3
    ORDER BY r.rating ASC, r.review_id DESC;
";

$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    echo "<table>";
    echo "<tr>
            <th>Review ID</th>
            <th>Product</th>
            <th>Customer</th>
            <th>Rating</th>
            <th>Comment</th>
          </tr>";
    while ($row = $result->fetch_assoc()) {
        echo "<tr>
                <td>" . htmlspecialchars($row['review_id']) . "</td>
                <td>" . htmlspecialchars($row['product_name']) . "</td>
                <td>" . htmlspecialchars($row['customer_name']) . "</td>
                <td>" . htmlspecialchars($row['rating']) . "</td>
                <td>" . htmlspecialchars($row['comment']) . "</td>
              </tr>";
    }
    echo "</table>";
} else {
    echo "<p>No low-rated reviews found.</p>";
}
?>

<?php
include("footer.php");
?>
