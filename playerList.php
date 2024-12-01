<?php
    include "connect.php"; // Make sure $conn is a PDO object

    // Query to fetch data
    $sql = "SELECT full_name, sport, position, real_team, fantasy_points, availability_status FROM player";
    
    // Prepare and execute the query using PDO
    $stmt = $conn->prepare($sql);
    $stmt->execute();

    // Display player information
    echo 'Player information: <br />';
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) { 
        echo '----------------------------------------<br />';
        echo "Name: " . $row["full_name"] . "<br />";
        echo "Sport: " . $row["sport"] . "<br />";
        echo "Position: " . $row["position"] . "<br />";
        echo "Real Team: " . $row["real_team"] . "<br />";
        echo "Total Points: " . $row["fantasy_points"] . "<br />";
        echo "Status: " . $row["availability_status"] . "<br />";
    }
?>