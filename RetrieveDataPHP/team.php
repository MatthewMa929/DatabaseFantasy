<?php
include "connect.php"; 

$sql = "SELECT TeamID, LeagueID, UserID, team_name, total_points_scored, ranking, status FROM team";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
