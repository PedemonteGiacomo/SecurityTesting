<?php
session_start();
// Connect to DB
$conn = new mysqli('172.17.0.2', 'root', 'pede' /* FIXME hide this? */, 'fstt23');

if(isset($_POST['user'])){

	// Get user input
	$user = $_POST['user'];
	$pass = $_POST['pass'];

	/*
	if (str_contains($pass, "'")) { die('NO HAX PLZ'); }
	else if (str_contains($pass, '"')) { die('NO HAX PLZ'); }
	// other possibility is to escape using the prepared statement
	if (str_contains($user, "'")) { die('NO HAX PLZ'); }
	*/

	// execute query
	$results = $conn->query("SELECT * FROM users WHERE username = '$user' AND password = '$pass'");


	// check if any rows were returned
	// FIXME number of rows should be 1, not more
	if ($results->num_rows > 0) {
		// Display welcome message if login was successful
		$row = $results->fetch_assoc();
		$first_name = $row['first_name'];
		$last_name = $row['last_name'];
		echo "Login successful! Welcome $first_name $last_name!";
        $_SESSION['user'] = $user;
        header("refresh:5;url=/");
	} else {
		// Otherwise, generic error message
		echo "Invalid username or password";
        header("refresh:5;url=/");
	}

}else if(isset($_GET['user'])){
	$user = $_GET['user'];
	$query = "SELECT username, first_name, last_name FROM users WHERE username LIKE '%$user%' OR first_name LIKE '%$user%'OR last_name LIKE '%$user%'";
	// $term = a' UNION ALL SELECT username, password, NULL from users -- -
	$result = $conn->query($query);

	echo "<table>";
	echo "<tr><th>Username</th><th>FirstName</th><th>LastName</th>";
	while($row = $result->fetch_assoc()){
		echo "<tr><td>".$row['username']."</td><td>".$row['first_name']."</td><td>".$row['last_name']."</td>";
	}
	echo "</table>";
    $_SESSION['user'] = $user;
    header("refresh:5;url=/");
}

// close connection
$conn->close();