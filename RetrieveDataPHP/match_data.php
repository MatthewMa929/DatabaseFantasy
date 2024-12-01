<?php
include "connect.php"; 

$sql = "SELECT MatchID, TeamID, match_date, final_score, winner FROM match_data";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
