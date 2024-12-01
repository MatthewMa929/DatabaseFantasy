<?php
$conn = new PDO("mysql:host=localhost;dbname=fantasy_sports", "root", "");
$sql = "SELECT * FROM player";
$stmt = $conn->prepare($sql);
$stmt->execute();
echo '{CONNECT TEST: <br />';
while ($row = $stmt->fetch())
{ echo '----------------------------------------<br />';
echo $row["full_name"] . ' ';
echo $row["sport"] . '<br />';
}
echo '}<br />';
echo '<br />'
?>