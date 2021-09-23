from selenium import webdriver
import time
import cv2 
import pytesseract
import base64
from PIL import Image
from io import BytesIO
from selenium.webdriver.firefox.options import Options

from flask import Flask,make_response
from flask_restful import Api,Resource,reqparse,abort
import json

app = Flask(__name__)
api = Api(app)

class WebScrapping:

    # opt = webdriver.ChromeOptions()
    # opt.add_argument('-headless')
    web = webdriver.Firefox()
    web.get('https://foscos.fssai.gov.in/')
    First_Click = web.find_element_by_xpath('/html/body/app-root/div[2]/div/div[2]/input').click()
    Second_Click = web.find_element_by_xpath('/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/ul/li[3]/a').click()

    time.sleep(2)

    # Function For Getting Captcha Value
    def Captcha(self):
        images = self.web.find_elements_by_tag_name('img')
        for image in images:
            if(image.get_attribute('alt')=="Captcha"):
                c = image.get_attribute('src')
                Get_Base64_Value = c[23:]
                break

        Get_Image = Image.open(BytesIO(base64.b64decode(Get_Base64_Value)))

        pytesseract.pytesseract.tesseract_cmd=r"C:/Users/Divy/AppData/Local/Tesseract-OCR/tesseract.exe"
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        Get_Captcha = pytesseract.image_to_string(Get_Image)

        return Get_Captcha

    # Function For Getting Detail After Autofill form
    def Get_Detail_form(self):
        dataInJson = {}
        all_detail = []
        Get_detail = self.web.find_elements_by_xpath('/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div[2]/div/form/div/div/div/div[1]/table/tbody/tr/td')
        for item in Get_detail:
            company_detail = item.text
            all_detail.append(company_detail)
            if(company_detail == "View Products"):
                try:
                    get_list_product_len = len(self.web.find_elements_by_xpath('//*[@id="governmentAgenciesDiv1"]/div[1]/div/div/div[2]/app-product-details/div/div/form/div'))
                    if(get_list_product_len<=1):
                        path3 = '/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div[2]/div[2]/table/tbody/tr/td[2]'
                        get_product_data = self.web.find_elements_by_xpath(path3)
                        a = []
                        for data in get_product_data:
                            all_product_data = data.text
                            a.append(all_product_data)
                        dataInJson['uncategorised'] = a
                        all_detail.append(dataInJson) 
                        
                        return all_detail
                        
                    else:
                        category_count=0
                        product_count = 0
                        for i in range(2,get_list_product_len+1):
                            path1 = '/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div[2]/app-product-details/div/div/form/div['+str(i)+']/h5'
                            path2 = '/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div[2]/app-product-details/div/div/form/div['+str(i)+']/div/table/tbody/tr/td[2]'
                            get_list_category1 = self.web.find_elements_by_xpath(path1)
                            get_data_product = self.web.find_elements_by_xpath(path2)
                            for data in get_list_category1:
                                categories_data = data.text
                                category_count = category_count+1
                                product_count=0
                                all_detail.append(categories_data)
                                a = []
                            for data in get_data_product:
                                categories_product_data = data.text
                                product_count = product_count+1
                                a.append(categories_product_data)
                            dataInJson[categories_data] = a
                            all_detail.append(dataInJson)
                            dataInJson = {}

                        
                except:
                    print('Error in product data')

        return all_detail

    # Function For Automatic fill form
    def Autofillform(self,Get_License_Number):
        # Get_License_Number = "20717030000293"
        Send_License_Number = self.web.find_element_by_xpath('/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div[1]/form/div/div/div[3]/div/input').clear()
        Send_License_Number = self.web.find_element_by_xpath('/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div[1]/form/div/div/div[3]/div/input').send_keys(Get_License_Number)
        Get_From_Captcha = self.Captcha()
        Send_Captcha = self.web.find_element_by_xpath('/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div[1]/form/div/div/div[4]/div/input').send_keys(Get_From_Captcha)
        Submit_button = self.web.find_element_by_xpath('/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div/form/div/div/div[4]/button').click()

        time.sleep(5)

        fassai_detail = self.Get_Detail_form()
        return fassai_detail

        time.sleep(2)

# def abort_if_license_no_doesnt_exist(license_Id):
#     if (license_Id is None):
#         abort(404, message="Please pass License No")

class GetFssaiDetail(Resource,WebScrapping):

    def inJsonFormat(self,rawData):

        dataInJson = {}
        dataInJson['licenseId'] = rawData[3]
        dataInJson['companyName'] = rawData[1]
        dataInJson['premisesAddress'] = rawData[2]
        dataInJson['licenseType'] = rawData[4]
        dataInJson['valid'] = rawData[5]
        dataInJson['products'] = rawData[-1]

        return dataInJson

    def get(self,license_Id):
        # abort_if_license_no_doesnt_exist(license_Id)
        # print(type(license_Id))

        rawData = self.Autofillform(license_Id)
        data = self.inJsonFormat(rawData)
        resp = make_response(json.dumps(data),200)
        return resp
        
        # return license_Id


api.add_resource(GetFssaiDetail,'/getFSSAIDetails/<int:license_Id>')

if __name__ == "__main__":
    app.run(debug=True)