<?php

session_start();

//if (!isset($_SESSION['user'])) {
//  header("Location: login.html");
//  exit(); // Do you know why we need this?
//}
?>

<!DOCTYPE html>
<html>
<head>
	<title>Sign Up Form</title>
</head>
<body>
	<?php if(isset($_SESSION['user'])){ ?>
		<h1>Send Message</h1>
		<form action="send_message.php" method="POST">
			<label for="to">To:</label>
			<input type="text" name="to"><br><br>

			<label for="message">Password:</label>
			<input type="text" name="message"><br><br>

			<input type="submit" name="submit" value="Send">
		</form>
	<?php } else { ?>
		<h1>Login</h1>
		<form action="signIn.php" method="POST">
			<label for="name">Name:</label>
			<input type="text" name="user"><br><br>

			<label for="password">Password:</label>
			<input type="password" name="pass"><br><br>

			<input type="submit" name="submit" value="SignIn">
		</form>
	<?php } ?>
	<br><br><br>
	<?php

// Connect to DB
$conn = new mysqli('172.17.0.2', 'root', 'pede', 'fstt23');
if(isset( $_SESSION['user'])){
	// Get user input
	$user = $_SESSION['user'];

	// Prepare the query
	$stmt = $conn->prepare("SELECT from_user, message FROM messages WHERE to_user = ?");
	$stmt->bind_param("s", $user);
	// Execute the query
	$stmt->execute();
	$results = $stmt->get_result();

	echo "\n\n Messages Recieved";
	echo "<table>";
	echo "<tr><td>From</td><td>Message</td></tr>";
	while ($row = $results->fetch_assoc()) {
	  echo "<tr><td>{$row['from_user']}</td><td>{$row['message']}</td></tr>";
	}
	echo "</table>";
}
// close connection
$conn->close();

?>
</body>
</html>