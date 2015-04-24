<html>

  <head>
    <title>MAC & Cheese</title>
    <p id="main_header">MAC & Cheese: Mapping Population Densities with WiFi Signals </p>
  </head>

  <body>

    <!-- Includes jQuery 2.1.0 for use by script.js -->
    <script type "text/javascript" src="http://code.jquery.com/jquery-2.1.0.min.js" type="text/javascript"></script>
    <script type="text/javascript" src="script.js"></script>


    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">	 
  	<link rel="stylesheet" type='text/css' href='stylesheet.css'/>

    <div class="tabs">
        <ul class="tab-links">
	        <li class="active"><a href="#project_description">Project Description</a></li>
            <li><a href="#map">Map</a></li>
            <li><a href="#team">Our Team</a></li>
	    </ul>

	    <div class="tab-content">
            <div id="project_description" class="active">
                <p id="proj_desc"> In the modern world, buildings are areas of high pedestrian traffic, but the owners of most sites have little to no data on the extent nor patterns of that traffic. Knowing how many people are in the building or a specific room can be important and useful data to building owners. The solution is MAC & Cheese: by monitoring WiFi packets sent and received in a small locality, it is possible to track building usage, possibly even down to the repeated presence in certain rooms of certain devices. This data can be used to manage the energy costs by adjusting heating and cooling, analyze energy use patterns, or even make sure that someone is not somewhere they should not be. Also, it can be used to encourage an energy saving behavior and to allocate resources in a university classroom. In a commercial environment this could even provide data on which areas are frequented most.</p>
            </div>
	        <div id="map" class="tab">
                <p>Location of Devices on the First Floor of Breakiron</p>
		<?php
			$command = escapeshellcmd('images/grad.py');
			$output = shell_exec($command);
		?>
                <img src="images/test.png" alt="Place density gradient map here" id="img_test" style='width:400px;height=500px'>
            </div>

            <div id="team" class="tab">
		<p><strong>Samuel Brandstadt</strong> - Computer Science, BS</p>
		<p><strong>Colin Heinzmann</strong> - Computer Science & Engineering</p>
		<p><strong>Maggie Overstreet</strong> - Computer Science, BS and Physics, BA</p>
		<p><strong>Tiago Bozzetti</strong> - Computer Science</p>
		<p><strong>Ethan Vynalek</strong> - Computer Science, BS</p>
            </div>

        </div>
    </div>

  </body>
</html>
