from selenium import webdriver
driver = webdriver.PhantomJS()
driver.get('https://psxdatacenter.com/psx2/ntsc-u_list2.html')
p_element = driver.find_element_by_id(id_='table302')
print(p_element.text)
# result:
'Yay! Supports javascript'