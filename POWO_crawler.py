import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import re
import time
import winsound
import pandas as pd
from multiprocessing.dummy import Pool
from selenium.webdriver.chrome.options import Options
from pynput.keyboard import Key, Controller
import asyncio
import aiohttp
from aiohttp import TCPConnector


'''
url = "https://powo.science.kew.org/results?f=species_f%2Caccepted_names&cursor=*&p=0&page.size=480"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
          "Connection": "keep-alive"}
response = requests.get(url = url, headers = header)
print(response.text)
'''


async def powo_crawl(url):
    # keyboard = Controller()
    species = []
    native_range = []
    distributions = []
    native_to = []
    ##########################################
    chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('blink - settings = imagesEnabled = false')
    ##########################################
    bro = webdriver.Chrome(executable_path="./chromedriver", chrome_options = chrome_options)
    bro.get(url)
    sleep(15)
    web = bro.page_source
    #next_page = "https://powo.science.kew.org/results?f=species_f%2Caccepted_names&cursor=" + re.findall("\<a data-cursor\=\"(.*?)\"", str(web))[0].strip()
    specie_urls = re.findall("(\/taxon\/urn\:lsid\:ipni.*?)\"", str(web))
    if len(specie_urls) != 480:
        winsound.Beep(500, 1000)
    print(len(specie_urls))
    # timer1 = 0
    # timer2 = 0
    # timer3 = 0
    for i in specie_urls:
        # sleep(0.5)
        new_url = "https://powo.science.kew.org" + i.strip()
        print(new_url)
        #with open("C:/Users/chufeng zhao/Desktop/powo/powo_species_urls_adding.txt", 'a', encoding="utf-8") as psua:
        #    psua.write(new_url+"\n")
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Connection": "close"}
        # new_page = requests.get(url=new_url, headers=header).text
        # 异步代码
        # async with aiohttp.ClientSession(connector=TCPConnector(ssl=False), trust_env=True) as session:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(new_url, headers=header) as response:
                new_page = await response.text()

        # new_page = requests.get(url=new_url, headers=header, verify=False)
        # new_page.encoding = "UTF-8"
        # new_page = new_page.text
        # new_page.content.decode("utf8", "ignore").encode("utf8", "ignore")
        # bsoj = BeautifulSoup(new_page)
        ######
        '''
        if bsoj.h1.find_all(lang="la")[0]:
            species.append(BeautifulSoup(next_page).h1.find_all(lang="la")[0].get_text().strip())
            timer1 += 1
            print("species count", timer1)
            # winsound.Beep(600, 500)
        '''
        if re.findall("\<meta property\=\"og\:title\" content\=\".*?\s\|", new_page):
            species.append(re.findall("\<meta property\=\"og\:title\" content\=\"(.*?)\|", new_page)[0].strip())
            # timer1 += 1
            # print("species count", timer1)
            print("species count", len(species))
            # winsound.Beep(600, 500)
        else:
            species.append("none")
        '''
        if bsoj.find_all(class_ = "details")[0]:
            native_range.append(BeautifulSoup(next_page).find_all(class_ = "details")[0].get_text().strip())
            timer2 += 1
            print("native range count", timer2)
        '''
        if re.findall("\<p class\=\"p\"\>", new_page):
            native_to.append(re.findall("\<p class\=\"p\"\>(.*?)\<\/p", new_page, flags=re.S)[0].strip())
            # timer1 += 1
            # print("species count", timer1)
            print("Native to count", len(native_to))
            # winsound.Beep(600, 500)
        else:
            native_to.append("none")

        if re.findall("\<div class\=\"details p\"\>\s*\n?\s*(.*?)\n?\s*?\<\/d", new_page):
            # native_range.append(re.findall("\<div class\=\"details\"\>\s*\n?\s*(.*?)\n?\s*?.*?\<", new_page)[0].strip())
            native_range.append(re.findall("\<div class\=\"details p\"\>(.*?)\<\/d", new_page, flags=re.S)[0].strip())
            # timer2 += 1
            # print("native range count", timer2)
            print("native range count", len(native_range))
        else:
            native_range.append("none")
        if re.findall("\<span class\=\"description\-type\-list\-item\"\>Distribution\<\/span\>.*?\<dd\>(.*?)\<\/dd", new_page, flags=re.S):
            distributions.append(re.findall("\<span class\=\"description\-type\-list\-item\"\>Distribution\<\/span\>.*?\<dd\>(.*?)\<\/dd", new_page, flags=re.S)[0].strip())
            # timer3 += 1
            #print("distribution count", timer3)
            print("distribution count", len(distributions))
