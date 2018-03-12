import os
import subprocess
import urllib2
import uuid
from flask import Flask, render_template, redirect, request, url_for, make_response
import redis


import boto

import time


# Video streaming location
raspberry_addr = 'REPLACE WITH RASPBERRY PUBLIC IP AND PORT'



# Redis connections
r = redis.Redis(host='REPLACE WITH REDIS URL', port='REPLACE WITH REDIS PORT', password='REPLACE WITH REDIS PASSWORD')
rediscounter = 'counter'
redistimestamp = 'timestamp'


html_start = """
<html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

<script type="text/JavaScript">
<!--
function TimedRefresh(t){
setTimeout("location.reload(true);", t);
}
//   -->
</script>
<body id="page-top" onload="JavaScript:TimedRefresh(60000);">


<nav class="navbar navbar-inverse navbar-fixed-top">
    <div class="container">
    <div class="navbar-header">
        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand">Piped Piper Project</a>
    </div>
    <div id="navbar" class="collapse navbar-collapse">
        <ul class="nav navbar-nav">
        <li class="active"><a href="#">Home</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
        </ul>
    </div><!--/.nav-collapse -->
    </div>
</nav>

    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div class="jumbotron">
      <div class="container">
        <h1>Pied Piper Home Intrusion Monitor</h1>
        <p>Below sections provide information for a Raspberry PI based home monitoring and intrusion device</p>
 
      </div>
    </div>


    

"""

html_end = """

    <section id="contact">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <h2>Contact us</h2>
            <p style="font-size:20px" class="lead">Tan Sin Lip sinlip@gmail.com</p>
          </div>
        </div>
      </div>
    </section>

</a>
</div>
</center>
</body>
</html>
"""

app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#777799"
GREEN = "#99CC99"

COLOR = GREEN



@app.route('/')
def mainmenu():
 
    print html_start

    html_mid = """
    <div class="container">
      <!-- Example row of columns -->

          <h2>Video Streamed from location</h2>
          <p> The video stream is from the RaspBerry location and is using the MJPEG mechanism. Resolution is 640x480 from a PI camera </p>


 
      </div>

      <hr>


    </div> <!-- /container -->


    </br>
    <center>
    """

    html_mid = html_mid + '<img src=' + raspberry_addr + '/?action=stream" />'


    # Use info from Redis to display intrusion info
    detect_intrude = r.get('intrusion')
  
    if int(detect_intrude) == 1:  
        intrude_timestamp = r.get('intrusion_timestamp')
        html_mid = html_mid + '</br>'
        html_mid = html_mid + '<p style="font-size:20px">Last Intrusion was detected at ' + time.ctime(int(float(intrude_timestamp))) + '</p>'
        



    return html_start + html_mid + html_end

if __name__ == "__main__":        
        app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))


