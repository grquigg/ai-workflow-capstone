from flask import Flask, jsonify, request
from flask import render_template
from app.model import model_train

MODELS = ["ar", "prophet", "arima"]
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/predict", methods=["GET", "POST"])
def predict():

    pass

@app.route("/train", methods=["GET", "POST"])
def train():
    if not request.json:
        print("ERROR: API (train): did not receive request data")
        return jsonify(False)
    
    test = False
    if 'mode' in request.json and request.json['mode'] == 'test':
        test = True

    if 'model' not in request.json or request.json['model'] not in MODELS:
        print("ERROR: API (train): did not recognize model name")
        return jsonify(False)
    model = request.json['model']
    parameters = None
    if 'parameters' in request.json:
        parameters = request.json['parameters']
    print("...training model")
    model = model_train(test=test, model_name=model, parameters=parameters)
    print("...training complete")

    return(jsonify(True))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)