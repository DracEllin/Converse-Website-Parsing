from bs4 import BeautifulSoup as BS
import requests
from openpyxl import Workbook
import time

def get_html(url):
    cookies = {
        'Path': '/',
        'visid_incap_2186926': '4+qfjb7dQ3+8rBVK4PelJl1lrGYAAAAAQUIPAAAAAADQ5g0bj+zQ4JdNSO7xVZcm',
        'form_key': 'yrhdjwYEBkQFmFbW',
        '_gid': 'GA1.2.1014953208.1722574191',
        'wp_ga4_customerGroup': 'NOT%20LOGGED%20IN',
        '_ALGOLIA': 'anonymous-600e3666-a72b-4227-985f-76bed2f10fff',
        'CookieScriptConsent': '{"googleconsentmap":{"ad_storage":"targeting","analytics_storage":"performance","ad_user_data":"targeting","ad_personalization":"targeting","functionality_storage":"functionality","personalization_storage":"functionality","security_storage":"functionality"},"firstpage":"https://converse.ca/","action":"accept","consenttime":1719438355,"categories":"[\\"performance\\",\\"targeting\\",\\"functionality\\"]"}',
        '_fbp': 'fb.1.1722574318578.167943963717703283',
        'incap_ses_1849_2186926': 'qWKGAldCPE/hBPHIuPeoGZTVrGYAAAAATCJLg4KU+mL2pLyzVMzMTA==',
        '_ga_47F8W0TXJ9': 'GS1.1.1722602906.2.1.1722603950.60.0.0',
        '_ga': 'GA1.2.1399080599.1722574178',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'Path=/; visid_incap_2186926=4+qfjb7dQ3+8rBVK4PelJl1lrGYAAAAAQUIPAAAAAADQ5g0bj+zQ4JdNSO7xVZcm; form_key=yrhdjwYEBkQFmFbW; _gid=GA1.2.1014953208.1722574191; wp_ga4_customerGroup=NOT%20LOGGED%20IN; _ALGOLIA=anonymous-600e3666-a72b-4227-985f-76bed2f10fff; CookieScriptConsent={"googleconsentmap":{"ad_storage":"targeting","analytics_storage":"performance","ad_user_data":"targeting","ad_personalization":"targeting","functionality_storage":"functionality","personalization_storage":"functionality","security_storage":"functionality"},"firstpage":"https://converse.ca/","action":"accept","consenttime":1719438355,"categories":"[\\"performance\\",\\"targeting\\",\\"functionality\\"]"}; _fbp=fb.1.1722574318578.167943963717703283; incap_ses_1849_2186926=qWKGAldCPE/hBPHIuPeoGZTVrGYAAAAATCJLg4KU+mL2pLyzVMzMTA==; _ga_47F8W0TXJ9=GS1.1.1722602906.2.1.1722603950.60.0.0; _ga=GA1.2.1399080599.1722574178',
        'priority': 'u=0, i',
        'referer': url,
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    response = requests.get(url, cookies=cookies, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def get_glide_link(html):
    links = []
    soup = BS(html, 'html.parser')
    product_list = soup.find('div', {'id' : 'amasty-shopby-product-list'})
    product_items_list = product_list.find('ol', class_='products list items product-items')
    product_items_links= product_items_list.find_all('a', class_='product photo product-item-photo')
    for link in product_items_links:
        links.append(link.get('href'))
    return links

def get_data(html):
    soup = BS(html, 'html.parser')
    page_title = soup.find('div', class_='page-title-wrapper product')
    name = page_title.find('h1', class_='page-title display-name').text.strip()
    print(name)

    product_info_price = soup.find('div', class_='product-info-price')
    price = product_info_price.find('span', class_='price-wrapper').text.strip()
    print(price)

    amtheme_product_wrap = soup.find('div', class_='amtheme-product-wrap')
    descriptions = amtheme_product_wrap.find('div', class_='product-attribute--list').text.strip('')
    print(descriptions)

    # product_media = soup.find('div', class_='product media')
    # div_img = product_media.find('div', class_='fotorama__stage__frame fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img fotorama__fade-rear magnify-wheel-loaded fotorama__active')
    # print(product_media)
    # colors_sizes = soup.find('div', class_='swatch-opt -round')
    # print(q)


    data = {
        'name': name,
        'price': price,
        'description': descriptions,
    }
    return data

def save_to_exel(data):
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1'] = 'Наименование'
    sheet['B1'] = 'Цена'
    sheet['C1'] = 'Описание'
    for i, item in enumerate(data, 2):
        sheet[f'A{i}'] = item['name']
        sheet[f'B{i}'] = item['price']
        sheet[f'C{i}'] = item['description']
    workbook.save('converse_data.xlsx')

def main():
    URL = 'https://converse.ca/men/shoes/all-shoes/'
    for i in range(1, 12):
        html = get_html(URL + f'?p={i}')
        links = get_glide_link(html)
        all_data = []
        for link in links:
            time.sleep(3)
            html2 = get_html(link)
            all_data.append.get_data(html2)
        print(all_data)
        
            
        
    print('________________________________________________________________________________________________________')

if __name__ == '__main__':
    main()