from datetime import datetime
import pandas as pd
import traceback

def eat(pandasSeries, v):
    for i in range(len(pandasSeries)):
        if pandasSeries[i] - v >= 0:
            pandasSeries[i] -=  v
            v = 0

        else:
            v -= pandasSeries[i]
            pandasSeries[i] = 0

    return v


def calculateWriteOffAGV(dictMateriais, df):
    for material in list(dictMateriais.keys()):
        #print(material)

        for key in list(df.keys()):
            #print(key)
            if key == material:
                try:
                    meses =list(df[key]['Meses'])
                    forecast = list(df[key]['AGV Forecast'])
                    forecastReplica = pd.Series()
                    
                    batchExpirationDict = {}
                    batchStockAmountDict = {}

                    for batch in list(dictMateriais[material]['Batch'].keys()):
                        if str(dictMateriais[material]['Batch'][batch].get('Storage location')) == '1001' and str(dictMateriais[material]['Batch'][batch].get('Plant')) == 'BR08':
                        
                            lsdString = dictMateriais[material]['Batch'][batch].get('Limit sales date')
                            limitSalesDate = datetime.strptime(lsdString, "%Y-%m-%d")
                            batchExpirationDict[batch] = limitSalesDate
                            batchStockAmountDict[batch] = dictMateriais[material]['Batch'][batch].get('Stock Amount')

                    orderedBatchList = sorted(batchExpirationDict.items(), key=lambda item: item[1])

                    limitMonth = None  
                    for batch in orderedBatchList:
                        limitSalesDate = batch[1] 
                        stockAmount = batchStockAmountDict[batch[0]]
                        previousLimitMonth = limitMonth
                        for m in meses:
                            try:
                                
                                dateObj = datetime.strptime(m.lower(), "%b %Y")
                                #print(dateObj)
                                if dateObj < limitSalesDate:
                                    limitMonth = dateObj.strftime("%b %Y").upper()
                            except:
                                ...                        
                        if limitMonth != None:
                            idx = meses.index(limitMonth)
                            if forecastReplica.empty or previousLimitMonth != limitMonth:
                                _meses = meses[:idx + 1]
                                _forecast = forecast[:idx + 1]
                                forecastReplica = pd.Series(data=_forecast, index=_meses)
                            #print()
                            #print(batch[0],"Forecast Replica: ",forecastReplica)
                            #print(batch[0],"Stock Amount: ",stockAmount)
                            wo = eat(forecastReplica, stockAmount)
                            #print(batch[0],"Forecast Replica2: ",forecastReplica)
                            for i in range(len(forecastReplica)):
                               forecast[i] = forecastReplica[i] 
                            dictMateriais[material]['Batch'][batch[0]]["Write off"] = wo
                            #print("BATCH: ",batch,"WO: ",wo)
                            #print()

                except:
                    traceback.print_exc()

                    #print(key)
                    #print("AQUI",df[key], "aqui")
                    ...