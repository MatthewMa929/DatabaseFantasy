<?php
include "connect.php";
// Get the values from the form
$un = $_POST['uname'];
$pass = $_POST['pwd'];
$sql = "SELECT * FROM users WHERE username LIKE '$un' and password LIKE
'$pass'";
$result = mysqli_query($conn, $sql);
if(mysqli_num_rows($result)===1){
$row = mysqli_fetch_assoc($result);
if($row['username'] === $un && $row['password']===$pass){
echo "login successful!";
}else{
header("Location: index.html?error=incorrect username or password");
exit();
}
}else{
header("Location: index.html?error=incorrect username or password");
exit();
}
?>