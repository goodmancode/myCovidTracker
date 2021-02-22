# System Architecture 

## Design Document
### Overview
With My Covid Tracker, we aim to produce a predictive model for COVID-19 data with a user friendly front-end that provides users assistance with risk assessment. The system will consist of a machine learning model trained with COVID-19 data for the United States, a database to act as a conduit for the model’s data, and a web page that users can use to view predictions and get personalized risk assessment.
### Major classes
My Covid Tracker will have a ‘State’ class and ‘StateMetrics’ class. The ‘State’ class will consist of functions to get the name and metrics of a given state including average cases per day, predictions for a given number of days into the future, and the percent change in cases over a given interval. The ‘StateMetrics’ class will contain variables for predictions, average cases per day, and percent change as well as functions to calculate these metrics through interaction with the model. There will also be a ‘Risk Assessment’ class that will contain all of the fields necessary for calculating the risk assessment profile as well as a method that accesses the state metrics class.

![Class Diagram](https://github.com/goodmancode/myCovidTracker/blob/main/architecture/class_diagram.png)

#### StateMetrics
The State_Metrics class will hold all the values calculated by the state’s specific model. It will hold values such as the predictions for up to a month. The average number of cases per day, as well as other fields such as daily percent change and metadate of the model such as the accuracy of the model. The predict_days_out method will take in the number of days in the future to get a set of predictions from and return that amount of days’ worth of predictions as a list.

#### State 
The State class will hold the state name and the corresponding metrics. The metrics field is of the type State_Metrics which holds relevant metrics that will be used to calculate the risk assessment profiles. 

#### RiskAssessment
The Risk_Assessment Class will contain all the fields necessary for calculating the risk assessment as well as methods that assist in the calculation. All the fields will be filled in by user input into the front end. The methods will set the fields and check to make sure all input is valid. To calculate the risk assessment, the Risk_Assessment class will use the State_Metrics class to calculate the risk assessment for traveling to a specific state. 

### Data Design
We will have a database for user information and a database to store current COVID-19 information for the prediction model. The user database will store the user's personalized risk assessment information as well as their login credentials. The predicion model's database will contain COVID-19 data for each of the 50 United States and will include information about the number of cases at specific times. The actual prediction model will be trained with a data set stored in a .csv file pulled daily from the CDC. Python’s pandas library has a read .csv option and it is the file type we can best take advantage of for use with machine learning. Users may access this COVID-19 data because it is stored in the user accessible prediction model database. We found this database approach optimal as it allows for better interoperability and organization than data stored and accessed on a single machine and then sent to a user. 

![ER Diagram](https://github.com/goodmancode/myCovidTracker/blob/main/architecture/ER_diagram.png)

### User Interface
My Covid Tracker’s UI will be a webpage. The site will have a header containing the title of the project, account user/pass login, links to additional educational COVID resources, and a link to our project's GitHub. The middle-left body will hold dropdowns to manually select a US state, and select a county once state is selected. When a user selects a state, the webpage will display COVID-19 data for that state and provide risk assessment. This page will include the date the data had last been updated. It also will hold an interactive map of the US that will dynamically highlight and zoom to chosen state/county and will allow choosing state/county via mouse-click on the map. The middle-right body will hold all data and statistics, including a line graph with both historical COVID data as well as ML predictions. The user can select how many weeks in the future for the model to predict into. Case changes for user selections are represented both in percentage and numerically. The lower-left body will contain fields for risk factor entry. The risk factors will be entered first then a risk assessment in the lower-right body will be produced showing the likelihood of exposure based on the factors and location selected. This risk assessment can be saved to a user's profile if the user has created an account to track risk over time and save risk factor settings.

![UI Diagram](https://github.com/goodmancode/myCovidTracker/blob/main/architecture/UI_mockup_withUIDs.png)

### Resource Management
Resource management will not be of concern with My Covid Tracker as the model will only process small amounts of numeric data without the need for hardware acceleration. The resources required are well within the capabilities of the intended implementation environment.
### Security
My Covid tracker will not be susceptible to security breaches or untrustworthy data as the user accounts will be handled via Firebase and the only user input will be an integer containing their age which cannot threaten the system.
### Scalability
Scalability is not an issue as My Covid Tracker is not expected to grow beyond what it can handle in terms of users or database records.
### Interoperability
The COVID-19 dataset will be acquired from the CDC via their API and will be passed through our databases for the front-end to display. The dataset will also be sent to the prediction model regularly for training purposes. Our user account system, Firebase Auth, will handle account credentials and some user information. Users will access the My Covid Tracker Single-Page Application which will in turn interact with Firebase Auth, the Machine Learning Model, and the COVID-19 database.

![Container Diagram](https://github.com/goodmancode/myCovidTracker/blob/main/architecture/container_diagram.png)

![Context Diagram](https://github.com/goodmancode/myCovidTracker/blob/main/architecture/context_diagram.png)

![Component Diagram](https://github.com/goodmancode/myCovidTracker/blob/main/architecture/component_diagram.png)

### Error Processing
My Covid Tracker will have little room for error in regards to user input. The only area in which a user can cause an error would be when they are inputting data into the age field for personalized risk assessment and this would be handled by checking whether the input is a positive integer that is not beyond a realistic age.
### Fault Tolerance
My Covid Tracker will pull data from the CDC and if there are any failures with data requests the system will continue requests until the files are retrieved while having the front-end continue to display the old data. This should not be an issue since the date of the data’s last update will be shown to the user.