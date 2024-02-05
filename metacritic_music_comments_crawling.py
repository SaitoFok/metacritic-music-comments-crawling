import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re

def get_one_song_info(s_style, l): #得到一首歌的评论
    driver.get(l)
    ss = re.search("(?<=date/).+", s_style).group()
    txt = "./pages/comments_"+ss+".txt"
    f_getmeta = open(txt,'a')
    while True:
        time.sleep(2)
        ex = driver.find_elements(By.XPATH, '//span[@class="toggle_expand_collapse toggle_expand"]')
        for i in ex:
            i.click()
        for c in driver.find_elements(By.XPATH, '//div[@class="body product_reviews"]//div[@class="review_body"]'):
            content = c.text.replace("Collapse","").replace("This review contains spoilers.","").replace("\n","").strip()
            f_getmeta.write(content+"\n")
        try:
            ret = driver.find_element(By.XPATH, '//a[@rel="next"]').get_attribute("href")
            driver.implicitly_wait(5)
            driver.get(ret)
        except:
            print(l, "Successfully executed!")
            break
    f_getmeta.close()

def get_songs_of_same_genre(s_style): # 得到同一风格的歌曲
    driver.get(s_style)
    while True:
        ex = driver.find_elements(By.XPATH, '//label[@class="clamp-list-expand-label"]')
        for i in ex:
            i.click()

        songs = driver.find_elements(By.XPATH, '//div[@class="clamp-userscore"]//a[@class="metascore_anchor"]')
        ls = []
        for song in songs:
            if song.text != "tbd":
                ls.append(song.get_attribute("href"))
        
        for l in ls:
            get_one_song_info(s_style, l) #获取一首歌的信息

        try:
            ret = driver.find_element(By.XPATH, '//a[@rel="next"]').get_attribute("href")
            driver.implicitly_wait(15)
            driver.get(ret)
        except:
            print(s_style, "Successfully executed!")
            break
    
def get_styles(): #得到不同风格的网站，在不同风格网站下面采集数据
    driver.get("https://www.metacritic.com/music")
    d = []
    for p in range(27,28):
        pa = '//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div/div/div/ul/li['+str(p)+']/a'
        d.append(driver.find_element(By.XPATH, pa).get_attribute("href")) # 得到所有风格网站的列表

    for s_style in d:
        get_songs_of_same_genre(s_style)     
    driver.close()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    get_styles()