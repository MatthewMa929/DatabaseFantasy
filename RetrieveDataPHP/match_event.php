<?php
include "connect.php"; 

$sql = "SELECT MatchEventID, MatchID, PlayerID, event_type, event_time, fantasy_points FROM match_event";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
