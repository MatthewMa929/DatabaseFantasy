<?php
include "connect.php";
// Get the values from the form
$firstname = $_POST['fname'];
$lastname = $_POST['lname'];
$username = $_POST['uname'];
$password = $_POST['pwd'];
// preparing and executing statment
$sql = "INSERT into users(firstname, lastname, username, password)
values('$firstname','$lastname','$username','$password')";
$result = mysqli_query($conn, $sql);
if($result){
echo $firstname. " is registred succesfully!";
}
$conn->close();
?>