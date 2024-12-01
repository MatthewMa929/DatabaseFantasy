<?php
include "connect.php"; 

$sql = "SELECT PlayerStatsID, PlayerID, game_date, performance_stats, injury_status FROM player_stats";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
