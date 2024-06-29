<?php
// Database connection parameters
$servername = "localhost"; // Change this to your database server name if different
$username = "id22099649_pothole"; // Change this to your database username
$password = "Pothole@12345"; // Change this to your database password
$dbname = "id22099649_pothole"; // Change this to your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to select data from the pothole table
$sql = "SELECT caseid, depth, location, files, date FROM pothole";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Output data of each row
    $data = array();
    while($row = $result->fetch_assoc()) {
        // Push each row as an associative array into the $data array
        $data[] = $row;
    }
    
    // Encode the $data array as JSON and output it
    echo json_encode($data);
} else {
    echo "0 results";
}

// Close connection
$conn->close();
?>
