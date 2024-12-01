<?php
include "connect.php"; 

$sql = "SELECT TradeID, PlayerID, trade_date, teams_involved FROM trade";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
