<?php
include "connect.php"; 

$sql = "SELECT DraftID, LeagueID, PlayerID, draft_date, draft_order, draft_status FROM draft";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
