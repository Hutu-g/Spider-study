import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import Config

def isElementExist(driver):
    flag=True
    sale = driver.find_element(By.CLASS_NAME,'no-br').text
    if "点起售" in sale:
        flag = False
    return flag


def get_ticket(conf, driver, url):
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined})"""})
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(5)
    login = driver.find_element(by=By.ID, value='J-btn-login')
    login.click()
    driver.implicitly_wait(10)

    # 账号密码登录
    # username_tag = driver.find_element(by=By.ID, value='J-userName')
    # username_tag.send_keys(conf.username)
    # password_tag = driver.find_element(by=By.ID, value='J-password')
    # password_tag.send_keys(conf.password)
    # login_now = driver.find_element(by=By.ID, value='J-login')
    # login_now.click()
    # time.sleep(2)
    # very = driver.find_element(By.ID,'id_card')
    # very_input = input("请输入身份证后四位: ")
    # very.send_keys(very_input)
    # driver.find_element(By.ID,'verification_code').click()
    # phone_code_input = input("请输入手机验证码: ")
    # phone_code = driver.find_element(By.ID,'code')
    # phone_code.send_keys(phone_code_input)
    # driver.find_element(By.ID,'sureClick').click()
    # time.sleep(2)




    # # 过滑动验证码
    # picture_start = driver.find_element(by=By.ID, value='nc_1_n1z')
    # # 移动到相应的位置，并左键鼠标按住往右边拖
    # ActionChains(driver).move_to_element(picture_start).click_and_hold(picture_start).move_by_offset(300, 0).release().perform()


    # 扫码登录
    scan_QR = driver.find_element(by=By.XPATH, value='//*[@id="toolbar_Div"]/div[2]/div[2]/ul/li[2]/a')
    scan_QR.click()
    driver.implicitly_wait(10)


    # 点提示框
    # try:
    #     driver.find_element(by=By.XPATH, value='//div[@class="dzp-confirm"]/div[2]/div[3]/a').click()
    #     driver.implicitly_wait(5)
    # except:
    #     pass

    time.sleep(2)
    # 点击车票预订跳转到预订车票页面
    driver.find_element(by=By.XPATH, value='//*[@id="link_for_ticket"]').click()
    driver.implicitly_wait(10)
    # 输入出发地和目的地信息
    # 出发地
    driver.find_element(by=By.XPATH, value='//*[@id="fromStationText"]').click()
    driver.find_element(by=By.XPATH, value='//*[@id="fromStationText"]').clear()
    driver.find_element(by=By.XPATH, value='//*[@id="fromStationText"]').send_keys(conf.fromstation)
    time.sleep(1)
    driver.find_element(by=By.XPATH, value='//*[@id="fromStationText"]').send_keys(Keys.ENTER)

    # 目的地
    destination_tag = driver.find_element(by=By.XPATH, value='//*[@id="toStationText"]')
    destination_tag.click()
    destination_tag.clear()
    destination_tag.send_keys(conf.destination)
    time.sleep(1)
    destination_tag.send_keys(Keys.ENTER)
    driver.implicitly_wait(5)

    # 出发日期
    date_tag = driver.find_element(by=By.XPATH, value='//*[@id="train_date"]')
    date_tag.click()
    date_tag.clear()
    date_tag.send_keys(conf.date)
    time.sleep(1)
    query_tag = driver.find_element(by=By.XPATH, value='//*[@id="query_ticket"]')

    start = time.time()

    while True:
        driver.implicitly_wait(5)
        # 点击查询
        driver.execute_script("$(arguments[0]).click()", query_tag)

        # 判断页面中是否开售状态 如果没有开售则进入等待
        if not isElementExist(driver):
            # 车票处于待开售状态
            print(f"现在是{time.strftime('%H:%M:%S', time.localtime())}，还未开始售票")
            # 每隔两分钟刷新一次，否则3分钟内无购票操作12306系统会自动登出
            if time.time() - start >= 120:
                driver.refresh()
                start = time.time()
            time.sleep(1)
            continue

        # 获取所有车票
        tickets = driver.find_elements(by=By.XPATH, value='//*[@id="queryLeftTable"]/tr')
        # 每张车票有两个tr，但是第二个tr没什么用
        tickets = [tickets[i] for i in range(len(tickets) - 1) if i % 2 == 0]
        #print(tickets)
        for ticket in tickets:
            # 如果车票的车次等于想要的车次并且硬卧的状态不是候补则点击预订
            #if ticket.find_element(by=By.CLASS_NAME,value='cdz').text== conf.fromstation:
                #print(ticket.find_element(by=By.CLASS_NAME,value='number').text)
                # value = '//td[8]'表示硬卧，td[10]表示硬座
            ticket_type = 10
            if conf.traintype == "硬卧":
                ticket_type = 8
            if ticket.find_element(by=By.CLASS_NAME,value='number').text == conf.trainnumber and ticket.find_element(By.XPATH,f'//td[{ticket_type}]').text != "候补":
                # 点击预订
                #print(ticket.find_element(by=By.CLASS_NAME,value='cdz').text)
                #time.sleep(1)
                ticket.find_element(by=By.CLASS_NAME, value='btn72').click()
                # 这里之后就不能继续使用ticket.find_element()了，因为页面进行了跳转，会出现stale element reference: element is not attached to the page document的错误
                # 我们可以使用driver.find_element()
                '//*[@id="normal_passenger_id"]/li[1]/label'
                # 选择车票人 选择车票类型
                for i in range(0,conf.trainPeopleNum):
                    driver.find_element(by=By.XPATH, value=f'//*[@id="normalPassenger_{i}"]').click()
                    tran_people = driver.find_element(By.XPATH,f'//*[@id="normal_passenger_id"]/li[{i+1}]/label')
                    if "学生" in tran_people.text:
                        driver.find_element(by=By.XPATH, value='//*[@id="dialog_xsertcj_ok"]').click()
                    else:
                        pass

                    # ticket_type = driver.find_elements(By.ID,'seatType_1')
                    # for type in ticket_type:
                    #     types =  type.find_element(By.TAG_NAME,'option')
                    #     if  conf.traintype in types.text:
                    #         types.click()
                # 提交订单
                # time.sleep(60)
                driver.find_element(by=By.XPATH, value='//*[@id="submitOrder_id"]').click()
                #这里直接使用id和xpath定位不到，所以直接加上他的路径,可以不用这么长，但是懒得删
                try:
                    driver.find_element(by=By.XPATH, value='//html/body/div[5]/div/div[5]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[2]/ul[2]/li[2]/a[@id="1F"]').click()
                except:
                    pass
                # 确认提交订单，然后这里和上面是一样的
                driver.find_element(by=By.ID, value='qr_submit_id').click()
                print(f"{conf.trainnumber}次列车抢票成功，请尽快在10分钟内支付！")
                return


if __name__ == '__main__':
    conf = Config()
    url = 'https://www.12306.cn/index/'
    driver = webdriver.Chrome()
    get_ticket(conf, driver, url)
    time.sleep(10)
    driver.quit()