#        elif re.findall("\<h3\>Native to:\<\/h3\>"):
#            distributions.append(re.findall("\<h3\>Native to:\<\/h3\>.*?\>(.*?)\<", new_page, flags=re.S))[0].strip()
        else:
            distributions.append("None")
    # winsound.Beep(600, 2000)
    #with open("C:/Users/chufeng zhao/Desktop/powo/powo_page_got.txt", 'a', encoding="utf-8") as psug:
    #    psug.write(url + "\n")
    #with open("C:/Users/chufeng zhao/Desktop/powo/powo_info_adding.txt", 'a', encoding="utf-8") as pinfo:
    #    pinfo.write(str(species)+"|"+str(native_range)+"|"+str(distributions)+"\n")
    # keyboard.type("Count" + str(url))
    # keyboard.press(Key.enter)
    # keyboard.release(Key.enter)
    # keyboard.press(Key.enter)
    # keyboard.release(Key.enter)
         # response.close()
    return species, native_to, native_range, distributions
# url = "https://powo.science.kew.org/results?f=species_f%2Caccepted_names&cursor=*&p=0&page.size=480"


def func1(url):
    ##########################################
    chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument('blink - settings = imagesEnabled = false')
    ##########################################
    bro = webdriver.Chrome(executable_path="E:/python_projects/pycharm/powa爬虫/chromedriver", chrome_options = chrome_options)
    bro.get(url)
    sleep(15)
    web = bro.page_source
    objt = BeautifulSoup(web)
    # next_page = "https://powo.science.kew.org/results?f=species_f%2Caccepted_names&cursor=" + re.findall("\<a data-cursor\=\"(.*?)\"", str(web))[1].strip() + "&page.size=480"
    # next_page = "https://powo.science.kew.org/results" + \
    #            re.findall("href\=.*?\/(.*?)\"\>Next", str(web))[0].strip()
    next_page = "https://powo.science.kew.org/results" + objt.find(id="paginate-next").a["href"][1:]
    if len(re.findall("(\/taxon\/urn\:lsid\:ipni.*?)\"", str(web))) != 480:
        winsound.Beep(500, 500)
    print("Last pages contains: "+str(len(re.findall("(\/taxon\/urn\:lsid\:ipni.*?)\"", str(web)))))
    #next_page = "https://powo.science.kew.org/results?f=accepted_names&page.size=480&cursor=" + \
    #            re.findall("\<a data-cursor\=\"(.*?)\"", str(web))[1].strip()
    return next_page


