from selenium import webdriver
from time import sleep
import os
import protected
import time

log = open("log.txt",'a')

class InstaBot:
    task = 0
    count = 0
    
    def __init__(self, username, pw):
        global log
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        log.write("__Session start__\n\t")
        # self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(5)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        
        try:
            sleep(5)
            while self.driver.find_elements_by_xpath("//button[contains(text(), 'Not Now')]") > 0:
                self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
                    .click()
                sleep(3)
        except:
            sleep(1)
        
        print("Bot alive! :)")
        str = time.asctime(time.localtime(time.time())) + '->  Login Successful ('+username+'):'
        log.write(str)

    def get_my_followers(self):
        file = self.username + "_followers_"
        list_ = open(file,"w+")
        sleep(2)
        
        self.driver.get('https://www.instagram.com/' + self.username + '/')
        sleep(4)
        no_f = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]").text
        fol = no_f.replace(" followers", "")
        print("followers: ",fol)
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
            
        self.scroll_followers_list(int(fol))
        scroll_box = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        links = scroll_box.find_elements_by_tag_name('a')
        usernames = [name.text for name in links if name.text != '']
               
        list_.writelines(["%s\n" % follower for follower in usernames])
        list_.close()
        str_ = "\n\tTask: "+str(self.task)+" Fetched " + str(len(usernames)) +'/' + str(fol) +" followers of "+self.username
        log.write(str_)
        print("Done extracting")

             
    def get_followers_of(self):
        
        username = input("Username of target: ")
        file = self.username + "_followers_"
        list_ = open(file,"w+")
        sleep(2)
        self.driver.get('https://www.instagram.com/' + username + '/')
        sleep(4)
        
        no_f = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]").text
        fol = no_f.replace(" followers", "")
        print("followers: ",fol)
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
            
        self.scroll_followers_list(int(fol))
        scroll_box = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        links = scroll_box.find_elements_by_tag_name('a')
        usernames = [name.text for name in links if name.text != '']
        list_.writelines(["%s\n" % follower for follower in usernames])
        list_.close()
        
        str_ = "\n\tTask: "+str(self.task)+" Fetched " + str(len(usernames)) +'/' + str(fol) +" followers of "+ username
        log.write(str_)
        print("Done extracting")

        
    def scroll_followers_list(self, followers):
        print("Scrolling the list. Dont close the window")
        sleep(5)
        scroll_element  = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        length = 0
        sleep(3)
        self.driver.execute_script("return arguments[0].scrollIntoView();", scroll_element)
        
        while  length < followers-1  :
            
            sleep(3)
            elements = scroll_element.find_elements_by_tag_name('button')[-10:]
            for element in elements:
                try:
                    self.driver.execute_script("return arguments[0].scrollIntoView();", element)
                    sleep(0.25)
                except:
                    continue

            while  len(scroll_element.find_elements_by_xpath("//div[@class='By4nA']"))>0:
                print("sleeping")
                sleep(1)
            
            sleep(1)
            length = len(scroll_element.find_elements_by_tag_name('button'))
        print('scroll complete')
    
    def focus_and_click(self,element):
        self.driver.execute_script("return arguments[0].scrollIntoView();", element)
        self.driver.execute_script("arguments[0].click();", element)
            
    def follow_followers_of(self,username):
        
        self.driver.get('https://www.instagram.com/' + username + '/')
        sleep(5)
        
        no_f = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]").text
        fol = no_f.replace(" followers", "")
        fol = int(fol.replace(",", ""))
        print("followers: ",fol)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        sleep(2)

        count = 0
        target = int(input("Enter max people to follow: "))
        
        self.scroll_followers_list(min(target*10,fol))
        
        print("\nNow following the users~~~~~~~~\n")
        scroll_element  = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        buttons = scroll_element.find_elements_by_tag_name('button')
        for button in buttons:
            try:
                self.driver.execute_script("return arguments[0].scrollIntoView();", button)
            except:
                pass
            if button.text == 'Follow':
                sleep(2)
                try:
                    self.focus_and_click(button)
                    count += 1
                    print("Followed: ",count,end = '\r')
                except:
                    continue
                if count >= target :
                    print('Target met')
                    break
                if count == 50:
                    sleep(20)
                if count==100:
                    sleep(30)
            while button.text == 'follow':
                sleep(2)
                self.focus_and_click(button)
        self.task +=1
        log.write("\n\tTask :"+str(self.task)+" Followed "+ str(count) +" followers of "+username)
        self.count += count
    
    def follow_likers(self):
        usr = input('Enter target username: ')
        self.driver.get('https://www.instagram.com/' + usr + '/')
        sleep(2)
        
        print('Open the post to scavenge likes. After the post is opened enter "scrap" to continue')
        
        _ = input('Continue? ')
        
        count = 0
        
        div = self.driver.find_element_by_xpath("//div[@class ='Nm9Fw']")
        bttn = div.find_element_by_xpath("//button[contains(text(), 'others')]")
        bttn.click()
        sleep(5)
        
        target = int(input("Enter max people to follow: "))
        while count<target:
            sleep(2)
            buttons = self.driver.find_elements_by_css_selector(('button[type="button"]'))
            sleep(1)
            for button in buttons:
                if(button.text == 'Follow'):
                    sleep(1)
                    self.driver.execute_script("return arguments[0].scrollIntoView();", button)
                    self.driver.execute_script("arguments[0].click();", button)
                    
                    count+=1
                    if count == 50:
                        sleep(20)
                    elif count==100:
                        sleep(30)
    
            sleep(1)
        task +=1
        log.write("\n\t Task: "+str(self.task)+" Followed "+ str(count) +" followers from "+usr+"'s post")
        self.count += count
        
    
    def __del__(self):
        print("Bot is terminated! :(")
        print('Followed ',self.count,' Users')
        log.write("\n\tFollowed total "+str(self.count)+' users and performed '+str(self.task)+' tasks \n__Session_End__ \n\n')

def main():
    print("Fetching Username, Password ")
    pw = protected.pw
    usr = protected.username
    mybot = InstaBot(usr , pw)
    sleep(0.5)
    print("\nEnter \n1 to get your followers \n2 to follow followers of @xyz \n3 To follow likers of some post \n4 to get @username's followers\n\t OR \n 00 to terminate Bot")
    while True:
        ip = input("Choice: ")
        if(ip == '1'):
            sleep(2)
            mybot.get_my_followers()

        elif(ip == '2'):
            user = input("Username of account to be scrapped: ")
            mybot.follow_followers_of(user)
        
        elif(ip == '3'):
            sleep(1)
            mybot.follow_likers()

        elif(ip == '4'):
            sleep(1)
            mybot.get_followers_of()

        elif(ip == "00"):
            break
        
        else:
            print(" Wrong Choice. Sleeping 3 seconds!")
            sleep(3)
            continue
        
        print("Task finished!")
    print("Bot terminating!!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('You terminated the operation.')
    
    log.close()m
