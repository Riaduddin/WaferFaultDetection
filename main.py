from flask import Flask,request
from training_Validation_Insertion import train_validation
from flask import Response
from trainingModel import trainModel
from prediction_Validation_Insertion import pred_validation
from predictFromModel import prediction

app=Flask(__name__)


@app.route("/predict", methods=['POST'])
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']
            pred_val = pred_validation(path)

            pred_val.prediction_validation()

            pred = prediction(path)
            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()

        elif request.form is not None:
            path = request.form['filepath']

            pred_val = pred_validation(path)
            pred_val.prediction_validation()

            pred = prediction(path)
            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()


        else:
            print('Nothing Matched')

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)

    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)

@app.route('/train',methods=['POST'])
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