if __name__ == '__main__':
    flag1 = True
    top_counter =108
    # top_counter = 54
    # start_page = "https://powo.science.kew.org/results?f=%2Caccepted_names%2Cspecies_f&page.size=480&cursor=*&p=0"
    # start_page = "https://powo.science.kew.org/results?f=%2Caccepted_names%2Cspecies_f&page.size=480&cursor=AoMIP4AAAD8ANjAwUnViaWFjZWFlUGVudGFuaXNpYWxvbmdpdHViYStUYXhvbl82NTg5MA%3D%3D&p=660"
    # start_page = "https://powo.science.kew.org/results?f=%2Caccepted_names%2Cspecies_f&page.size=480&cursor=AoMIP4AAADs2MDBSdXRhY2VhZURydW1tb25kaXRhZnVsdmEtVGF4b25fMTAxNzM3Mg%3D%3D&p=672"
    # start_page = "https://powo.science.kew.org/results?f=%2Caccepted_names%2Cspecies_f&page.size=480&cursor=AoMIP4AAAD8ANjAwVXJ0aWNhY2VhZVBvdXpvbHppYXNheG9waGlsYSxUYXhvbl85NTUyNjE%3D&p=714"
    start_page = "https://powo.science.kew.org/results?f=%2Caccepted_names%2Cinfraspecific_f&page.size=480&cursor=AoMIP4AAAD8QNzAwVXJ0aWNhY2VhZVBpcHR1cnVzcG9seW5lc2ljdXN2YXIubWVsYW5lc2ljdXMtVGF4b25fMTA0MDA1Mg%3D%3D&p=108"
    # with open("C:/Users/chufeng zhao/Desktop/powo/start_page.txt", "a", encoding="utf-8") as sp:
    #    sp.write(str(top_counter)+"===> "+start_page+"\n")
    while flag1:
        with open("C:/Users/chufeng zhao/Desktop/powo/start_page.txt", "a", encoding="utf-8") as sp:
            sp.write(str(top_counter) + "===> " + start_page + "\n")
        #keyboard3 = Controller()
        #keyboard3.type("Starting number is " + str(top_counter) + " ;url is " + start_page)
        #keyboard3.press(Key.enter)
        #keyboard3.release(Key.enter)
        #keyboard3.press(Key.enter)
        #keyboard3.release(Key.enter)
        #keyboard3 = Controller()
        # pages = ["https://powo.science.kew.org/results?f=species_f%2Caccepted_names&cursor=AoMIP4AAAD8ENjAwQWNhbnRoYWNlYWVDYXJsb3dyaWdodGlhaGludG9uaWksVGF4b25fMjk4MjQx&page.size=480"]
        # pages = ["https://powo.science.kew.org/results?f=species_f%2Caccepted_names&cursor=*&p=0&page.size=480"]
        # pages = ["https://powo.science.kew.org/results?f=%2Caccepted_names%2Cspecies_f&page.size=480&cursor=*&p=0"]
        pages = [start_page]
        # pages = ["https://powo.science.kew.org/results?f=accepted_names&page.size=480"]
        count = 1
        flag = True
        sps = []
        nato = []
        nrs = []
        dis = []
        timer1 = time.time()
        while flag:
            #with open("C:/Users/chufeng zhao/Desktop/powo/powo_pages_adding.txt", "a", encoding="utf-8") as pp:
            #    pp.write(pages[-1]+"\n")
            next_page = func1(pages[-1])
            pages.append(next_page)
            count += 1
            print("New added page was", next_page)
            print("Total pages are", str(len(pages)))
            # keyboard2.type("get " + str(next_page)+";total pages are "+ str(len(pages)))
            # keyboard2.press(Key.enter)
            # keyboard2.release(Key.enter)
            # keyboard2.press(Key.enter)
            # keyboard2.release(Key.enter)
            if count == 3: # 81, 输入每轮获取页面数
                flag = False
        #with open("C:/Users/chufeng zhao/Desktop/powo/powo_all_pages.txt", "w", encoding="utf-8") as pa:
        #    pa.write(str(pages))
        # start_page = func1(pages[-1])
        winsound.Beep(500, 300)

        # 方法一：多进程
        '''
        pool = Pool(1)
        time1 = time.time()
        res = pool.map(powo_crawl, pages)
        time2 = time.time()
        print(time2 - time1)
        # print(res)
        print(len(res))
        with open("C:/Users/chufeng zhao/Desktop/powo/powo.txt", "w", encoding="utf-8") as powo:
            powo.write(str(res))
        winsound.Beep(500, 300)
        winsound.Beep(500, 300)


        for i in res:
                sps += i[0]
                nrs += i[1]
                dis += i[2]
        '''

        # 方法二：单线程串联
        # time1 = time.time()
        '''
        for i in pages:
            #winsound.Beep(600, 2000)
            sp, nr, di = powo_crawl(i)
            sps += sp
            nrs += nr
            dis += di
        # time2 = time.time()
        # print(time2 - time1)
        '''
        # 方法三：基于协程的异步
        tasks = []
        for i in pages:
            c = powo_crawl(i)
            task = asyncio.ensure_future(c)
            tasks.append(task)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        for i in tasks:
            sps += i.result()[0]
            nato += i.result()[1]
            nrs += i.result()[2]
            dis += i.result()[3]


        res_data = pd.DataFrame({"species": sps,"native to": nato, "native range": nrs, "distribution": dis})
        res_data.to_csv("C:/Users/chufeng zhao/Desktop/powo/csv/powo_"+str(top_counter)+".csv", encoding="utf-8")
        print("Total number of accepted species in Powo are", len(res_data["species"]))
        timer2 = time.time()
        print("Time is", str(timer2-timer1))
        top_counter += 6 # 81 累加每轮获取页面数

        # winsound.Beep(500, 300)
        # winsound.Beep(500, 300)
        # winsound.Beep(500, 300)
        if top_counter == 736: # 729 总页面数，终止循环条件
            flag1 = False
