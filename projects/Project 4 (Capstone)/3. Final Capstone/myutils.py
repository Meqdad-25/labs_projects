"""
myutils.py  —  every function created in the DSB FT3 class
==========================================================

All functions below are copied VERBATIM from the in-class notebooks, labs, exercises
and the myutil*.py module files. Nothing has been edited.

The source file of each function is written above it.

Total: 44 functions.
"""

# ---------------------------------------------------------------------------
# imports used across the class notebooks
# ---------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from random import randint
from scipy.stats import skew

from sklearn.preprocessing import PowerTransformer
from sklearn.metrics import (r2_score, mean_squared_error,
                             accuracy_score, recall_score, precision_score, f1_score,
                             balanced_accuracy_score, classification_report,
                             ConfusionMatrixDisplay)

# statsmodels is only needed by the time-series functions (adf_test, autocorr_plots).
# It is imported inside a try block so this file still works if statsmodels is missing.
try:
    from statsmodels.tsa.stattools import adfuller
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
except ImportError:
    pass


# ==========================================================================
# generate_random_report  (v1 of 2)
# source: batch1 — 3_5_1_python-modules-and-scripting_v1-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def generate_random_report(count):
    """
    Generate a random list of count number
    
    Args:
        count (int): number of randoms in the list
    
    Returns:
        list: list of random values of length count
    """
    from random import randint
    # your code here
    # random_list=[]
    # for i in range(count):
    #     random_list.append(randint(1,100))
    # return  random_list
    # another way to do it:
    return [randint(1,100) for i in range(count)]


# ==========================================================================
# calculate_statistics  (v1 of 2)
# source: batch1 — 3_5_1_python-modules-and-scripting_v1-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def calculate_statistics(numbers):
    """
    Generate a dictonary of statistics,
    mean, median, min,max, length
    
    Args:
        list: a list
    
    Returns:
        disctionay: contains mean,median,min,max and length of the list
    """
    # Your code here
    # your function should return a dictionary of:
    # mean, median, minimum, maximum and sample size
    numbers.sort()
    mean=sum(numbers)/len(numbers)
    minimum=numbers[0]   # or min(numbers)
    maximum=numbers[-1]  # or max(numbers)
    sample_size = len(numbers)
    mid = len(numbers)//2
    if len(numbers)%2 == 0:
        median=(numbers[mid]+numbers[mid-1])/2
    else:
        median=numbers[mid]
    
    return  {'Mean':mean,'Median':median,'Min':minimum,'Max':maximum,
             'Sample Size':sample_size}


