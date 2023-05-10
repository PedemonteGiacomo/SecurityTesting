<?php

// Connect to DB
$conn = new mysqli(
  '172.17.0.2',
  'root',
  'pede' /* FIXME hide this? */,
  'fstt23');

$user = $_GET['user'];

$query = "SELECT * FROM users WHERE username='$user'";
// Execute SQL query
$result = $conn->query($query);

// Build table to display search results
if ($result->num_rows > 0) {
  $row = $result->fetch_assoc();
  echo "First name: " . $row['first_name'] . "</br>";
  echo "Last name: " . $row['last_name'] . "</br>";
} else {
  echo "User not found";
}

// close connection
$conn->close();