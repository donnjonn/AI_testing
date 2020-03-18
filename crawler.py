from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
list_done = []
binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options = Options()
options.set_headless(headless=True)
options.binary = binary
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True
driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path="geckodriver.exe")

original_link = 'http://automationpractice.com'
site_name = 'automationpractice'
class treeNode:
    def __init__(self, link, parent):
        self.parent = parent
        self.link = link
        self.childs = []
    def add_child(self, child):
        self.childs.append(child)
        
def get_link(link, tn):
    print(link)
    if site_name in link and not link in list_done:
        driver.get(link);
        list_done.append(link)
        list_links = driver.find_elements_by_tag_name('a')
        print(list_done)
        for i in list_links:
            
            next_link = i.get_attribute('href')
            tn_next = treeNode(next_link, tn)
            tn.add_child(tn_next)
            if next_link != '':
                try:
                    print('link:',i.get_attribute('href'))
                    get_link(next_link, tn)
                except Exception as inst:
                    print('Something went wrong when trying to load:', next_link)
                    f = open('errors.log', 'a')
                    f.write(str(inst))
                    f.write(str(i)+'\n')
                    f.write('op pagina '+link+'\n\n')
                    f.close()
                    print('Error message saved to log')
            

tn = treeNode(original_link, None)    
get_link(original_link, tn)
print(tn.childs)
driver.quit()