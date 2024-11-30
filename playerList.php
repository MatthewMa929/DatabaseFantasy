<?php
    include "connect.php";

    $sql = "SELECT name, sport, position, real_team, total_points, status FROM players";
    $result = mysqli_query($conn, $sql);

    $stmt = $conn->prepare($sql); $stmt->execute(); 
    echo 'Player information: <br />'; 
    while ($row = $stmt->fetch()) { 
        echo '----------------------------------------<br />';
        echo "Name: " . $row["full_name"] . "<br />";
        echo "Sport: " . $row["sport"] . "<br />";
        echo "Position: " . $row["position"] . "<br />";
        echo "Real Team: " . $row["real_team"] . "<br />";
        echo "Total Points: " . $row["fantasy_points"] . "<br />";
        echo "Status: " . $row["availability_status"] . "<br />";
    }
?>