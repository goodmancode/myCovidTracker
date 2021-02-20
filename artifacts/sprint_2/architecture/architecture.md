# System Architecture 

## Design Document



## C4 Model



## Class Diagrams

(class_diagram.jpg)

### State_Metrics
The State_Metrics class will hold all the values calculated by the state’s specific model. It will hold values such as the predictions for up to a month. The average number of cases per day, as well as other fields such as daily percent change and metadate of the model such as the accuracy of the model. The predict_days_out method will take in the number of days in the future to get a set of predictions from and return that amount of days’ worth of predictions as a list.

### State 
The State class will hold the state name and the corresponding metrics. The metrics field is of the type State_Metrics which holds relevant metrics that will be used to calculate the risk assessment profiles. 

### Risk_Assessment
The Risk_Assessment Class will contain all the fields necessary for calculating the risk assessment as well as methods that assist in the calculation. All the fields will be filled in by user input into the front end. The methods will set the fields and check to make sure all input is valid. To calculate the risk assessment, the Risk_Assessment class will use the State_Metrics class to calculate the risk assessment for traveling to a specific state. 



## UI Mockup
