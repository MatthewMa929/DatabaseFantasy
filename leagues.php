<?php
include "connect.php";

// Get the user ID from the session or request
$user_id = $_GET['user_id'] ?? null; // Replace with session data if applicable

if (!$user_id) {
    echo json_encode(["error" => "User ID is required"]);
    exit;
}

$sql = "SELECT full_name, sport, position, real_team, fantasy_points, availability_status 
        FROM player 
        WHERE user_id = :user_id";

$stmt = $conn->prepare($sql);
$stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);
$stmt->execute();

$data = [];
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $data[] = $row;
}

// Return data as JSON
header('Content-Type: application/json');
echo json_encode($data);
?>