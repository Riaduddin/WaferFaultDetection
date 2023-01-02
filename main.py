from flask import Flask,request
from training_Validation_Insertion import train_validation
from flask import Response
from trainingModel import trainModel
app=Flask(__name__)

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
