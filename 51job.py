from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# 优化的点：城市可以选多个

class QCWY:
    def __init__(self, city, jobclass, maxpages):
        self.city = city
        self.jobclass = jobclass
        self.maxpages = maxpages

    def run(self):
        # 隔离日志
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging']) 
        wd = webdriver.Chrome(options=options)

        # 隐式等待        
        wd.implicitly_wait(5)
        # 打开网页
        wd.get('https://www.51job.com/')
        # 获取工作地点
        address = wd.find_element(By.ID,'work_position_input')
        address.click()
        # 判断是否有已经选中的城市
        selected = wd.find_elements(By.CSS_SELECTOR, '.tin > span')
        if selected:
            for select in selected:
                select.click()
        time.sleep(1)

        cities = wd.find_elements(By.CSS_SELECTOR, 'tr > td >em')
        # print(cities.outerHTML)
        for city in cities:
            if city.text == self.city:
                city.click()
                break
        time.sleep(1)

        # 点击确定
        wd.find_element(By.CSS_SELECTOR, '#work_position_click_bottom_save').click()
        wd.find_element(By.ID, 'kwdselectid').send_keys(self.jobclass)
        wd.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/div/button').click()
        time.sleep(1)
        QCWY.get_page(self,wd)
        wd.quit()



    def get_page(self,wd):


        # 点击下一页
        for i in range(1,self.maxpages+1):
            print('第'+str(i)+'页'+"=====================================")
            _page = wd.find_element(By.CSS_SELECTOR, '#jump_page')
            # _page.clear()
            _page.send_keys(i)
            # 爬取第x页 的数据
            temp = wd.find_elements(By.CSS_SELECTOR, '.joblist-item-job-wrapper > div')
            for temp1 in temp:
                str_data = temp1.get_attribute('sensorsdata')
                str_data = json.loads(str_data)
                with open('51job.json','w',encoding='utf-8') as f:
                    json.dump(str_data,f,ensure_ascii=False)
                print(str_data['jobTitle']+':'+str_data['jobSalary'])

            

if __name__ == "__main__":
    QCWY('深圳','python',10).run()





