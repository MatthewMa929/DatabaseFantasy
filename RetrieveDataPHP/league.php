<?php
include "../connect.php"; 

$sql = "SELECT LeagueID, UserID, league_name, league_type, draft_date, max_teams FROM league";

$stmt = $conn->prepare($sql);
$stmt->execute();

$data = []; 
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
    $data[] = $row; 
}

header('Content-Type: application/json');
echo json_encode($data); 
?>
