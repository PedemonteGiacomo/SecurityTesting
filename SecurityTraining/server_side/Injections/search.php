<?php
// Error
ini_set('display_errors', 1);
// Connect to DB
$conn = new mysqli(
  '172.17.0.2',
  'root',
  'pede' /* FIXME hide this? */,
  'fstt23');
  
$term = $_GET['term'];
// Build SQL query with fuzzy search
$query = "SELECT username, first_name, last_name FROM users WHERE username LIKE '%$term%' OR first_name LIKE '%$term%' OR last_name LIKE '%$term%'";
// Execute SQL query
$result = $conn->query($query);

// Build table to display search results
echo "<table>";
echo "<tr><th>Username</th><th>First Name</th><th>Last Name</th></tr>";
while ($row = $result->fetch_assoc()) {
    echo "<tr><td>" . $row['username'] . "</td><td>" . $row['first_name'] . "</td><td>" . $row['last_name'] . "</td></tr>";
}
echo "</table>";

// close connection
$conn->close();