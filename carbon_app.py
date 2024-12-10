#importing the required libraries(Here, Kivy)
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.uix.floatlayout import FloatLayout

import time
import speech_recognition as pq
from twilio.rest import Client
import pyttsx3
import sqlite3
import matplotlib.pyplot as myPlot
import csv
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_percentage_error




lp=pq.Recognizer()

#mycon=mysql.connector.connect(host='localhost',user='root',database='app_db_pavitra',passwd='pavitra')

#mycursor=mycon.cursor()



current_connection_tosql_database = sqlite3.connect("carbon_app_users.db")

help_app_cur = current_connection_tosql_database.cursor()

create_table_initial_command = """CREATE TABLE IF NOT EXISTS carbon_app_users(first_name TEXT, last_name TEXT, username TEXT, phone_number INT, relative_number INT, location TEXT, password TEXT NOT NULL)"""
help_app_cur.execute(create_table_initial_command)

#Declaring the main class for our kivy app

class Page1(Screen):
    pass
class Page2(Screen):
    pass
class Page3(Screen):
    pass
class Page4(Screen):
    pass
class Page5(Screen):
    pass    
class Page7(Screen):
    pass
class emissionsGraph(Screen):
    pass
class predictionEmissionsPage(Screen):
    pass
class predictionNetEmissionsPerSectorPage(Screen):
    pass
class predictionNetEmissionsPage(Screen):
    pass
username_in_session = ""
'''
class Graph(FloatLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
'''

