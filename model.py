import pandas as pd
import numpy as np
from app.utils.load_data import load_data
from app.utils.clean_data import clean_data
from app.utils.prep_data import *
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json

MODELS = ["ar", "prophet", "arima"]
MODEL_VERSIONS = ["0.1", "0.1", "0.1"]
MODEL_NOTES = ["AR model", "Prophet model", "Arima model"]

def predict_with_time_series(model, test):
    y_pred = model.get_forecast(len(test.index))
    y_pred_df = y_pred.conf_int(alpha = 0.05)

    y_pred_df["Predictions"] = model.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
    y_pred_df.index = test.index
    y_pred_out = y_pred_df["Predictions"]
    return y_pred_out

def build_time_series_pipeline(model_type, order, train, test):
    pipe = Pipeline([("time", model_type(train["Total Revenue"], order = order).fit()), ("predict", predict_with_time_series)])
    y_pred_out = pipe["predict"](pipe["time"], test["Total Revenue"])
    return pipe, y_pred_out

def custom_grid_search(model, parameters, data, target_metric):
    train, test = train_test_split(data)
    best_model = None
    best_error = float("INF")
    best_order = None
    for order in parameters["order"]:
        try:
            pipeline, predictions = build_time_series_pipeline(model, order, train, test)
            error = target_metric(test["Total Revenue"].values, predictions)
            if error < best_error:
                best_error = error
                best_model = pipeline
                best_order = order
        except KeyboardInterrupt:
            break
    return best_model, best_error, best_order

def save_model(model, model_path):
    model.save(model_path)

def train_ARIMA(data_dir, params=None, grid_search=False, grid_search_params=None, save_best_model=True, model_path=None):
    df = load_data(data_dir)
    df = clean_data(df)
    df = prepare_data(df)
    if grid_search_params:
        best_pipe, best_error, best_order = custom_grid_search(ARIMA, grid_search_params, df, target_metric=params["target_metric"])
    if save_best_model:
        save_model(best_pipe["time"], model_path)
    return best_pipe, best_error, best_order

def train_AR(data_dir, params=None, grid_search=False, grid_search_params=None, save_model=True, model_path=None):
    pass

def train_prophet(data_dir, save_model=True, model_path=None):
    df = load_data(data_dir)
    df = clean_data(df)
    df = prepare_data(df)
    df.rename(columns={'Date':'ds', 'Total Revenue': 'y'}, inplace=True)
    df_train = df[:-30]
    df_test = df[-30:]
    model = Prophet(weekly_seasonality=True)  
    model.fit(df_train)
    y_pred = model.predict(df_test)
    error = mean_squared_error(df_test.y, y_pred.yhat)
    if save_model:
        with open(model_path, 'w') as fout:
            fout.write(model_to_json(model))  # Save model
    return model, error


if __name__ == "__main__":
    CSV_PATH = "time_series.csv"
    DATA_DIR = "../cs-train"
    # parameters = {"order": [(i, j, k) for i in range(0,10) for j in range(0,1) for k in range(0,10)]}
    # print("Training ARIMA")
    # best_model, best_error, best_order = train_ARIMA(DATA_DIR, params={"target_metric": mean_squared_error}, grid_search=False, grid_search_params=parameters, model_path="best_model.pkl")
    # print(best_order)
    # print(best_error)
    pr, error = train_prophet(DATA_DIR, save_model=True, model_path="prophet.json")
    print(error)
