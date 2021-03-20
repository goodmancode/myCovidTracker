# Hyper Parameter Tuning
To test the effects of the parameters (alpha, normalize) on different state models, three states (Florida, California, and Michigan) were tested with different forms of scaling. Most states' historical data follow the same *S* shaped curve so the results of this experimentation usually followed the same patterns for all states. The goal was to find a distribution that after 200 iterations, produced probabilities that fell towards lesser error values.

The three forms of scaling were Standard Scaling (the method originally used when the model was created), MinMaxScaling and just setting the *normalize* parameter to *True*. 

## Prediction Data
In previous iterations of the model, 60 data points were set aside. The first thirty which contained data points leading up the last thirty days were predicted on yielding pretty accurate results based on already existing data. The model then predicted thirty days into the future using the last thirty days of data. 

It turns out, only using the last thirty days as prediction data yielded better results as the model had more data to train and evaluate on. 

## Alpha
Different alpha values were tested but no matter the scaling method, the alpha value always stayed between (0, 0.001]. 

The scoring method used to evaluate the model was Mean Squared error as the model uses error based learning. Accuracy (R^2) was not very helpful because the accuracy was high, but MSE would return larger and larger values on certain models.

## Normalization
The final model will be using Ridge regression with a best fit alpha and *normalize* equal to *true*. This is because the regularization parameter penalizes based on the magnitude of the x values. If every value is between 0 and 1, it makes it easier to penalize these larger values. 
![FL_normalize.png](https://github.com/goodmancode/myCovidTracker/blob/main/backend/distributions/FL_normalize.png) ![CA_normalize.png](https://github.com/goodmancode/myCovidTracker/blob/main/backend/distributions/CA_normalize.png)  ![MI_normalize.png](https://github.com/goodmancode/myCovidTracker/blob/main/backend/distributions/MI_normalize.png)

## MinMaxScaler
Using the MinMaxScaler yielded distributions a bit worse than the normalized model but had less probability of smaller error values.

## StandardScaler
The old way of doing things by using the standard scaler yielded the worst distributions because the data **does not** follow a normal curve and does not need to based on the nature of it being time series data. 
