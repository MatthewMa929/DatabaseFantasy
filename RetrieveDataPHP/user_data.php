<?php
include "connect.php"; 

$sql = "SELECT UserID, full_name, email, username, password, profile_settings FROM user_data";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
