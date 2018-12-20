# from selenium import webdriver
# from bs4 import BeautifulSoup
#
# # chrome driver setting
# driver = webdriver.Chrome(r'C:\Users\student\Desktop\chromedriver_win32\chromedriver.exe')
#
# # open website
# driver.get("http://www.10000recipe.com/recipe/list.html")
#
# # find search box / if element is made by id
# searchText = driver.find_element_by_id("srhRecipeText")
# searchText.send_keys("우유")
#
# # if button is made by class
# bt1 = driver.find_element_by_css_selector("button.btn.btn-default")
# bt1.click()
#
# source = driver.page_source
# soup = BeautifulSoup(source, "html.parser")
#
# for i in soup.find_all("h4", class_="ellipsis_title2"):
#     print(i.get_text())

