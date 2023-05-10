<?php

session_start();
// Connect to DB
$conn = new mysqli('172.17.0.2', 'root', 'historyStoresThis', 'fstt23');

// Get user input
$user = $_POST['user'];
$pass = $_POST['pass'];

// Prepare the query
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->bind_param("ss", $user, $pass);
// Execute the query
$stmt->execute();
$results = $stmt->get_result();

if ($results->num_rows === 1) {
// if ($results->num_rows === 1) {
    // Display welcome message if login was successful
    $row = $results->fetch_assoc();
    $first_name = $row['first_name'];
    $last_name = $row['last_name'];

    // storing connected user in session
    $_SESSION['username'] = $row['username'];
    echo "Login successful! Welcome $first_name $last_name!";
} else {
    // Otherwise, generic error message
    echo "Invalid username or password";
}

// close connection
$conn->close();
