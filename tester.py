from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from anytree import AnyNode, RenderTree
from anytree.exporter import UniqueDotExporter
import requests
from html_similarity import *

driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path="geckodriver.exe")
original_link = 'http://127.0.0.1:8000/'
site_name = '127.0.0.1'

def get_next_links(link, tn, tn_root, level):
        #driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path="geckodriver.exe")
        
        driver.get(link)
        fn = link
        if level != 0:
            fn = link.replace(original_link,"")
        fn = fn.replace("/", ".")
        fn = fn.replace(":", "")
        with open('html_files/'+fn+".html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        list_done.append(link)
        list_links = driver.find_elements_by_tag_name('a')
        print('lengte:', len(list_done))
        print('lengte:', len(list_links))
        for i in range(len(list_links)):
            #driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path="geckodriver.exe")
            #driver.set_page_load_timeout(5)
            
            print('current page:'+link)
            driver.get(link)
            list_links = driver.find_elements_by_tag_name('a')
            #print(list_links)
            next_link = list_links[i].get_attribute('href')
            tn_next = AnyNode(id=next_link, name=next_link, parent=tn, level = level)
            #tn.add_child(tn_next)
            UniqueDotExporter(tn_root).to_dotfile(site_name+".dot")
            if next_link != '' and 'http' in next_link and not next_link in list_done and site_name in next_link:
                print('van:', link, 'naar:',list_links[i].get_attribute('href'))
                try:
                    #driver.quit()
                    get_next_links(next_link, tn_next, tn_root, level+1)
                except Exception as inst:
                    #driver.quit()
                    print('Something went wrong when trying to load:', next_link)
                    f = open('errors.log', 'a')
                    f.write(str(inst))
                    f.write(str(list_links[i])+'\n')
                    f.write('op pagina '+link+'\n\n')
                    f.close()
                    print('Error message saved to log')
            

tn_root = AnyNode(id=original_link, name=original_link, level = 0)    
get_next_links(original_link, tn_root, tn_root, 1)
print(RenderTree(tn_root))
print(tn_root.children)
driver.quit()