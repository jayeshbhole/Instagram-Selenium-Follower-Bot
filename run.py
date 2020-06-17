from selenium import webdriver
from time import sleep
import os
import protected
import time

log = open("log.txt",'a')

class InstaBot:
    count = 0
    
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
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
            global log
            sleep(5)
            while self.driver.find_elements_by_xpath("//button[contains(text(), 'Not Now')]") > 0:
                self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
                    .click()
                sleep(2)
        except:
            sleep(1)
        
        print("Bot alive! :)")
        str = time.asctime(time.localtime(time.time())) + '->  Login Successful ('+username+'):\n'
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
        str_ = "\n\tFetched " + str(len(usernames)) +'/' + str(fol) +" followers of "+self.username
        log.write(str_)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        
        
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
        
        str_ = "\n\tFetched " + str(len(usernames)) +'/' + str(fol) +" followers of "+self.username
        log.write(str_)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()

        
    def scroll_followers_list(self, followers):
        sleep(5)
        scroll_element  = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        length = 0
        while  length <= followers  :
            sleep(3)
            last_element  = (self.driver.find_elements_by_xpath("//div[@class='wo9IH']"))[-5]
            
            self.driver.execute_script("return arguments[0].scrollIntoView();", last_element)
            sleep(0.5)
            while  len(self.driver.find_elements_by_xpath("//div[@class='By4nA']"))>0:           
                sleep(2)
            
            sleep(2)
            length = len(scroll_element.find_elements_by_xpath("//div[@class='wo9IH']"))
        

    def follow_followers_of(self,username):
        self.driver.get('https://www.instagram.com/' + username + '/')
        sleep(5)
        
        no_f = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]").text    
        fol = no_f.replace(" followers", "")
        fol = fol.replace(",", "")
        print("followers: ",int(fol))
        sleep(1)
        
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        sleep(2)
        self.scroll_by_number(9)
        sleep(2)
        count = 0
        clearline = '\033[A                             \033[A'
        for i in range(int(fol)):
            if(self.count<100):
                try:          
                    button = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/ul/div/li["+str(i+1)+"]/div/div[2]/button")
                    
                    if(button.text == 'Follow'):
                        button.click()
                        count += 1
                        print(clearline)
                        print('followed : ',self.count)
                        sleep(2)
                    else:
                        print (clearline)
                        print("Skipped! ")
                        sleep(0.25)                
                except:
                    try:
                        button = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/ul/div/li["+str(i+2)+"]/div/div[2]/button")
                    
                        if(button.text == 'Follow'):
                            button.click()
                            count = count + 1
                            print(clearline)
                            print('followed : ',self.count)
                            sleep(2)
                        else:
                            print (clearline)
                            print("Skipped! ")
                            sleep(0.25)
                    except:
                        try:
                            self.driver.find_element_by_xpath("//button[contains(text(), 'Cancel')]")\
                                .click()
                            sleep(1)
                        except:
                            print("Error: Terminating!")
                            break
            else:
                print("process terminated. follow requests > 100")
                break   
        log.write("\tFollowed "+ str(count) +" followers of "+username+'\n' )
        self.count += count
    
    def follow_likers(self):
        usr = input('Enter target username: ')
        self.driver.get('https://www.instagram.com/' + usr + '/')     
        sleep(2)
        
        print('Open the post to scavenge likes. After the post is opened enter "scrap" to continue')
        
        _ = input('Continue? ')
        
        count = 0
        try:
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button')\
                .click()
        except:
            self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button')\
                .click()
        self.scroll_to_bottom()
        sleep(5)
        while count<150:   
            # try:
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
                        sleep(30)
                    if count>100:
                        sleep(30)
    
            sleep(1)

        log.write("\tFollowed "+ str(count) +" followers from "+usr+"'s post\n")
        self.count += count

    
    def __del__(self):
        try:
            self.driver.close()
        except:
            pass
        print("Bot is terminated! :(")
        print('Followed ',self.count,' Users')
        log.write("\n\tFollowed total "+str(self.count)+' users\n\n')

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
    
    log.close()
