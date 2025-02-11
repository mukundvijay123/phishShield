# PhishShield
ML tool to detect phishing websites.

##### Team: Mukund V, M Nithyashree, Krupa P Nadgir

### Problem Statement
Detecting Phishing Attempts Using Machine Learning and Deep Learning Techniques

### Objective:
Develop a machine learning-based system to automatically identify and classify phishing attempts in email communications or web links, minimizing false positives and ensuring high detection accuracy.

## Outcomes:
- A machine learning model that accurately classifies phishing attempts with high precision and recall.
- An evaluation report detailing the model's performance metrics and comparison with baseline methods.
- A prototype system that integrates with existing security infrastructure and provides actionable insights for end-users.
- Development and deployment of end-to-end solutions to verify if a website is safe or malicious.

## Prototype Development
###	Flask Server Implementation:
- URL Submission Handling: Create a Flask route to handle POST requests from the frontend. This route will process the submitted URL, check it against the SQLite database, and use the Random Forest model if necessary.
- Result Display: After processing, return the result (phishing or legitimate) to the frontend for display.
-	View History Endpoint: Develop an additional route to handle GET requests for viewing history. This endpoint should query MongoDB to retrieve the history of URL submissions and their results for the user.

### Database Integration:
○	SQLite Integration:
  Set up and populate the SQLite database with blacklist and whitelist entries. Implement the logic to query this database to check if the URL is in either list.

○	MongoDB Integration:
  Configure MongoDB to store URL submission history and results. Implement functionality to insert new entries and retrieve historical data. Ensure that each URL submission and its classification result are stored in MongoDB, along with relevant metadata such as timestamps.

###	Parameter Extraction in Docker Container:
○	Deploy a Docker container specifically for parameter extraction. Configure the container to run in read-only mode to enhance security and ensure that it only has access to necessary resources.

○	Use gVisor as a sandbox to isolate the container, providing an additional layer of security and resource isolation.

○	Ensure the container performs feature extraction efficiently and securely, interfacing correctly with the rest of the system.

###	Machine Learning Integration:
Load the pre-trained Random Forest model into the Flask application. Implement the logic to use the model to classify URLs that are not found in the SQLite or MongoDB databases.
  

![image](https://github.com/user-attachments/assets/b7e645eb-f8de-47ca-8db2-891ff2fa9e3e)


## Sample Outputs:
1. Legitimate Website
   ![image](https://github.com/user-attachments/assets/c08ecf8a-37af-433c-b74b-a30ee27036f1)

3. Phishing Website
   ![image](https://github.com/user-attachments/assets/a8a6ed3e-b89d-49be-bc18-905c37ba2cc9)

5. View History
   ![image](https://github.com/user-attachments/assets/a76bf1c2-e8fc-4143-a40c-12bcff6c26c5)