# ==========================================================================
# celsius_to_fahrenheit  (v1 of 2)
# source: batch1 — 3_5_1_python-modules-and-scripting_v1-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius temperature to Fahrenheit.
    
    Args:
        celsius (float): Temperature in Celsius
    
    Returns:
        float: Temperature in Fahrenheit
    """
    return (celsius * 9/5) + 32


# ==========================================================================
# fahrenheit_to_celsius  (v1 of 2)
# source: batch1 — 3_5_1_python-modules-and-scripting_v1-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def fahrenheit_to_celsius(fahrenheit):
    """
    Convert Fahrenheit temperature to Celsius.
    
    Args:
        fahrenheit (float): Temperature in Fahrenheit
    
    Returns:
        float: Temperature in Celsius
    """
    return (fahrenheit - 32) * 5/9


# ==========================================================================
# write_data_to_csv
# source: batch1 — 3_5_1_python-modules-and-scripting_v1-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def write_data_to_csv(data, filename):
    """
    Saves a list of dictionaries to a CSV file. 
    Appends seamlessly if the file exists; creates a new one with headers if it doesn't.
    """
    import os
    # convert the passed data into a DataFrame
    df2= pd.DataFrame(data)
        
    # Check if the file already exists on your system using os.path.exists
    file_exists = os.path.exists(filename)
        
    if file_exists:
        # Append data: 'a' mode, turn off headers so columns aren't duplicated in mid-file
        df2.to_csv(filename, mode='a', header=False, index=False)
        print(f'File {filename} has been successfully updated!')
    else:
        # Create new file: 'w' mode (default), write the header columns
        df2.to_csv(filename, mode='w', header=True, index=False)
        print(f'File {filename} has been successfully created!')


# ==========================================================================
# strip_dollar_sign
# source: batch1 — 3_8_1_cleaning-data-with-pandas_v_6-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def strip_dollar_sign(x):
    return x.replace("$","")


# ==========================================================================
# calc_vat
# source: batch1 — 3_8_1_cleaning-data-with-pandas_v_6-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def calc_vat(row):
    return row['unit_price'] * row['quantity'] * 0.10
    # write code here


# ==========================================================================
# fill_generation
# source: batch1 — 3_8_1_cleaning-data-with-pandas_v_6-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def fill_generation(row):
    # If customer_generation already has a value (is not null), do nothing
    # To safely test if an individual cell is empty use pd.notna()
    if pd.notna(row['customer_generation']):
        return row['customer_generation']

    # Grab the birth year
    year = row['customer_birth_year']
    
    # Return birth year ranges
    if (year >=1950) and (year <=1964):
        return 'Baby Boomers'
    elif 1965 <= year <= 1979:
        return 'Gen X'
    elif 1980 <= year <= 1989:
        return 'Older Millennials'
    elif 1990 <= year <=1994:
        return 'Younger Millennials'
    elif 1995 <= year <=2001:
        return 'Gen Z'


# ==========================================================================
# profit_margin
# source: batch1 — 3_8_E1_Exercise-Cleaning-data-pandas-v1.ipynb
# ==========================================================================
def profit_margin(row):
    return row['profit']/row['sales']


# ==========================================================================
# margin_categorization
# source: batch1 — 3_8_E1_Exercise-Cleaning-data-pandas-v1.ipynb
# ==========================================================================
def margin_categorization(row):
    prft = row['profit_margin']
    if prft < 0:
        return 'unprofitable'
    elif prft == 0:
        return 'break even'
    elif prft > 0:
        return 'profitable'


# ==========================================================================
# time_cetegories
# source: batch1 — Lab_Data_Exploration_Python-HMA-v_2_1.ipynb
# ==========================================================================
def time_cetegories(transaction_time):
    hour  = transaction_time.hour
    if 5<= hour <12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Noon'
    elif 17<= hour < 19:
        return 'Evening'
    else:
        return 'Night'


# ==========================================================================
# scroll
# source: batch2 — 5_2_Selenium_v_5_2-InClass-DSB2FT.ipynb
# NOTE: this function was left unfinished in the original notebook
#       (no body was written). Kept verbatim but commented out so
#       this file still imports.
# ==========================================================================
# def scroll(driver):


# ==========================================================================
# get_stars
# source: batch2 — 5_1_E3_Exercise3-InClass-Guided-Webscaping-v_2.ipynb
# ==========================================================================
def get_stars(x):   
    return len(x.find_all('span', class_ = 'star fill' ))


# ==========================================================================
# SLR
# source: batch2 — 6_4_E1_Exercise_regression.ipynb
# ==========================================================================
def SLR(X,y):
    x_avg = X.mean() 
    y_avg = y.mean()
    x_std = X.std()
    y_std = y.std()
    corr = np.corrcoef(X,y)[0,1]
    coff = corr * (y_std/x_std)
    intr = y_avg - (coff*x_avg)

    return coff, intr


# ==========================================================================
# r2_adj
# source: batch2 — 6_4_E1_Exercise_regression.ipynb
# ==========================================================================
def r2_adj(r2, n, k):
    return 1 - ((1-r2)*(n-1)/(n-k-1))


# ==========================================================================
# skew_calc  (v1 of 2)
# source: batch2 — 6_8_E1_Transformation_Exercise.ipynb
# ==========================================================================
def skew_calc(df):
    """
    Diagnoses skewness for every numeric column in a DataFrame and recommends a transformation based on the column's skewness and
    minimum value. Binary, encoded, and ID columns are excluded, since skewness isn't a meaningful for them.
    It returns a DataFrame with the following columns:
    Feature, Skewness, Degree, Direction, Recommended Transformation
    """
    results = []
    for col in df.select_dtypes(include = np.number).columns:
        
        if df[col].nunique() <= 2:
            continue
        if col.lower() in ['id','index'] or col.lower().endswith('_id'):
            continue

        skewness = df[col].skew()
        minimum = df[col].min()

        
        if abs(skewness) >= 1:
            degree = 'Highly Skewed'
        elif abs(skewness) >= 0.5:
            degree = 'Moderately Skewed'
        else:
            degree = 'Normal'

        
        if skewness > 0:
            direction = 'Positive'
        else:
            direction = 'Negative'

        
        if degree == 'Normal':
            recommendation = 'No Recomm'
        elif minimum > 0:
            recommendation = 'Box-Cox or Yeo-Johnson'
        elif minimum == 0:
            recommendation = 'log(x+1) or Yeo-Johnson'
        else:
            recommendation = 'Yeo-Johnson'

        results.append({
            'Feature' : col,
            'Skewness' : skewness,
            'Degree' : degree,
            'Direction' : direction,
            'Recommended Transformation' : recommendation
        })
    return pd.DataFrame(results)


# ==========================================================================
# plot_transformations
# source: batch2 — 6_8_E1_Transformation_Exercise.ipynb
# ==========================================================================
def plot_transformations(df, skew_table):
    """
    Applies the recommended transformation to each column, then plots the before and after 
    distributions side by side with the skewness degree on each subplot.
    """


# ==========================================================================
# evaluate_model  (v1 of 2)
# source: batch2 — 6_9_E1_Regularization_Exercise.ipynb
# ==========================================================================
def evaluate_model(model, X_train, X_test, y_train, y_test, model_name="Model"):
    """
    Predicts and calculates R2 and RMSE for both train and test sets.
    Then prints the Train R2 and RMSE along with the Test R2 and RMSE
    """
    print(f"--- {model_name} Performance ---")
    
    # TODO: Generate predictions for both X_train and X_test
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # TODO: Calculate R2 for train and test
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    # TODO: Calculate RMSE for train and test
    train_rmse = mean_squared_error(y_train, y_train_pred)**0.5
    test_rmse = mean_squared_error(y_test, y_test_pred)**0.5
    
    # TODO: Print the results clearly
    print(f'score for  train = {train_r2}, and for test = {test_r2}')
    print(f'rmse for train = {train_rmse}, and for test = {test_rmse}')


# ==========================================================================
# evaluate_skewness  (v1 of 2)
# source: batch2 — 6_10_1_GridSearch_Pipelines_Solution.ipynb
# ==========================================================================
def evaluate_skewness(dataframe):
    numeric_cols = dataframe.select_dtypes(include=np.number).columns
    results = []
    
    for col in numeric_cols:
        skew_val = dataframe[col].skew()
        min_val = dataframe[col].min()
        
        # Determine skew type
        if skew_val > 0.5:
            skew_type = "Right-Skewed"
        elif skew_val < -0.5:
            skew_type = "Left-Skewed"
        else:
            skew_type = "Symmetrical"
            
        # Recommend transformation
        if skew_type == "Symmetrical":
            rec = "None needed"
        elif min_val > 0:
            rec = "Log, Box-Cox or Yeo-Johnson"
        elif min_val == 0:
            rec = "Log or Yeo-Johnson"
        else:
            rec = "Yeo-Johnson" # Yeo-Johnson handles zero and negative numbers!
            
        results.append([col, skew_type, skew_val, rec])
        
    return pd.DataFrame(results, columns=["Feature", "Skewness Type", "Skewness Value", "Recommendation"])


# ==========================================================================
# evaluation
# source: batch3 — 6_16_imbalanced-data-solution.ipynb
# ==========================================================================
def evaluation(X_test, y_test, preds, model):
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, cmap='Blues')
    
    b_acc = balanced_accuracy_score(y_test, preds)
    recall = recall_score(y_test, preds, pos_label = ">50K")
    prec = precision_score(y_test, preds, pos_label = ">50K")
    f1 = f1_score(y_test, preds, pos_label = ">50K")

    print(f'balanced_accuracy: {b_acc}')
    print(f'recall: {recall}')
    print(f'precision: {prec}')
    print(f'f1 score: {f1}')

    return {
        'balanced_accuracy': b_acc,
        'recall': recall,
        'precision': prec,
        'f1_score': f1
    }


# ==========================================================================
# print_classification_metrics
# source: batch3 — 6_15_E1_Logistic_Regression.ipynb
# ==========================================================================
def print_classification_metrics(y_true, y_pred):
    """
    Prints accuracy, recall, precision, specificity and F1,
    with an explanation.
    """
    accuracy = accuracy_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    specificity = recall_score(y_true, y_pred, pos_label=0)
    f1 = f1_score(y_true, y_pred)

    print(f"Accuracy : {accuracy}")
    print("Overall, how often the model is correct.")
    print()

    print(f"Recall : {recall}")
    print("Of the passengers who really survived, how many the model found.")
    print()

    print(f"Precision : {precision}")
    print("Of the passengers the model said survived, how many really did.")
    print()

    print(f"Specificity : {specificity}")
    print("Of the passengers who really died, how many the model got right.")
    print()

    print(f"F1 score : {f1}")
    print("The balance between precision and recall.")


# ==========================================================================
# print_number
# source: batch3 — 6_17_1_svms-v2-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def print_number(index):
    plt.imshow(digits.images[index],
               # cmap=plt.cm.gray_r,
               interpolation='nearest')
    plt.show()
    print(f'The model guessed this was: {df["Predict"].iloc[index]}.')
    print(f'This actually is: {df["Actual"].iloc[index]}.')
    print()


# ==========================================================================
# dist_plotter
# source: batch3 — 6_19_1_central-limit-theorem-v2-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def dist_plotter(sample,bins=50,kde=True):
    fig, ax = plt.subplots(figsize=(4,3))
    sns.histplot(sample, bins=bins, kde=kde)
    plt.show()


# ==========================================================================
# sampler
# source: batch3 — 6_19_1_central-limit-theorem-v2-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def sampler(population, n=30, k=1000):
    sample_means = []
    for i in range(k):
        sample = np.random.choice(population,size = n , replace=True)
        sample_means.append(np.mean(sample))
    
    return sample_means


# ==========================================================================
# f
# source: batch3 — 02-gradient-descent-solution.ipynb
# ==========================================================================
def f(x):
    return -np.log(x) / (1 + x)


# ==========================================================================
# f_deriv
# source: batch3 — 02-gradient-descent-solution.ipynb
# ==========================================================================
def f_deriv(x):
    return -(1 + 1/x - np.log(x)) / (1 + x)**2


# ==========================================================================
# beta_1_gradient
# source: batch3 — 02-gradient-descent-solution.ipynb
# ==========================================================================
def beta_1_gradient(x, y, beta_1, beta_0):
    grads = -x * (y - (beta_1*x + beta_0))
    return 2 * np.mean(grads)


# ==========================================================================
# update_beta_1
# source: batch3 — 02-gradient-descent-solution.ipynb
# ==========================================================================
def update_beta_1(beta_1, alpha, gradient):
    beta_1 = beta_1 - alpha * gradient
    return beta_1


# ==========================================================================
# check_update
# source: batch3 — 02-gradient-descent-solution.ipynb
# ==========================================================================
def check_update(beta_1, updated_beta_1, tolerance = 0.1):
    return abs(beta_1 - updated_beta_1) < tolerance


# ==========================================================================
# gradient_descent
# source: batch3 — 02-gradient-descent-solution.ipynb
# ==========================================================================
def gradient_descent(x, y, beta_1 = 0, alpha = 0.01, max_iter = 100):
    # Set converged = False
    converged = False
    
    # Iterate through our observations.
    step = 0
    while not converged:
        
        # Calculate gradient
        gradient = beta_1_gradient(x, y, beta_1, 200000)
        
        # Update beta_1
        updated_beta_1 = update_beta_1(beta_1, alpha, gradient)
        
        # Check for convergence
        converged = check_update(beta_1, updated_beta_1)
        
        # Overwrite beta_1
        beta_1 = updated_beta_1
        
        # Print out current step findings
        print(f'Iteration {step} with beta_1 value of {beta_1}.')
        
        # If we've converged, let us know!
        if converged:
            print(f'Our algorithm converged after {step} iterations with a beta_1 value of {beta_1}.')
        else:
            step += 1
            
        # If we exceed our step limit, break!
        if step > max_iter:
            break
        
    # If we didn't converge by the end of our loop, let us know!
    if not converged:
        print("Our algorithm did not converge, so do not trust the value of beta_1.")
    
    # Return beta_1
    return beta_1


# ==========================================================================
# plot_dendrogram
# source: batch4 — 02-dbscan-agglom-clustering-solution.ipynb
# ==========================================================================
def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)


# ==========================================================================
# autocorr_plots
# source: batch4 — 8.2.1 timeseries-autocorrelations-v2-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def autocorr_plots(y, lags=None):
    fig, ax = plt.subplots(ncols=2, figsize=(12, 4), sharey=True)
    plot_acf(y, lags=lags, ax=ax[0])
    plot_pacf(y, lags=lags, ax=ax[1])
    return fig, ax


# ==========================================================================
# adf_test  (v1 of 2)
# source: batch4 — 8.2.1 timeseries-autocorrelations-v2-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def adf_test(series,title=''):
    """
    Pass in a time series and an optional title, returns an ADF report
    """
    print(f'Augmented Dickey-Fuller Test: {title}')
    result = adfuller(series.dropna(),autolag='AIC') # .dropna() handles differenced data
    
    labels = ['ADF test statistic','p-value','# lags used','# observations']
    out = pd.Series(result[0:4],index=labels)

    for key,val in result[4].items():
        out[f'critical value ({key})']=val
        
    print(out.to_string())          # .to_string() removes the line "dtype: float64"
    
    if result[1] <= 0.05:
        print("Strong evidence against the null hypothesis")
        print("Reject the null hypothesis")
        print("Data has no unit root and is stationary")
    else:
        print("Weak evidence against the null hypothesis")
        print("Fail to reject the null hypothesis")
        print("Data has a unit root and is non-stationary")


# ==========================================================================
# show_predictions
# source: batch4 — 9.5.2 transfer-learning-v1-InClass-DSB2FT-Completed.ipynb
# ==========================================================================
def show_predictions(model, dataset, n=6, title="Predictions"):
    images, labels = next(iter(dataset))
    preds = model.predict(images[:n], verbose=0)
    pred_labels = np.argmax(preds, axis=1)

    fig, axes = plt.subplots(1, n, figsize=(14, 3))
    for i in range(n):
        axes[i].imshow(images[i].numpy().astype("uint8"))
        true_name = class_names[labels[i].numpy()]
        pred_name = class_names[pred_labels[i]]
        color = "green" if pred_name == true_name else "red"
        axes[i].set_title(f"true: {true_name}\npred: {pred_name}", color=color, fontsize=9)
        axes[i].axis("off")
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()


# ==========================================================================
# adf_test  (v2 of 2)
# source: batch4 — ARIMA_SARIMAX_Lab.ipynb
# ==========================================================================
def adf_test(series, title=''):
    """
    Pass in a time series and an optional title, returns an ADF report
    """
    print(f'Augmented Dickey-Fuller Test: {title}')
    result = adfuller(series.dropna(),autolag='AIC') # .dropna() handles differenced data
    
    labels = ['ADF test statistic','p-value','# lags used','# observations']
    out = pd.Series(result[0:4],index=labels)

    for key,val in result[4].items():
        out[f'critical value ({key})']=val
        
    print(out.to_string())          # .to_string() removes the line "dtype: float64"
    
    if result[1] <= 0.05:
        print("Strong evidence against the null hypothesis")
        print("Reject the null hypothesis")
        print("Data has no unit root and is stationary")
    else:
        print("Weak evidence against the null hypothesis")
        print("Fail to reject the null hypothesis")
        print("Data has a unit root and is non-stationary")


# ==========================================================================
# evaluate_model_performance
# source: batch4 — lab-classification-left-handedness_v3.ipynb
# ==========================================================================
def evaluate_model_performance(model, X_test, y_test, target_names):
    """
    Generates predictions, displays the classification report and confusion matrix.
    """

    # Generate predictions
    y_pred = model.predict(X_test)

    # Display the Classification Report
    print("======================================================")
    print("                CLASSIFICATION REPORT                 ")
    print("======================================================")
    print(classification_report(y_test, y_pred, target_names=target_names, zero_division=0.0))

    # Display Confusion Matrix
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=target_names, cmap='Blues')
    plt.title("Confusion Matrix")
    plt.show()


# ==========================================================================
# celsius_to_fahrenheit  (v2 of 2)
# source: myutilss.py
# ==========================================================================
def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius temperature to Fahrenheit.

    Args:
        celsius (float): Temperature in Celsius

    Returns:
        float: Temperature in Fahrenheit
    """
    return (celsius * 9/5) + 32


