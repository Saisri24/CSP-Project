<?php
require_once 'login.php';
include_once 'Website1html';
$conn = mysqli_connect($host, $user, $pass, $db, $port);
if($conn->connect_error) die($conn->connect_error);
$option = isset($_POST['cars']) ? $_POST['cars'] : false;

?>
