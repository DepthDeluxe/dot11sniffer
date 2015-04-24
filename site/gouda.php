<html>

  <head>
      <title>MAC & Cheese: Database</title>
      <p id="main_header">Temporary Header</p>    
  </head>

  <body>

    <script type="text/javascript" src="script.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    <link rel="stylesheet" type='text/css' href='stylesheet.css'/>

    <div class="tabs">
	    <ul class="tab-links">
	        <li class="active"><a href="#tab1">MAC Database</a></li>
 	        <li><a href="#tab2">Project Description</a></li>
	        <li><a href="#tab3">Map</a></li>
	        <li><a href="#tab4">Tab #4</a></li>
	    </ul>
    

        <div class="tab-content">
            <div id="tab1" class="active">

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
			            }
			            echo "</table>";
			          ?>
		            </div>
                </body>

	        </div>

            <div id="tab2" class="tab">
                <p>TAB TWO CONTENT</p>
	        </div>

	        <div id="tab3" class="tab">
	            <p>TAB THREE CONTENT</p>
	        </div>

	        <div id="tab4" class="tab">
	            <p>TAB FOUR CONTENT</p>
	        </div>
        </div> 
	 
  </body>
</html>
