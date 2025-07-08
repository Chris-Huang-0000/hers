import requests
from bs4 import BeautifulSoup
import os
import time
import random
import csv


dir_name = "./shoppingcart/static/images"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
else:
    print("資料夾已建立")

def image_download(url,save_path):
    file_name = url.split("/")[-1].strip() #取得網路圖片的圖檔名
    print(f"圖片下載中{url}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"./{save_path}/{file_name}","wb") as file: #存圖片至本機端路徑的資料夾時，路徑最後一定要加圖檔名
            file.write(response.content)
    else:
        print(f"圖片下載失敗，狀態碼{response.status_code}")
    time.sleep(random.uniform(15,20))
    print("-"*30)

def image_main():
    commudity=[]

    for page in range(1,19):
        url = f"https://www.wstyle.com.tw/Shop/itemList.aspx?m=34&o=0&sa=0&smfp={page}&"
        header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        response = requests.get(url,headers=header)
        soup = BeautifulSoup(response.text,"html.parser")

        products = soup.find_all("div",class_="itemListMerName")
        product_name = [product.a.text for product in products]

        prices = soup.find_all("div",class_="itemListMoney")
        product_price = [price.span.text for price in prices]

        images = soup.find_all("div",class_="ilImg1")
        product_image = [image.img.get("src") for image in images]

        product_list = [{"title":product_name[i],"price":product_price[i],"image":product_image[i]} for i in range(len(product_name))]

        for _ in product_image:
            j = _.split("/")[-1].strip()
            if os.path.exists(os.path.join(dir_name,j)):
                continue
            else:
                image_download(_,dir_name)
        
        commudity.extend(product_list)

    return commudity

# image_main()
products = image_main()
print(len(products))

for _ in products:
    _["image"] = _['image'].split("/")[-1].strip()

try:
    title = ['title','price','image']
    with open("./shoppingmall/product_list.csv","w",encoding="utf-8-sig",newline="") as file:
        writer = csv.DictWriter(file,fieldnames=title)
        writer.writeheader()
        writer.writerows(products)
except Exception as e:
    print(e)