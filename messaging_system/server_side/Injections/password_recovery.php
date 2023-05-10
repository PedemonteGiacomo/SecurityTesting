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
echo "If your user exists on our system, you will receive an email with the instruction to recover your password.";


// close connection
$conn->close();