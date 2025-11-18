<?php
include("db.php");
include("header.php");
?>

<h2>Product Ratings and Review Counts</h2>

<?php
$sql = "
    SELECT 
        name,
        avg_rating,
        review_count
    FROM Product
    ORDER BY avg_rating DESC, review_count DESC;
";

$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    echo "<table>";
    echo "<tr>
            <th>Product</th>
            <th>Average Rating</th>
            <th>Review Count</th>
          </tr>";
    while ($row = $result->fetch_assoc()) {
        echo "<tr>
                <td>" . htmlspecialchars($row['name']) . "</td>
                <td>" . htmlspecialchars($row['avg_rating']) . "</td>
                <td>" . htmlspecialchars($row['review_count']) . "</td>
              </tr>";
    }
    echo "</table>";
} else {
    echo "<p>No products found.</p>";
}
?>

<?php
include("footer.php");
?>