# ==========================================================================
# fahrenheit_to_celsius  (v2 of 2)
# source: myutilss.py
# ==========================================================================
def fahrenheit_to_celsius(fahrenheit):
    """
    Convert Fahrenheit temperature to Celsius.

    Args:
        fahrenheit (float): Temperature in Fahrenheit

    Returns:
        float: Temperature in Celsius
    """
    return (fahrenheit - 32) * 5/9


# ==========================================================================
# generate_random_report  (v2 of 2)
# source: myutilss.py
# ==========================================================================
def generate_random_report(count):
    """
    Generate Random Report.

    Args:
        count 

    Returns:
        whta sould be returned ig
    """

    # your code here
    emplist = []
    for i in range(count):
        random_num = randint(1,100)
        emplist.append(random_num)
        
    return  emplist


# ==========================================================================
# calculate_statistics  (v2 of 2)
# source: myutilss.py
# ==========================================================================
def calculate_statistics(numbers):
    """
    generate a dictonary of statistics, mean, median, min, max , length.

    Args:
        list: a list
    Returns:
        dictonary: contains mean, median, min, max and length of the list
    """
    # Your code here
    # your function should return a dictionary of:
    # mean, median, minimum, maximum and sample size (length)

    numbers.sort()
    
    mean = sum(numbers)/len(numbers)
    minimum = min(numbers)
    maximum = max(numbers)
    sample_size = len(numbers)
    
    mid = len(numbers) // 2
    if len(numbers) % 2 == 0:
        median = (numbers[mid]+numbers[mid-1])/2
    else:
        median = numbers[mid]
        
    
    return  {'Mean': mean, 'Median': median, 'Min': minimum, 'Max': maximum, 'Sample Size': sample_size}


