from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
import pytesseract
from pytesseract import image_to_string
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import re
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException


# 使用无头模式打开chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.implicitly_wait(60 * 3)
browser.maximize_window()

src = './'

start_time = time.time()


ume: str = input('请输入您的帐号(必填) :  ')        # YOUR ID
pwd: str = input('请输入您的密码（必填）:  ')        # YOUR PASSWORD
name: str = input('请输入您的名字:  ') or '用户'      # YOUR NAME
hour_goal: int = input('您的年度学习目标是多少小时？  ')       # 年度目标学时 YOU CAN CHANGE IT.


def login(ume: str, pwd: str, name: str = '用户'):  # 登录函数
    try:
        # 登录页面
        login_url = "https://www.sxgbxx.gov.cn/login"
        browser.get(login_url)

        username = browser.find_element(By.ID, "userEmail")
        ActionChains(browser).send_keys_to_element(username, ume).perform()
        # username.send_keys(ume)  # 此处填入账号
        password = browser.find_element(By.ID, 'userPassword')
        ActionChains(browser).send_keys_to_element(password, pwd).perform()
        # ActionChains(browser).send_keys_to_element(password, pwd).perform()
        # password.send_keys(pwd)  # 此处填入密码
        # 获取截图
        browser.get_screenshot_as_file(src+'/screenshot.png')

        # 获取指定元素位置
        element = browser.find_element(By.ID, 'img')
        left = int(element.location['x'])
        top = int(element.location['y'])
        right = int(element.location['x'] + element.size['width'])
        bottom = int(element.location['y'] + element.size['height'])

        # 通过Image处理图像
        im = Image.open(src+'/screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save(src+'/random.png')

        img = Image.open(src+'/random.png')
        code = pytesseract.image_to_string(img)

        randomcode = browser.find_element(By.ID, 'randomCode')
        randomcode.send_keys(code)
        browser.find_element(By.CLASS_NAME, 'bm-lr-btn').click()

        time.sleep(10)

    except WebDriverException:
        print("webdriver 异常")


def chaxun(name):               # 查询函数
    chaxun_url = 'https://www.sxgbxx.gov.cn/uc/home'
    browser.get(chaxun_url)
    shichang = browser.find_element(
        By.XPATH, '/html/body/div[1]/div[1]/div[4]/section[1]/div/div/div[2]/div/p/span[3]').text
    name = name
    print(name+'登录成功')
    print(shichang)
    T = re.findall(r'\d+', shichang)[1]
    T = int(T)

    if T > int(hour_goal):

            print('年度学习任务已完成')
            time.sleep(20)
            browser.quit()
            exit()

    else:   
        return T

    

def find_peixun():
    """获取我的专题培训课程url"""

    # https://www.sxgbxx.gov.cn/uc/plan  我的培训
    pei_url = 'https://www.sxgbxx.gov.cn/uc/plan'

    browser.get(pei_url)
    r = browser.page_source
    pei_obj = BeautifulSoup(r, "lxml")
    pei_list = pei_obj.findAll("div", {"class": "e-m-more"})  # 获取我的专题培训内容
    src = './'
    f1 = open(src+'peixun_url.txt', 'w')  # 培训课程的url

    for pid in pei_list:
        pid = str(pid)
        print(pid)
        pid = re.findall(r'id=(.+?)"', pid)
        print(pid)
        peixun_url = 'https://www.sxgbxx.gov.cn/uc/plan/info?id=' + pid[0]  # 生成培训课题的url
        browser.get(peixun_url)

        # print(browser.page_source)
        time.sleep(10)
        r = browser.page_source
        pei_obj = BeautifulSoup(r, "lxml")
        peixun_list = pei_obj.findAll("a", {"class": "lh-reply-btn"})

        for i in peixun_list:
            # print(i)
            # print(i.get_text())
            # print(i['href'])
            i = 'https://www.sxgbxx.gov.cn' + str(i['href'])
            print(i)
            f1.write(i)
            f1.write('\n')

    f1.close()
    print('专题培训url下载成功')
    
    
def find_course():
    browser.get("https://www.sxgbxx.gov.cn/front/showCourseList")
    #课程列表
    cou_url = "https://www.sxgbxx.gov.cn/front/showCourseList"
    browser.get(cou_url)
    # cou_html = urlopen(cou_url)
    # src = './'
    time.sleep(10)
    
    r = browser.page_source
    
    f1 = open(src+'cou_url.txt','w')
    f2 = open(src+'cou_name.txt','w')
    
    page = 0
    
    while page < 53:
        cou_obj = BeautifulSoup(r,"lxml")
        cou_list = cou_obj.findAll("a",{"class":"j-course-title"})

        print(page+1)
        for cou in cou_list:

            print(cou.get_text())
            print(cou['href'])


            f1.write(cou['href'])
            f1.write('\n')

            f2.write(cou.get_text())

            f2.write('\n')
        browser.find_element(By.ID, 'nextpage').click()
        time.sleep(2)
        page += 1
    f1.close()
    f2.close()

    print('课程url下载成功')    
    
def time_counter():
    
    end_time = time.time()
    study_time = (end_time - start_time) / 60
    print('已学习%s分' % study_time)   
    
def day_counter():
    
    end_time = time.time()
    study_time = (end_time - start_time) / 60   # 以分为单位
    study_time = int(study_time)                # 取整
    dtime = int(study_time / 60 / 24)           # 天
    other = study_time % (24*60) 
    htime = other // 60                         # 时
    mtime = other % 60                          # 分
    
    print('已学习%s天%s时%s分' % (dtime,htime,mtime))
    

def keicheng():
    """课程学习"""
    print('课程学习')
    # src = './'
    with open(src+'cou_url.txt', 'r') as f:
        cou_url_list = f.read().splitlines()

        # sum = len(cou_url_list)
    for cou_url in cou_url_list:
        
        print('--------------------------------------------------------------------------')
        print(cou_url)
        
        chaxun(name)
        
        browser.get(cou_url)
        # print(browser.page_source)

        browser.find_element(By.XPATH, '//*[@id="aCoursesList"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li').click()  # 切换到培训内容详情页
        # print(browser.page_source)
        cou_obj = BeautifulSoup(browser.page_source, 'lxml')
        time.sleep(3)
        li_list = cou_obj.findAll('li')  # 找到所有培训课程
        # print('--------------------------------------')
        # print(li_list)
        

        for li in li_list:
            

            day_counter()
            # time_counter()

            li_html = str(li)
            # print('--------------------------------------')
            # print(li_html)
            if 'kpoint_list' not in li_html:
                continue
            id = re.findall(r'kp_\d+', li_html)
            id = ''.join(id)
            print(id)

            if '视频播放' in li_html:
                if '100%' in li_html:
                    continue
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                # print('看视频')
                # print("本视频长%s秒" % shichang)
                # print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element(By.ID, id).click()
                time.sleep(3)
                action = ActionChains(browser)
                # title = browser.find_element_by_xpath('//*[@id="N-course-box"]/article/div/div[2]/section/h3/span')  # 鼠标移动到标题
                # action.move_to_element(title).click().perform()
                time.sleep(20)
                action.send_keys(Keys.SPACE).perform()  # 单击空格
                time.sleep(t + 40)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()
                

            elif '音频播放' in li_html:
                if '100%' in li_html:
                    continue
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                # print('听音频')
                # print("本音频长%s秒" % shichang)
                # print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element(By.ID, 'yp_play').click()
                time.sleep(t + 20)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '随堂小测验' in li_html:
                continue

            else:
                if '100%' in li_html:
                    continue
                print('读文字')
                browser.find_element(By.ID, id).click()
                time.sleep(5)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()
            


def kecheng_random():
    """课程学习"""
    print('课程学习')
    # src = './SXHGB/'
    with open(src+'cou_url.txt', 'r') as f:
        cou_url_list = f.read().splitlines()
        sum = len(cou_url_list)

    for x in range(1, 100):  # 每次随机学习，学习100次
        
        chaxun(name)

        # 课程学习页面
        cou_url = (cou_url_list[random.randint(1, sum - 1)])
        print('--------------------------------------------------------------------------')
        print(cou_url)
        
        browser.get(cou_url)
        # print(browser.page_source)

        browser.find_element(By.XPATH,
            '//*[@id="aCoursesList"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li').click()  # 切换到培训内容详情页
        # print(browser.page_source)
        cou_obj = BeautifulSoup(browser.page_source, 'lxml')
        time.sleep(3)
        li_list = cou_obj.findAll('li')  # 找到所有培训课程
        # print('--------------------------------------')
        # print(li_list)
        

        for li in li_list:
            

            day_counter()

            li_html = str(li)
            # print('--------------------------------------')
            # print(li_html)
            if 'kpoint_list' not in li_html:
                continue
            id = re.findall(r'kp_\d+', li_html)
            id = ''.join(id)
            # print(id)

            if '视频播放' in li_html:
                if '100%' in li_html:
                    continue
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                # print('看视频')
                # print("本视频长%s秒" % shichang)
                # print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element(By.ID, id).click()
                time.sleep(3)
                action = ActionChains(browser)
                # title = browser.find_element_by_xpath('//*[@id="N-course-box"]/article/div/div[2]/section/h3/span')  # 鼠标移动到标题
                # action.move_to_element(title).click().perform()
                time.sleep(20)
                action.send_keys(Keys.SPACE).perform()  # 单击空格
                time.sleep(t + 40)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '音频播放' in li_html:
                if '100%' in li_html:
                    continue
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                # print('听音频')
                # print("本音频长%s秒" % shichang)
                # print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element(By.ID, 'yp_play').click()
                time.sleep(t + 20)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '随堂小测验' in li_html:
                continue

            else:
                if '100%' in li_html:
                    continue
                print('读文字')
                browser.find_element(By.ID, id).click()
                time.sleep(5)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()
            



def peixun():
    
    """专题培训学习"""
    print('专题学习')
    with open(src+'peixun_url.txt', 'r') as f:
        cou_url_list = f.read().splitlines()

        # sum = len(cou_url_list)
    for pei_url in cou_url_list:
        chaxun(name)
        print('-----------------------------------------------------------------------------------')
        
        print(pei_url)
        
        browser.get(pei_url)
        # print(browser.page_source)

        browser.find_element(By.XPATH,
            '//*[@id="aCoursesList"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li').click()  # 切换到培训内容详情页
        # print(browser.page_source)
        cou_obj = BeautifulSoup(browser.page_source, 'lxml')
        time.sleep(3)
        li_list = cou_obj.findAll('li')  # 找到所有培训课程
        # print('--------------------------------------')
        # print(li_list)
        
        
        for li in li_list:
            
            
            day_counter()
            li_html = str(li)
            # print('--------------------------------------')
            # print(li_html)
            if 'kpoint_list' not in li_html:
                continue
            id = re.findall(r'kp_\d+', li_html)
            id = ''.join(id)
            print(id)

            if '视频播放' in li_html:
                if '100%' in li_html:
                    continue
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                # print('看视频')
                # print("本视频长%s秒" % shichang)
                # print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element(By.ID, id).click()
                time.sleep(3)
                action = ActionChains(browser)
                # title = browser.find_element_by_xpath('//*[@id="N-course-box"]/article/div/div[2]/section/h3/span')  # 鼠标移动到标题
                # action.move_to_element(title).click().perform()
                time.sleep(20)
                action.send_keys(Keys.SPACE).perform()  # 单击空格
                time.sleep(t + 40)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '音频播放' in li_html:
                if '100%' in li_html:
                    continue
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                # print('听音频')
                # print("本音频长%s秒" % shichang)
                # print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element(By.ID, 'yp_play').click()
                time.sleep(t + 20)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '随堂小测验' in li_html:
                continue

            else:
                if '100%' in li_html:
                    continue
                print('读文字')
                browser.find_element(By.ID, id).click()
                time.sleep(5)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()
            


def peixun_random():
    """专题培训学习"""
    print('专题学习')
    with open(src+'peixun_url.txt', 'r') as f:
        cou_url_list = f.read().splitlines()

        sum = len(cou_url_list)

    for x in range(1, 100):  # 每次随机学习，学习100次

        chaxun(name)
        
        # 培训页面
        pei_url = (cou_url_list[random.randint(1, sum - 1)])
        # for pei_url in cou_url_list:
        
        browser.get(pei_url)
        print('--------------------------------------')
        print(pei_url)
        # print(browser.page_source)

        browser.find_element(By.XPATH,
            '//*[@id="aCoursesList"]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/ul/li').click()  # 切换到培训内容详情页

        # print(browser.page_source)
        cou_obj = BeautifulSoup(browser.page_source, 'lxml')
        time.sleep(3)
        li_list = cou_obj.findAll('li')  # 找到所有培训课程
        # print('--------------------------------------')
        # print(li_list)
        
        
        for li in li_list:
            
            
            day_counter()

            li_html = str(li)
            # print('--------------------------------------')
            # print(li_html)
            if 'kpoint_list' not in li_html:
                continue
            id = re.findall(r'kp_\d+', li_html)
            id = ''.join(id)
            print(id)
        
            if '视频播放' in li_html:
                if '100%' in li_html:
                    continue
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                # print('看视频')
                # print("本视频长%s秒" % shichang)
                # print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element(By.ID, id).click()
                time.sleep(3)
                action = ActionChains(browser)
                # title = browser.find_element_by_xpath('//*[@id="N-course-box"]/article/div/div[2]/section/h3/span')  # 鼠标移动到标题
                # action.move_to_element(title).click().perform()
                time.sleep(20)
                action.send_keys(Keys.SPACE).perform()  # 单击空格
                time.sleep(t + 40)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '音频播放' in li_html:
                if '100%' in li_html:
                    continue
                title = li.get_text()  # 找到课程标题
                print(title)
                shichang = re.findall(r'\d+分\d+秒', li_html)
                shichang = re.findall(r'\d+', str(shichang))
                shichang = int(shichang[0]) * 60 + int(shichang[1])
                percent = re.findall(r'\d+\%', li_html)
                percent = re.findall(r'\d+', str(percent))
                percent = int(percent[0])
                # print('听音频')
                # print("本音频长%s秒" % shichang)
                # print("已学习%d%%" % percent)
                t = shichang * (100 - percent) * 0.01
                browser.find_element(By.ID, 'yp_play').click()
                time.sleep(t + 20)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()

            elif '随堂小测验' in li_html:
                continue

            else:
                print('读文字')
                browser.find_element(By.ID, id).click()
                time.sleep(5)
                print(li.get_text() + "学习完毕")
                print('\n')
                print('\n')
                browser.refresh()
            


if __name__ == "__main__":

    
    def study():
            
              
        
        login(ume, pwd, name)
        
        T = chaxun(name)
        
        # if T > int(hour_goal):
            
        #     print('年度学习任务已完成')
        #     time.sleep(20)
        #     browser.quit()
        #     exit()
            
       
        # 获取专题培训url
        # find_peixun()

        # 获取课程url
        # find_course()

        # 完成课程学习功能
        # print(name+"课程学习开始")
        # kecheng_random()
        keicheng()
        # print(name+"课程学习结束")

        # 完成专题培训学习功能
        print(name+"专题培训开始")

        peixun()               # 顺序学习
        # peixun_random()           # 随机学习
        # print(name+"专题培训结束")
        time.sleep(10)
        print('**************************************************************************************************************************')

    try:
        study()
    except:
        study()




    browser.quit()
    exit()


    
