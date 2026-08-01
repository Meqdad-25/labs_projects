import pandas as pd
import numpy as np
from scipy.stats import skew
from sklearn.preprocessing import PowerTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Custom Skewness Function
def evaluate_skewness(dataframe, unique_threshold=10, filter_result=False, high_skew_only=False, no_skew_only=False):
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

        skew_val = round(dataframe[col].skew(), 2)
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
            rec = "Yeo-Johnson"  # Yeo-Johnson handles zero and negative numbers!

        results.append([col, skew_type, skew_val, skew_level, rec])
    df_return = pd.DataFrame(results, columns=["Feature", "Skewness Type", "Skewness Value", "Skewness level", "Recommendation"])
    df_return = df_return.sort_values(by=["Skewness level"], ascending=[True])
    # return based on parameter passed to function to filter or high skew only
    print("Note: Skewness will be null if a column contains any null value")
    if no_skew_only:
        return df_return[(df_return['Skewness Type'] == 'Symmetrical')].reset_index(drop=True)
    elif filter_result and high_skew_only:
        return df_return[(df_return['Skewness Type'] != 'Symmetrical') & (df_return['Skewness level'] == "Highly skewed")].reset_index(drop=True)
    elif filter_result:
        return df_return[(df_return['Skewness Type'] != 'Symmetrical')].reset_index(drop=True)
    else:
        return df_return


def check_skew_before_after(df_skew, dataframe, method='yeo-johnson'):
    '''
    this function will check skewness before and after
    it will not modify any feature, just check skew values
    df_skew: skewness dataframe that is genereated by evaluate_skewness function
    dataframe: dataframe of your features
    method: ['yeo-johnson','box-cox'] , default it 'yeo-johnson'
    '''
    # get the list of current skewness values for all the passed features
    df_skew = df_skew[df_skew['Recommendation'] != 'None needed']
    skew_before = df_skew['Skewness Value'].to_list()
    skew_after = []

    list_of_col = df_skew['Feature'].to_list()
    for col in dataframe[list_of_col]:
        min_val = dataframe[col].min()
        if method == 'yeo-johnson':
            pt = PowerTransformer(method='yeo-johnson')
        elif method == 'box-cox':
            if min_val <= 0:
                return f"can't use box-cox with 0 or negative valued column {col}"
            else:
                pt = PowerTransformer(method='box-cox')
        skew_after.append(round(skew(pt.fit_transform(dataframe[[col]]))[0], 2))
    df_return = pd.DataFrame({
        "Feature": list_of_col,
        "Skew Before": skew_before,
        "Skew After": skew_after
    })
    return df_return


def evaluate_model(model, X_train, X_test, y_train, y_test, model_name="Model"):
    """
    Predicts and calculates MAE, RMSE and R2 for both train and test sets.
    """
    print(f"--- {model_name} Performance ---")

    # Generate predictions for both X_train and X_test
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Calculate MAE for train and test (this is the competition metric)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)

    # Calculate RMSE for train and test
    train_rmse = mean_squared_error(y_train, y_train_pred) ** 0.5
    test_rmse = mean_squared_error(y_test, y_test_pred) ** 0.5

    # Calculate R2 for train and test
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)

    # Print the results clearly
    print(f'mae   for train = {train_mae}, and for test = {test_mae}')
    print(f'rmse  for train = {train_rmse}, and for test = {test_rmse}')
    print(f'score for train = {train_r2}, and for test = {test_r2}')

    # Return the numbers so we can build a comparison table later
    return {'Model': model_name,
            'Train MAE': train_mae,
            'Test MAE': test_mae,
            'Train RMSE': train_rmse,
            'Test RMSE': test_rmse,
            'Train R2': train_r2,
            'Test R2': test_r2}