# ==========================================================================
# skew_calc  (v2 of 2)
# source: myutils.py
# ==========================================================================
def skew_calc(df):
    """
    Diagnoses skewness for every numeric column in a DataFrame and recommends a transformation based on the column's skewness and
    minimum value. Binary, encoded, and ID columns are excluded, since skewness isn't a meaningful for them.
    It returns a DataFrame with the following columns:
    Feature, Skewness, Degree, Direction, Recommended Transformation
    """
    results = []
    for col in df.select_dtypes(include = np.number).columns:

        if df[col].nunique() <= 2:
            continue
        if col.lower() in ['id','index'] or col.lower().endswith('_id'):
            continue

        skewness = df[col].skew()
        minimum = df[col].min()


        if abs(skewness) >= 1:
            degree = 'Highly Skewed'
        elif abs(skewness) >= 0.5:
            degree = 'Moderately Skewed'
        else:
            degree = 'Normal'


        if skewness > 0:
            direction = 'Positive'
        else:
            direction = 'Negative'


        if degree == 'Normal':
            recommendation = 'No Recomm'
        elif minimum > 0:
            recommendation = 'Box-Cox or Yeo-Johnson'
        elif minimum == 0:
            recommendation = 'log(x+1) or Yeo-Johnson'
        else:
            recommendation = 'Yeo-Johnson'

        results.append({
            'Feature' : col,
            'Skewness' : skewness,
            'Degree' : degree,
            'Direction' : direction,
            'Recommended Transformation' : recommendation
        })
    return pd.DataFrame(results)


