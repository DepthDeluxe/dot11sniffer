<html>
  <head>
    <title>MAC & Cheese: Database </title>
  <head>
    <p id="temp">Temporary Header</p>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">	 
  </head>
  <body>
    <div class="container">
      <?php
	$m = new MongoClient();
	$db = $m->selectDB('mydb');
    $collection = new MongoCollection($db, 'persons');
	$personQuery = array('lastName' => 'Overstreet');
	$cursor = $collection->find();
	echo "<table class='table'>";
	echo "<thead>";
	echo "<tr>";
	echo "<th>Last Name</th>";
        echo "<th>First Name</th>";
	echo "<th>Age</th>";
	echo "</tr>";
	echo "</thead>";
	echo "<tbody>";
	foreach ($cursor as $doc) {
	    echo "<tr>";
	    echo "<td>" . $doc['lastName'] . "</td>";
	    echo "<td>" . $doc['firstName'] . "</td>";
	    echo "<td>" . $doc['age'] . "</td>";
	    echo "</tr>";
	}
	echo "</table>";
	?>
    </div>								
  </body>
</html>
