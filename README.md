# Simple optical character recognition (OCR) for car registration card (RC)

## Description:
1. Extract some important information from RC images
2. Pass image through API to webserver running the OCR model.
3. Model is pretrained using [keras-ocr](https://github.com/faustomorales/keras-ocr), and served using flask framework


## Getting started
1. clone this repo
2. install dependencies -> requirements.txt 
3. run ```python run.py``` to start the webserver
4. pass the image to the API using the program of your choice (request, postman, etc.)
 - example using request
 ```
 import requests
 
 test_img = 'sample_image.jpg'

 files = {'file': open(test_img, 'rb')}
 response = requests.post(url, files=files)
 print(response.json())
 ```


## Sample input and output
1. Image input through API
![example of input image](https://github.com/asyrafjanai/rc_ocr/blob/master/flaskapp/app/uploads/sample_output1.png)

output result:
```
{
    "text": "SIJIL PEMILIKAN KENDERAAN JABATAN PENGANGKUTAN JALAN AYJUET NO PENDAFTARAN JSD3798 NO ID NAMA PENUN BERDAFTAR YA ALL AMAT NO CHASIS NO ENJIN CAUA3A15369 V02031534A BUATAN/NAMA MODEL NISSAN CEF IRO OL KEUPAYAN ENJI IN 195 BAHAN BAKAR PETROL STATUS ASAL PEMASANGAN TEMPATAN KELAS KEGUNAAN PERSENDIRIAN-MO TOKAR INDIVIDU JENIS BADAN/TAHUN DIBUAT MOTOKAR 2003 TAR IKH PENDAFTARAN 26/08 /2003 D SYARAT PENDAFTARAN SYARAT PENDAFTARAN SYARAT PENDAFTARAN LULUS MILIK PEMERIKSAAN TUKAR KEPUTUSAN",
    "no_pendaftaran": "JSD3798",
    "no_enjin": "V02031534A",
    "no_chasis": "CAUA3A15369"
  }
```
  
 2. Sample Annotation on image
 ![example of input image](https://github.com/asyrafjanai/rc_ocr/blob/master/flaskapp/app/uploads/sample_annot.png)


#### note!
1. training script is not included. Refer to keras-ocr for guide 
1. Simple app for ocr application, not suitable for production environment
2. Use proper webserver (wsgi, gunicorn) instead of flask server 