# ==========================================================================
# evaluate_skewness  (v2 of 2)
# source: myutil.py
# ==========================================================================
def evaluate_skewness(dataframe, unique_threshold=10,filter_result=False,high_skew_only=False,no_skew_only=False):
    '''
    The function will return skewness value for any numeric continous column.
    
    unique_threshold: it will ignore to check skewness for any binary or ordinal 
    features based on the number of unique values in that numeric column.
    if it is less than the unique_threshold(default is 10), then ignore them.

    filter_result: whether to return columns that needs skewness fix only
    high_skew_only: whether to return columns with high skewness only
    '''
    numeric_cols = dataframe.select_dtypes(include=np.number).columns
    results = []
    
    for col in numeric_cols:
        # Count unique values to identify binary or ordinal features
        num_unique = dataframe[col].nunique()
        
        # Skip if binary (exactly 2 unique values) or ordinal (low unique value count)

        if num_unique <= unique_threshold:
            continue
            # continue: This is a Python keyword used inside loops. It tells Python to stop what it 
            # is doing with the current column right now, skip the rest of the code below it, and 
            # jump immediately to the next column in the loop
        
        skew_val = round(dataframe[col].skew(),2)
        min_val = dataframe[col].min()
        
        # Determine skew type
        if skew_val > 0.5:
            skew_type = "Right-Skewed"
        elif skew_val < -0.5:
            skew_type = "Left-Skewed"
        else:
            skew_type = "Symmetrical"

        # Determine skew level
        if skew_val > 1 or skew_val < -1:
            skew_level = "Highly skewed"
        elif skew_val > 0.5 or skew_val < -0.5:
            skew_level = "Moderately skewed"
        else:
            skew_level = ""
            
        # Recommend transformation
        if skew_type == "Symmetrical":
            rec = "None needed"
        elif min_val > 0:
            rec = "Log1p, Box-Cox or Yeo-Johnson"
        elif min_val == 0:
            rec = "Log1p or Yeo-Johnson"
        else:
            rec = "Yeo-Johnson" # Yeo-Johnson handles zero and negative numbers!
            
        results.append([col, skew_type, skew_val, skew_level, rec])
    df_return=pd.DataFrame(results, columns=["Feature", "Skewness Type", "Skewness Value", "Skewness level", "Recommendation"])
    df_return = df_return.sort_values(by=["Skewness level"], ascending=[True])
    # return based on parameter passed to function to filter or high skew only
    print("Note: Skewness will be null if a column contains any null value")
    if no_skew_only:
        return df_return[(df_return['Skewness Type']=='Symmetrical')].reset_index(drop=True)
    elif filter_result and high_skew_only:
        return df_return[(df_return['Skewness Type']!='Symmetrical') & (df_return['Skewness level'] == "Highly skewed")].reset_index(drop=True)
    elif filter_result:
        return df_return[(df_return['Skewness Type']!='Symmetrical')].reset_index(drop=True)
    else:
        return df_return


