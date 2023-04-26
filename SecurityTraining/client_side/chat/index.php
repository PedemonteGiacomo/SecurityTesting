<?php

session_start();
if (!isset($_SESSION['username'])) {
  header("Location: login.html");
  exit(); // Do you know why we need this?
}
?>

<form action="send_message.php" method="POST">
  <input name="to" placeholder="To">
  <input name="message" placeholder="Message">
  <input type="submit">
</form>

<?php

// Connect to DB
$conn = new mysqli('172.17.0.2', 'root', 'historyStoresThis', 'fstt23');

// Get user input
$user = $_SESSION['username'];

// Prepare the query
$stmt = $conn->prepare("SELECT from_user, message FROM messages WHERE to_user = ?");
$stmt->bind_param("s", $user);
// Execute the query
$stmt->execute();
$results = $stmt->get_result();


echo "<table>";
echo "<tr><td>From</td><td>Message</td></tr>";
while ($row = $results->fetch_assoc()) {
  echo "<tr><td>{$row['from_user']}</td><td>{$row['message']}</td></tr>";
}
echo "</table>";

// close connection
$conn->close();
