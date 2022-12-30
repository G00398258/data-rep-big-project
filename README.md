# Data Representation - Big Project
***  
**Student Name:** Gillian Kane-McLoughlin | **Student Number:** G00398258  
<br>
### Description
***  
This repository will contain my submission for the Data Representation Big Project (Winter 2022).  
<br>
For this project, I have made a Flask server that has a RESTful API and can perform CRUD operations on three separate database tables. There is also an accompanying web interface, which uses AJAX calls to perform these operations.  
<br>
Please note that this API has been hosted on pythonanywhere.com and can be accessed at the below link:  
http://g00398258.pythonanywhere.com/survey.html  
<br>
  
### Background Information  
***  
I work for a team in Dell, whose primary function is to run and then analyse the results of a quarterly survey called the IT Pulse. We present the results of this survey to product managers, engineers and designers, and use it to gauge team member sentiment around the IT products available to them through a scoring system.  
<br>
We currently use a third party survey tool to host the survey, which requires us to manually export the results and import them into our SQL database, but recently my manager and I have been talking about ways in which we could host the survey ourselves to simplify the process. With this project, and using the lecturer's examples as my base code, I decided to build a basic API for that purpose to see what it might look like and how it would work.  
<br>
Upon loading the interface, the user will be invited to take a survey. They can also view the current survey results (minus Employee IDs, as these would be private) and statistics around the survey results, including the average scores as they stand, responses by departments, the laptop models belonging to users who are providing negative laptop scores and employee information for users who consent to sharing their contact information for further follow up post survey (this is the last question they answer in the survey). 
<br>  
Aftewards, the user has a chance to amend their responses or delete them, but once they leave this page they cannot do so again (nor can they delete or alter responses from other employees). The user can then see the updated results and statistics again if they wish, or they can choose to exit. I have entered a handful of dummy responses in the DB so there is something to show if you decide to view the results/stats before taking the survey.  
<br>
Please bare in mind that this is not the finished product. I would have liked to have done more with the survey results (e.g. export results to csv files, populate charts from the data, create word clouds and do some natural language processing on the text box responses, etc.) and do some authentication (e.g. confirm EmployeeID exists in the DB, limit how many times an employee can take the survey in a certain time frame, etc.) but due to time constraints I had to settle for a more basic API. I will continue to work on adding additional functionality to this API with a view to putting it forward to be considered by my manager as a possible solution to our survey hosting issues.  
<br>
### Note on Interacting with the API  
***  
When you opt to take the survey, please note that EmployeeID (the first input box) must be a number between 1 & 20 (as I got tired of making up employee data after doing 20. I will have over 100,000 available to me at work when I connect this API to our SQL database).  
<br>
Andrew - I made you a Dell employee for this exercise with EmployeeID 20. Please feel free to use this!  
<br>
### Basic Instructions on Running the Code  
***  
To Run Locally:  
- Download the contents of this GitHub repository and navigate to the relevant directory on your PC using the command line  
- Use the example structure in the dbconfig_template.py file to make a new file called db_config.py (name must be exact)  
- Fill in the relevant host, user, password and database information as per your setup on the db_config.py file  
- On the command line, run 'python survey_DAO.py' to create the required SQL tables and (optionally) database  
	- NOTE: please check lines 325 & 326 of survey_DAO.py in case these lines have been commented out before running  
	- The message 'Hello from surveyDAO' will be printed to the console upon successful execution  
- Back on the command line, run 'python server_application.py' to start the server  
	- If any errors are encountered, run 'pip install -r requirements.txt' and retry the above command  
- Open your browser and go to http://127.0.0.1:5000/ to confirm the server is running  
- You can then go to http://127.0.0.1:5000/survey.html to interact with the API  
<br>

To Run on Python Anywhere:  
- In your browser, go to http://g00398258.pythonanywhere.com/survey.html  
<br>

### Contents  
***
- HTML (subfolder containing the below HTML pages and images that make up the web interface of the API)  
	- images (sub folder containing any images used in the web pages)  
	- goodbye.html  
	- survey.html  
- .gitignore  
- README.md  
- dbconfig_template.py  
- requirements.txt  
- server_application.py  
- survey_DAO.py  
<br>  

### Software Information  
***  
The back end code for this project was written in Python (version 3.8.8) and compiled in Visual Studio Code (version 1.74.0). The HTML, CSS & Javascript used in the front end user interface was also compiled in Visual Studio Code.  
<br>  
Please see file requirements.txt for information on the Python modules used in this project.  
<br>  

## End  
***
