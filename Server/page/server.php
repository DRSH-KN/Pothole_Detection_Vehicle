<?php
// Database connection parameters
$servername = "localhost";
$username = "id22099649_pothole";
$password = "Pothole@12345";
$database = "id22099649_pothole";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
    
}

// Fetch data from the database
$sql = "SELECT caseid, depth, location, files, date FROM pothole";
$result = $conn->query($sql);

$data = array();

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
}

$conn->close();

// Return data as JSON
header('Content-Type: application/json');
echo json_encode($data);
?>
