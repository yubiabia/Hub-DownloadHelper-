from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import json
import time
#Go to Insendi
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"block_third_party_cookies": False})
browser = webdriver.Chrome('C:/WebDriver/chromedriver', options=chrome_options)#replace PATH with the path of your chromedriver
browser.get('https://imperial.insendi.com/login?returnPath=/programmes') #go to Imperial's insendi navigation page
browser.find_element_by_xpath('//*[@id="__next"]/div/div/div[1]/section/div/div/a[1]').click() #For course material download: click on internal log-in 

#login Input
username = browser.find_element_by_id("username")
password = browser.find_element_by_id("password")
name_input=input("Input your user name: ")
pw_input=input("Input your password: ")
username.send_keys(name_input)
password.send_keys(pw_input)

#Submit Login
browser.find_element_by_name("_eventId_proceed").click()
# # Retrieve Courses
#Get all courses 
time.sleep(2) #get list of modules
items = browser.find_elements_by_xpath('//div[@class="grid"]/a[@class="card is-horizontal is-shadowless CourseCardHorizontal__root has-subtitle-animation"]')
courses=[]
i=1
for item in items:
    #course name
    coursename=item.find_element_by_xpath('.//h2[@class="subtitle break-long-words is-5 has-ellipsis-line-2 is-marginless"]').text
    #course period
    try:
        courseperiod=item.find_element_by_xpath('.//span[@class="has-text-grey"]').text
    except:
        courseperiod="NA" 
    courses.append((i,coursename))
    i+=1
print(*courses,sep="\n")
courseNo=input("To select a module, enter the serial number: ")#select module number
task=[courseNo]
while courseNo is not None:
    # Navigate to a course
    browser.find_element_by_xpath('//*[@id="__next"]/div/div/section[2]/div/div/div[1]/a['+courseNo+']').click()
    # go to module page
    try:
        element = WebDriverWait(browser, 10).until(
            lambda x: x.find_element_by_xpath('//*[@data-test-id="ProgrammeMenu(cmenu.x-9siz3ul)__NavbarItem--item"]'))
    except:
        print("The module does not have any files uploaded")
        print(*courses,sep="\n")
        More=input("Any other module? If not, please enter -1 to exit")
        if int(More) in range(1,len(courses)):
            task.append(More)
            courseNo=More
            continue
        else:
            print("Thank you~ Happy Learning <3")
            courseNo=None
            break
    browser.find_element_by_xpath('//*[@data-test-id="ProgrammeMenu(cmenu.x-9siz3ul)__NavbarItem--item"]').click()

    element1= WebDriverWait(browser, 10).until(
        lambda x: x.find_element_by_xpath('//*[@id="__next"]/div/div/section/div/div[2]/div/div/div/div/div/iframe'))
    #navigate to the actual iframe for embedded dropbox 
    frame = browser.find_element_by_xpath('//*[@id="__next"]/div/div/section/div/div[2]/div/div/div/div/div/iframe')
    browser.switch_to.frame(frame)
    browser.implicitly_wait(2)
    sub_frame=browser.find_element_by_xpath('//*[@id="app"]/main/div/iframe')
    browser.switch_to.frame(sub_frame)
    time.sleep(10)
    browser.find_element_by_xpath('//*[@id="embedded-app"]/div/div/div/div[1]/div/div/div[2]/button').click()
    time.sleep(5) #wait until downloading is start
    #download all files under the module
    browser.switch_to.default_content()
    browser.find_element_by_xpath('//*[@id="__next"]/div/section[1]/div/nav/nav/div').click() #back to home page
    print("All files from 【"+courses[int(courseNo)-1][1]+" 】have been downloaded to your defaulted download directory")
    print(*courses,sep="\n")
    More=input("Any other module? If not, please enter -1 to exit")
    if int(More) in range(1,len(courses)):
        task.append(More)
        courseNo=More
    else:
        print("Thank you~ Happy Learning <3")
        courseNo=None
        break

