<?php

session_start();
// Connect to DB
$conn = new mysqli('172.17.0.2', 'root', 'pede', 'fstt23');

if (!isset($_SESSION['user'])) {
  header("Location: /");
  exit(); // Do you know why we need this?
}

$from = $_SESSION['user'];
$to = $_POST['to'];
$message = $_POST['message'];

// Prepare the query
$stmt = $conn->prepare("INSERT INTO messages VALUES (?, ?, ?)");
$stmt->bind_param("sss", $to, $from, $message);
// Execute the query
$stmt->execute();
$results = $stmt->get_result();

// close connection
$conn->close();

echo "Message sent";
header("refresh:5;url=/");
?>
