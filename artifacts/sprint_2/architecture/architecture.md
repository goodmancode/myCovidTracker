# System Architecture 

## Design Document
### Overview
With My Covid Tracker, we aim to produce a predictive model for COVID-19 data with a user friendly front-end that provides users assistance with risk assessment. The system will consist of a machine learning model trained with COVID-19 data for the United States, a database to act as a conduit for the model’s data, and a web page that users can use to view predictions and get personalized risk assessment.
### Major classes
My Covid Tracker will have a ‘State’ class and ‘StateMetrics’ class. The ‘State’ class will consist of functions to get the name and metrics of a given state including average cases per day, predictions for a given number of days into the future, and the percent change in cases over a given interval. The ‘StateMetrics’ class will contain variables for predictions, average cases per day, and percent change as well as functions to calculate these metrics through interaction with the model. There will also be a ‘Risk Assessment’ class that will contain all of the fields necessary for calculating the risk assessment profile as well as a method that accesses the state metrics class.
![Class Diagram](https://github.com/goodmancode/myCovidTracker/blob/main/artifacts/sprint_2/architecture/class_diagram.png)

#### StateMetrics
The State_Metrics class will hold all the values calculated by the state’s specific model. It will hold values such as the predictions for up to a month. The average number of cases per day, as well as other fields such as daily percent change and metadate of the model such as the accuracy of the model. The predict_days_out method will take in the number of days in the future to get a set of predictions from and return that amount of days’ worth of predictions as a list.

#### State 
The State class will hold the state name and the corresponding metrics. The metrics field is of the type State_Metrics which holds relevant metrics that will be used to calculate the risk assessment profiles. 

#### RiskAssessment
The Risk_Assessment Class will contain all the fields necessary for calculating the risk assessment as well as methods that assist in the calculation. All the fields will be filled in by user input into the front end. The methods will set the fields and check to make sure all input is valid. To calculate the risk assessment, the Risk_Assessment class will use the State_Metrics class to calculate the risk assessment for traveling to a specific state. 

### Data Design
The data set will be stored in a .csv file because Python’s pandas library has a read .csv option and it is the file type we can best take advantage of for use with machine learning.
### User Interface
My Covid Tracker’s UI will be a webpage. The site will have a login page and a dropdown menu that lets users select a state. When a user selects a state, the webpage will display COVID-19 data for that state and provide risk assessment. This page will include the date the data had last been updated. The user will also be able to input their own data for a more personalized risk assessment. The user data will include their age, whether they have been vaccinated, the types of venues they intend to visit, and whether they are immunocompromised. The site will also have a page referring users to additional educational resources to further prevent COVID transmission and allow users to mitigate risk on their own.
### Resource Management
Resource management will not be of concern with My Covid Tracker as the model will only process small amounts of numeric data without the need for hardware acceleration. The resources required are well within the capabilities of the intended implementation environment.
### Security
My Covid tracker will not be susceptible to security breaches or untrustworthy data as the user accounts will be handled via Firebase and the only user input will be an integer containing their age which cannot threaten the system.
### Scalability
Scalability is not an issue as My Covid Tracker is not expected to grow beyond what it can handle in terms of users or database records.
### Interoperability
The dataset will be acquired from the CDC via their API and will be passed through Firebase’s cloud platform for the front-end to display. The dataset will also be sent to the model regularly for training purposes.
### Error Processing
My Covid Tracker will have little room for error in regards to user input. The only area in which a user can cause an error would be when they are inputting data into the age field for personalized risk assessment and this would be handled by checking whether the input is a positive integer that is not beyond a realistic age.
### Fault Tolerance
My Covid Tracker will pull data from the CDC and if there are any failures with data requests the system will continue requests until the files are retrieved while having the front-end continue to display the old data. This should not be an issue since the date of the data’s last update will be shown to the user.