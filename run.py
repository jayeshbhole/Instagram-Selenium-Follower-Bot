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
        sleep(2)

        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        
        try:
            global log
            sleep(5)
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
                .click()
            sleep(2)
        except:
            sleep(1)
        
        print("Bot alive! :)")
        str = time.asctime( time.localtime(time.time()) ) + '  Login Successful ('+username+'):\n'
        log.write(str)
    
    def _get_names(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/ul")
    
        self.scroll_to_bottom()
        sleep(2)

        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']

        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
        return names
    
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
                            self.count = self.count + 1
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


    def get_my_followers(self):
        list = open("myfollowers.txt","w+")
        sleep(2)
        self.driver.get('https://www.instagram.com/' + self.username + '/')
        sleep(4)
        no_f = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]").text
          
        fol = no_f.replace(" followers", "")
        print("followers: ",fol)
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        
        followers = self._get_names()

        list.writelines(["%s\n" % follower for follower in followers])
        list.close()
    
    def scroll_to_bottom(self):
        height = 0
        scroll_box  = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        ht = 1
        last_ht = 0
     
        while (last_ht < ht):
            sleep(1)
            last_ht = ht
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', scroll_box)
            sleep(1)
            
            ht = self.driver.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight);
                        return arguments[0].scrollHeight;
                        """, scroll_box)
            height = -ht
        self.driver.execute_script(str(height), scroll_box)

    def scroll_by_number(self,num):
        height = 0
        scroll_box  = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        ht = 1
        scroll = 0
        while scroll < num:
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', scroll_box)
            sleep(2)
            ht = self.driver.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight);
                        return arguments[0].scrollHeight;
                        """, scroll_box)
            height = -ht
            scroll += 1
        self.driver.execute_script(str(height), scroll_box)
    
    def follow_likers(self):
        usr = input('Enter target username: ')
        self.driver.get('https://www.instagram.com/' + usr + '/')
        sleep(2)
        
        print('Open the post to scavenge likes. After the post is opened enter "scrap" to continue')
        ip = input('Continue? ')
        
        count = 0
        try:
            self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button')\
                .click()
        except:
            self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button')\
                .click()
        
        sleep(5)
        while count<150:
            # try:
            sleep(2)
            buttons = self.driver.find_elements_by_css_selector(('button[type="button"]'))
            length = len(buttons)
            sleep(1)
            for button in buttons:
                if(button.text == 'Follow'):
                    sleep(1)
                    self.driver.execute_script("return arguments[0].scrollIntoView();", button)
                    self.driver.execute_script("arguments[0].click();", button)
                    # button.click()
                    count+=1
                    if count == 50:
                        sleep(30)
                    if count>100:
                        sleep(30)
    
            sleep(1)
            
        log.write("\tFollowed "+ str(count) +" followers from "+usr+"'s post\n")
        self.count += count

    
    def __del__(self):
        # try:
            # self.driver.close()
        # except:
        #     pass
        print("Bot is terminated! :(")
        print('Followed ',self.count,' Users')
        log.write("Followed total "+str(self.count)+' users\n\n')


def main():
    print("Fetching Username, Password and providing CPR to the Bot ")
    pw = protected.pw
    usr = protected.username
    mybot = InstaBot(usr , pw)
    sleep(0.5)

    print("\nEnter \n1 to get your followers \n2 to follow followers of @xyz \n3 To follow likers of some post \n\t OR \n 00 to terminate Bot")
    while True:
        ip = input("Choice: ")
     
        if(ip == '1'):
            sleep(2)
            mybot.get_my_followers()

        if(ip == '2'):
            user = input("Username of account to be scrapped: ")
            mybot.follow_followers_of(user)
        
        if(ip == '3'):
            sleep(1)
            mybot.follow_likers()

        if(ip == "00"):
            break
        else:
            print(" Wrong Choice. Sleeping 3 seconds!")
            sleep(3)
    print("Bot is terminating!!")
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('You terminated the operation.')
    
    log.close()
