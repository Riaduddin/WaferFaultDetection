from flask import Flask,request
from training_Validation_Insertion import train_validation
from flask import Response,render_template
from flask_cors import cross_origin
from trainingModel import trainModel
from prediction_Validation_Insertion import pred_validation
from predictFromModel import prediction
import json
app=Flask(__name__)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']
            pred_val = pred_validation(path)

            pred_val.prediction_validation()

            pred = prediction(path)
            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!" + str(path) + 'and few of the predictions are ' + str(
                json.loads(json_predictions)))

        elif request.form is not None:
            path = request.form['filepath']

            pred_val = pred_validation(path)
            pred_val.prediction_validation()

            pred = prediction(path)
            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!" + str(path) + 'and few of the predictions are ' + str(
                json.loads(json_predictions)))

        else:
            print('Nothing Matched')

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)

    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

@app.route('/train',methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path=request.json['folderPath']

            train_valObj=train_validation(path)

            train_valObj.train_validation()

            trainModelObj= trainModel()
            trainModelObj.trainingModel()

    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")
