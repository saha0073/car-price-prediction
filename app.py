# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 19:25:53 2020


"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


app=Flask(__name__)
#model=pickle.load(open("car_model.pkl","rb"))
model=pickle.load(open("random_forest_regression_model.pkl","rb"))
 
standard_to=StandardScaler()
@app.route("/",methods=['GET'])

def Home():
    return render_template('index.html')


@app.route("/predict",methods=['POST'])
def predict():
    fuel_Type_Diesel=0
    if request.method=='POST':
        Year=int(request.form['Year'])
        Present_Price_USD=float(request.form['Present_Price'])
        Present_Price=Present_Price_USD*70./pow(10.,5)
        Miles_Driven=int(request.form['Kms_Driven'])
        Kms_Driven=int(Miles_Driven*1.6)
        #Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
             Fuel_Type_Petrol=0
             Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            
        Year=2020-Year
       # Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output_INR=prediction[0]
        output=int(round(output_INR*pow(10.,5)/70.,-1))
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at  ${}".format(output))
    else:
        return render_template('index.html')
    


if __name__=="__main__":
    app.run()




