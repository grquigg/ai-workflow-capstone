from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.ar_model import AutoReg

def show_pacf(data):
    plot_pacf(data)

def show_acf(data):
    plot_acf(data)

def extract_acf_data(data, threshold=0.25, nlags=25):
    stats = acf(data, nlags=nlags)
    return np.argwhere(stats>=threshold)

def extract_pacf_data(data, threshold=0.25, nlags=25):
    stats = pacf(data, nlags=nlags)
    return np.argwhere(stats>=threshold)

def find_best_autoreg_model(train, test, values, error_function):
    best_model = None
    best_error = np.inf
    best_lags = 0
    for value in values:
        ar_model = AutoReg(train["Total Revenue"], lags=value).fit()
        pred = ar_model.predict(start=len(train)+1, end=len(train)+len(test), dynamic=False)
        error = error_function(test["Total Revenue"], pred)
        if error < best_error:
            best_model = ar_model
            best_error = error
            best_lags = value
    return best_model, best_error, best_lags