<?php
include "connect.php";

// Fetch players from the database
$sql = "SELECT * FROM players ORDER BY total_points DESC";
$result = mysqli_query($conn, $sql);
?>