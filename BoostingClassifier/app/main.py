from flask import Flask, request, make_response
from flask_cors import CORS

from app.config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig())
CORS(app)


@app.before_request
def log_the_request():
    print(request)
    print(request.get_json())


@app.route('/')
def testAPI():
    return 'API is UP and Running on Development' + app.config.get("DEPLOYMENT_STATUS")


# Boosting Classifier
@app.route('/docker/boostingclassifier/v1/app/<algorithm>',
           methods=['POST'])
def boosting(algorithm):
    from app.methods.gbm import boost as GradientBoostingMachine
    from app.methods.xgbm import boost as ExtremeGradientBoostingMachine
    from app.methods.lightgbm import boost as LightGBM
    from app.methods.catboost import boost as CatBoost
    from app.methods.adaboost import boost as AdaBoost

    data = request.get_json()

    dataObject = data.get('file')
    parameters = data.get('parameters')

    switcher = {
        "GradientBoostingMachine": GradientBoostingMachine,
        "ExtremeGradientBoostingMachine": ExtremeGradientBoostingMachine,
        "LightGBM": LightGBM,
        "CatBoost": CatBoost,
        "AdaBoost": AdaBoost
    }

    func = switcher.get(algorithm, lambda: "Invalid arg")
    result, output = func(dataObject, parameters)
    if result == 1:
        response = make_response(output)
        response.headers['Content-type'] = 'application/json'
        return response, 200
    else:
        return make_response({"error": output}, 400)