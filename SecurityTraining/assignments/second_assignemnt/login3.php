<?php
// import credentials
include('mysql_credentials.php');
$con = new mysqli( $mysql_server, $mysql_user, $mysql_pass, $mysql_db );
if ($con->connect_error) die ("Connection failed: " .$con->connect_error);

$user = $_POST['user'];
$pass = $con->real_escape_string($_POST['pass']);

$query = "SELECT * FROM users WHERE username='admin' AND password='$pass'";
$result = $con->query($query);
echo $con->error;

if($result->num_rows > 0) {
  $row = $result->fetch_assoc();
  $username = $row["username"];
  echo "Welcome $username!";
} else {
  echo "Wrong username or password";
}

$con->close();
