<?php

    $servername = "servername";
    $DBname = "dbname";
    $username = "username";
    $password = "password";
    $tblinstitute = "table name";
   
   
        
// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Check if files are uploaded
    if (isset($_FILES['image1']) && isset($_FILES['image2'])) {
        $image1 = $_FILES['image1'];
        $image2 = $_FILES['image2'];
        
        // Specify the directory where you want to save the images
        $target_dir = "images/";
        
        // Move uploaded files to the specified directory
        move_uploaded_file($image1["tmp_name"], $target_dir . basename($image1["name"]));
        move_uploaded_file($image2["tmp_name"], $target_dir . basename($image2["name"]));

        $conn = new mysqli($servername, $username, $password, $DBname);
		// Check connection
		if ($conn->connect_error) {
    		die("Connection failed: " . $conn->connect_error);
		} 
        $depth = $_POST['depth'];
        $location = $_POST['location'];
        if ($location == ",");
            $location = "15.322718,74.7542826667";
        $id = $_POST['caseid'];
		$fileloc = $target_dir.basename($image1["name"]).';'.$target_dir.basename($image2["name"]);
		date_default_timezone_set('Asia/Kolkata');
        $date = date("d-m-Y H:i:s");
        $sql = "INSERT INTO ".$tblinstitute."(caseid, location, depth, files, date) VALUES ('$id','".$location."','".$depth."','".$fileloc."','".$date."')";
        if ($conn->query($sql) === TRUE) {
                echo "1";
            } else {
                echo "Error: ".$conn->error;
                }
        
        // Get JSON data
        
        echo "Images uploaded successfully.";
        echo "Name: $depth, Age: $location, City: $id";
        
    } else {
        echo "Please upload both images.";
    }
} else {
    echo "Method not allowed.";
}
?>
