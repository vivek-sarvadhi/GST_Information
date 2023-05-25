from fastapi import FastAPI, UploadFile, Request
import uvicorn, os
import pandas as pd
import numpy as np
import requests


app = FastAPI()

@app.post("/gst_information")
def get_excelimage(file: UploadFile):
    stjCd = []
    stj = []
    lgnm = []
    dty = []
    comapny_addrs = []
    status = []
    tradeNam = []
    ctjCd = []
    ctj = []
    einvoiceStatus = []
    directory = os.getcwd()
    data_file = "new_file.xlsx"
    full_path = f"{directory}/{file.filename}"
    label_path = f"{directory}/{data_file}"
    xls = pd.ExcelFile(full_path)
    dbframe1 = pd.read_excel(xls)
    dbframe1 = dbframe1.replace(to_replace=np.nan,value=None)
    for index, row in dbframe1.iterrows():
        url = "https://commonapi.mastersindia.co/commonapis/searchgstin"

        parms = {
            "gstin":row['gst_no']
        }
        headers = {
            'Authorization': 'Bearer 0ab31ef7392227173c6e8d34195e86d5eb0da1e9',
            'client_id': 'JarZChUcsytSBbnkpt'
        }

        response = requests.request("GET", url, headers=headers,params=parms)
        result = response.json()
        stjCd.append(result['data']['stjCd'])
        stj.append(result['data']['stj'])
        lgnm.append(result['data']['lgnm'])
        dty.append(result['data']['dty'])
        comapny_addrs.append(result['data']['adadr'])
        status.append(result['data']['sts'])
        tradeNam.append(result['data']['tradeNam'])
        ctjCd.append(result['data']['ctjCd'])
        ctj.append(result['data']['ctj'])
        einvoiceStatus.append(result['data']['einvoiceStatus'])
    dataframe1 = pd.DataFrame({'stjCd':stjCd,'stj':stj,'lgnm':lgnm,"dty":dty,"comapny_addrs":comapny_addrs,"status":status,"tradeNam":tradeNam,"ctjCd":ctjCd,"ctj":ctj,"einvoiceStatus":einvoiceStatus})
    with pd.ExcelWriter(label_path) as writer:
        dataframe1.to_excel(writer, sheet_name='GST Detail', index=False)
    return {"file_name":label_path}
