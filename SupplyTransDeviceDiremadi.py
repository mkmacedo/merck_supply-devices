from datetime import datetime
import pandas as pd
import traceback


def calculateTransfer(dictMateriais, df):
    dfTransfer = pd.DataFrame()
    for material in list(dictMateriais.keys()):
        #print(material)

        for key in list(df.keys()):
            #print(key)
            if key == material:
                try:
                    forecast = list(df[key]['Forecast'])
                    mes =list(df[key]['Meses'])[0]
                    forecastReplica = pd.Series()
                    
                    batchExpirationDict = {}
                    batchStockAmountDict = {}
                    batchBSKDict = {}
                    batchPlantDict = {}
                    batchBR01Dict = {}
                    batchTransfer = {}
                    batchStorageLocationDict = {}


                    for batch in list(dictMateriais[material]['Batch'].keys()):
                        
                        lsdString = dictMateriais[material]['Batch'][batch].get('Limit sales date')
                        limitSalesDate = datetime.strptime(lsdString, "%Y-%m-%d")
                        batchExpirationDict[batch] = limitSalesDate
                        batchStockAmountDict[batch] = dictMateriais[material]['Batch'][batch].get('Stock Amount')
                        batchBSKDict[batch] = dictMateriais[material]['Batch'][batch].get('Batch status key')
                        batchPlantDict[batch] = dictMateriais[material]['Batch'][batch].get('Plant')
                        batchStorageLocationDict[batch] = dictMateriais[material]['Batch'][batch].get('Storage location')
                    
                    orderedBatchList = sorted(batchExpirationDict.items(), key=lambda item: item[1])
                    totalAmount = 0
                    for batch in orderedBatchList:
                        print(batchBSKDict[batch[0]])
                        print(type(batchBSKDict[batch[0]]))
                        print(batchBSKDict[batch[0]] == 0.0)
                        print(batchPlantDict[batch[0]])
                        if batchPlantDict[batch[0]] == "BR08":
                            totalAmount += batchStockAmountDict[batch[0]]
                            #print(totalAmount)
                        if batchBSKDict[batch[0]] == '0.0' and batchPlantDict[batch[0]] == "BR01":
                            batchBR01Dict[batch[0]] = batchStockAmountDict[batch[0]]
                    fc = forecast[0]
                    #print(fc)
                    try:
                        forcastPercentage = (totalAmount / fc) * 100  
                        if forcastPercentage < 150:
                            x = 150 * fc / 100 
                            complement = x - totalAmount
                            for key in list(batchBR01Dict.keys()):
                                if batchBR01Dict[key] <= complement:
                                    if complement > 0 and batchExpirationDict[key] > datetime.strptime(mes.lower(),"%b %Y"):
                                        batchTransfer[key] = batchBR01Dict[key]
                                        complement -= batchBR01Dict
                                elif batchExpirationDict[key] > datetime.strptime(mes.lower(),"%b %Y"):
                                    batchTransfer[key] = complement
                                    complement = 0
                            print(batchTransfer)

                            #transferDf = pd.DataFrame()
                            transferDict = {}
                            transferDict["Item"] = [material] * len(batchTransfer)
                            transferDict["Descricao"] = [dictMateriais[material].get("Description")] * len(batchTransfer)
                            transferDict["Lote"] = []
                            transferDict["Planta Atual"] = []
                            transferDict["Planta"] = []
                            transferDict["Qtd"] = []
                            transferDict["Storage location"] = []
                            
                            for lote in list(batchTransfer.keys()):
                                transferDict['Lote'].append(lote)
                                transferDict['Planta Atual'].append(batchPlantDict.get(lote)) 
                                transferDict['Planta'].append("BR08")                         
                                transferDict["Qtd"].append(batchTransfer.get(lote))
                                transferDict['Storage location'].apped(batchStorageLocationDict.get(lote))

                            batchTransferDf = pd.DataFrame(data = transferDict)
                            dfTransfer = dfTransfer.append(batchTransferDf)
                            
                            #print(batch, "resultado", forcastPercentage)
                    
                    except:
                        ...

                except:
                    ...
    #print(dfTransfer)
    dfTransfer.to_excel("planilha_transferencia.xlsx")
