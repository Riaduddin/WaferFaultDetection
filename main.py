from flask import Flask,request
from training_Validation_Insertion import train_validation

app=Flask(__name__)

@app.route('/train',methods=['POST'])
def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path=request.json['folderPath']

            train_valObj=train_validation(path)

            train_valObj.train_validation()