class pavitra_app(MDApp):
    def build(self):
        new=Builder.load_file('kivy_app1_pavitra.kv')
        abc=ScreenManager()
        abc.add_widget(Page1(name='page1'))
        abc.add_widget(Page2(name='page2'))
        abc.add_widget(Page3(name='page3'))
        abc.add_widget(Page4(name='page4'))
        abc.add_widget(emissionsGraph(name='page5'))
        abc.add_widget(Page7(name='page7'))
        abc.add_widget(predictionEmissionsPage(name='page11'))
        abc.add_widget(predictionNetEmissionsPerSectorPage(name='page12'))
        abc.add_widget(predictionNetEmissionsPage(name='page13'))
        
        

        return new



    def register_user(self):
        self.fn = repr(self.root.get_screen('page3').ids.fname.text).strip("'")
        print(self.fn)
        self.ln= repr(self.root.get_screen('page3').ids.lname.text).strip("'")
        self.user= repr(self.root.get_screen('page3').ids.username.text).strip("'")
        
        self.pas= repr(self.root.get_screen('page3').ids.password.text).strip("'")
        
        q1="insert into carbon_app_users values ('{}','{}','{}',{},{},'{}','{}')".format(self.fn,self.ln,self.user,self.pn,self.rn,self.lo,self.pas)
        help_app_cur.execute(q1)
        current_connection_tosql_database.commit()
         
        self.root.get_screen('page3').ids.fname.text = ""
        self.root.get_screen('page3').ids.lname.text = ""
        self.root.get_screen('page3').ids.username.text = ""
        self.root.get_screen('page3').ids.pnumber.text = ""
        self.root.get_screen('page3').ids.rnumber.text = ""
        self.root.get_screen('page3').ids.location.text = ""
        self.root.get_screen('page3').ids.password.text = ""


    def login_user(self):
        self.lguser = self.root.get_screen('page2').ids.username.text
        self.lgpass=self.root.get_screen('page2').ids.password.text
        q1="select username, password from carbon_app_users"
        help_app_cur.execute(q1)
        new_app=help_app_cur.fetchall()

        for i in new_app:
            if i[0]==self.lguser and i[1]==self.lgpass:
                username_in_session = self.lguser
                return True
        else:
            print("false returned")
            self.root.get_screen('page2').ids.username.text = ""
            self.root.get_screen('page2').ids.password.text = ""
            return False    
               


    def getAllLabels(self,path):
        emissionsdata = []

        with open(path, newline='') as emissionsFile:
            emissionsreader = csv.DictReader(emissionsFile)
            for i in emissionsreader:
                emissionsdata.append(i['Sector'])
        return emissionsdata
    
    def getAllYAxis(self,path, label):
        yaxis = []
        emissionsdata = []
        with open(path, newline='') as emissionsFile:
            emissionsreader = csv.DictReader(emissionsFile)
            for i in emissionsreader:
                emissionsdata.append(i)

        for j in emissionsdata:
            if j['Sector'] == label:
                for valueRow in j:
                    if valueRow == 'Sector':
                        pass
                    else:
                        yaxis.append(int(j[valueRow]))
            
        return yaxis

    def offsetCompanies(self, path, cost, netEmissionValue ):
        result = ""
        offsetCompanies = []
        with open(path, newline='') as emissionsFile:
            emissionsreader = csv.DictReader(emissionsFile)
            for i in emissionsreader:
                offsetCompanies.append(i)
        if (netEmissionValue<3000):
            costArr = []
            for i in offsetCompanies:
                costArr.append(int(i['Cost']))
            minCost = min(costArr)
            indexValue = costArr.index(minCost)
            count = 0
            print(offsetCompanies)
            for i in offsetCompanies:
                if count == indexValue:
                    result = result + "\n The offset can be covered by giving contract to "
                    result = result + i['Company Name']
                    result = result + " because it offsets "
                    result = result + str(i['CO2OffsetTonnes'])
                    result = result + " metric tonnes of carbon at a cost of "
                    result = result + str(i['Cost'])
                    result = result + " dollars \n After this, the net emissions would become "
                    result = result + str(netEmissionValue - int(i['CO2OffsetTonnes']))
                    result = result + " metric tonnes of carbon"
                count = count + 1
        return result
    def create_emissions_graph(self, path):
        allLabels= self.getAllLabels(path)
        xaxis = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
        for i in allLabels:
            yAxisEach = self.getAllYAxis(path, i)
            myPlot.plot(xaxis, yAxisEach, label = i)
        myPlot.xlabel('Year')
        myPlot.ylabel('Carbon Emissions')
        myPlot.title('Carbon emissions per year in all sectors')
        myPlot.legend(loc='upper right')  
        return myPlot.show()
    def subtractFunc(self, a, b):
        return a-b
    def net_emissions_graph(self, path, path2):
        allLabels= self.getAllLabels(path)
        xaxis = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
        for i in allLabels:
            yAxisEachEmission = self.getAllYAxis(path, i)
            yAxisEachOffset = self.getAllYAxis(path2, i)
            realYAxis = map(self.subtractFunc, yAxisEachEmission, yAxisEachOffset)
            newyaxis = list(realYAxis)
            myPlot.plot(xaxis, newyaxis, label = i)
        myPlot.xlabel('Year')
        myPlot.ylabel('Carbon Emissions')
        myPlot.title('Carbon emissions per year in all sectors')
        myPlot.legend(loc='upper right')  
        return myPlot.show()
    
    def getListData(self, path,i):
        return self.getAllYAxis(path, i)
            
    def getPredictionForAllSector(self, path):
        result = ""
        allLabels= self.getAllLabels(path)
        ret = []
        for i in allLabels:
            result = result + "The emission only prediction for next year in " 
            result = result + i
            result = result + " is "
            ret.append(self.predictionCalcForecast(self.getListData(path,i)))
            result = result + str(self.predictionCalcForecast(self.getListData(path,i)))
            result = result + "\n\n"
        
        return result


    def generate_graph_all_sectors_done(self, path):
        result = ""
        xaxis = ['Agri', 'Avi', 'Comm', 'Ener', 'Fores', 'indus', 'marine', 'resedential', 'transport', 'waste']
        allLabels= self.getAllLabels(path)
        ret = []
        for i in allLabels:
            ret.append(self.predictionCalcForecast(self.getListData(path,i)))
        myPlot.plot(xaxis, ret, label = i)
        myPlot.xlabel('Year')
        myPlot.ylabel('Carbon Emissions')
        myPlot.title('Predicted emissions only for next year')
        myPlot.legend(loc='upper right')  
        return myPlot.show()
    
    def generate_graph_all_sectors_NET_done(self, path, path2):
        result = ""
        xaxis = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
        allLabels= self.getAllLabels(path)
        ret = []
        for i in allLabels:
            yAxisEachEmission = self.getAllYAxis(path, i)
            yAxisEachOffset = self.getAllYAxis(path2, i)
            realYAxis = map(self.subtractFunc, yAxisEachEmission, yAxisEachOffset)
            newyaxis = list(realYAxis)
            myPlot.plot(xaxis, newyaxis, label = i)
        myPlot.xlabel('Year')
        myPlot.ylabel('Carbon Emissions')
        myPlot.title('Predicted NET emissions only for next year')
        myPlot.legend(loc='upper right')  
        return myPlot.show()
            
    def getNetPredictionForPerSector(self, path, path2):
        result = ""
        allLabels= self.getAllLabels(path)

        for i in allLabels:
            yAxisEachEmission = self.getAllYAxis(path, i)
            yAxisEachOffset = self.getAllYAxis(path2, i)
            realYAxis = map(self.subtractFunc, yAxisEachEmission, yAxisEachOffset)
            newyaxis = list(realYAxis)
            result = result + "The net emission prediction for next year in " 
            result = result + i
            result = result + " is "
            result = result + str(self.predictionCalcForecast(newyaxis))
            result = result + "\n\n"
        return result

    def getNetPrediction(self, path, path2):
        result = ""
        newValRet = []
        allLabels= self.getAllLabels(path)

        for i in allLabels:
            yAxisEachEmission = self.getAllYAxis(path, i)
            yAxisEachOffset = self.getAllYAxis(path2, i)
            realYAxis = map(self.subtractFunc, yAxisEachEmission, yAxisEachOffset)
            newyaxis = list(realYAxis)
            newValRet.append(self.predictionCalcForecast(newyaxis))

        result = result + "The Net emission prediction for next year for all sectors combined is "+ str(round(sum(newValRet),2))

        if (sum(newValRet)>0):
            result = result + "\n\n"
            result = result + "The total carbon tax to be paid is: "
            result = result + "$"+ str(round(65*sum(newValRet),2))
            result = result + self.offsetCompanies('/Users/pavitrakamleshkumarmodi/Downloads/SDC_Hackathon_Comp_Package/CarbonOffsetCompanies.csv', round(65*sum(newValRet),2), sum(newValRet))
        else:
            result = result + "The predictions for next year show that carbon offsetting is done through\n Irvine Gasoline's sectors of business itself."
            result = result + "\n So, There is no need to buy offsets from other companies."
        return result
            


    def predictionCalcForecast(self, listGiven):
        series = pd.Series(listGiven)

        model = ARIMA(series, order=(1,0,0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=1)
        
        return round(list(forecast)[0],2)
    
    def predictionCalcPredValue(self, listGiven):
        series = pd.Series(listGiven)

        model = ARIMA(series, order=(3,1,0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=1)
        return self.find_accuracy(listGiven)

    def find_accuracy(self, listGiven):
        #accuracy = mean_absolute_percentage_error(listGiven, [self.predictionCalcForecast(listGiven)])
        #return accuracy
        pass



if __name__=="__main__":
    app_new = pavitra_app()
    app_new.run()
     