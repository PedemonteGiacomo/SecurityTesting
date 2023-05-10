<?php

$host = $_GET['host'];

// Use this instead, if you are using PHP 7 or lower
// if (strpos($host, " ") > -1)
if (str_contains($host, " ")) { die('NO HAX PLZ'); }

system("ping -c 3 $host");
