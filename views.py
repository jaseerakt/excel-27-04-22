# from datetime import time
import time

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
# from . migrate import *
import pandas as pd
import requests
from .models import Customer

# Create your views here.
def home(request):
    return render(request,'index.html')
def upload_file(request):
    file = request.FILES['filefield']
    print(file)
    fs = FileSystemStorage()
    fname = time.strftime("%Y%m%d-%H%M%S") + ".xlsx"
    file_name = fs.save(fname, file)
    path = fs.url(file_name)
    obj=Customer()
    obj.save()
    obj.customer=path
    df = pd.read_excel(file, engine='openpyxl')
    return render(request,'dropdown.html',{'allcolumns':list(df.columns)})

def select(request):
    obj =Customer.objects.all()
    df = pd.read_excel(obj, engine='openpyxl')
    url = "https://api.bigcommerce.com/stores/b5ajmj9rbq/v3/customers"
    company = request.POST['select']
    first_name = request.POST['select1']
    last_name = request.POST['select2']
    phone = request.POST['select3']
    email = request.POST['select4']
    notes = request.POST['select5']
    address1 = request.POST['select6']
    address2= request.POST['select7']
    address_type= request.POST['select8']
    address_city= request.POST['select9']
    address_company= request.POST['select10']
    country_code= request.POST['select11']
    address_fname= request.POST['select12']
    address_lname= request.POST['select13']
    address_phone= request.POST['select14']
    postal_code= request.POST['select15']
    state_or_province= request.POST['select16s']
    for index,row in df.iterrows():
        payload =[{
                "company": company,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "email": email,
                "notes": notes,
                "address1": address1,
                "address2": address2,
                "address_type": address_type,
                "address_city": address_city,
                "address_company": address_company,
                "country_code": country_code,
                "address_fname": address_fname,
                "address_lname": address_lname,
                "address_phone": address_phone,
                "postal_code": postal_code,
                "state_or_province": state_or_province
        }]
        print(payload)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Auth-Token": "redptv84kmlgfed97l7jroa0mdknfgc"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.text)
    return home(request)