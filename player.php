<?php
include "connect.php"; 

$sql = "SELECT PlayerID, full_name, sport, real_team, position, fantasy_points, availability_status FROM player";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
