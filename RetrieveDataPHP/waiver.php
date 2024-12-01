<?php
include "connect.php"; 

$sql = "SELECT WaiverID, TeamID, waiver_status, waiver_pickup_date FROM waiver";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