# ==========================================================================
# check_skew_before_after
# source: myutil.py
# ==========================================================================
def check_skew_before_after(df_skew,dataframe,method='yeo-johnson'):
    '''
    this function will check skewness before and after
    it will not modify any feature, just check skew values
    df_skew: skewness dataframe that is genereated by evaluate_skewness function
    dataframe: dataframe of your features
    method: ['yeo-johnson','box-cox'] , default it 'yeo-johnson'
    '''

    # get the list of current skewness values for all the passed features
    df_skew=df_skew[df_skew['Recommendation']!='None needed']
    skew_before=df_skew['Skewness Value'].to_list()
    skew_after=[]

    
    list_of_col=df_skew['Feature'].to_list()
    for col in dataframe[list_of_col]:
        min_val = dataframe[col].min()
        if method=='yeo-johnson':
            pt = PowerTransformer(method='yeo-johnson')
        elif method=='box-cox':
            if min_val <= 0:
                return f"can't use box-cox with 0 or negative valued column {col}"
            else:
                pt = PowerTransformer(method='box-cox')
        skew_after.append(round(skew(pt.fit_transform(dataframe[[col]]))[0], 2))
    df_return=pd.DataFrame({
        "Feature" : list_of_col,
        "Skew Before" : skew_before,
        "Skew After" :skew_after
    })
    return df_return


# ==========================================================================
# evaluate_model  (v2 of 2)
# source: myutil2.py
# ==========================================================================
def evaluate_model(model, X_train, X_test, y_train, y_test, model_name="Model"):
    """
    Predicts and calculates R2 and RMSE for both train and test sets.
    Then prints the Train R2 and RMSE along with the Test R2 and RMSE
    """
    print(f"--- {model_name} Performance ---")
    
    # Generate predictions for both X_train and X_test
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Calculate R2 for train and test
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    
    # Calculate RMSE for train and test
    train_rmse = mean_squared_error(y_train, y_train_pred)**0.5
    test_rmse = mean_squared_error(y_test, y_test_pred)**0.5
    
    # Print the results clearly
    print(f'score for  train = {train_r2}, and for test = {test_r2}')
    print(f'rmse for train = {train_rmse}, and for test = {test_rmse}')

