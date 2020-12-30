from selenium import webdriver
from time import sleep
import os
import protected
import time


class InstaBot:
    task = 0
    count = 0

    def __init__(self, username, pw):
        log = open("log.txt", 'a')
        log.write("__Session start__\n\t")
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
            print('sleeping', end='\r')
            sleep(5)
            while self.driver.find_elements_by_xpath("//button[contains(text(), 'Not Now')]") > 0:
                self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
                    .click()
                sleep(3)
        except:
            sleep(1)

        print("Bot alive! :)")
        str = time.asctime(time.localtime(time.time())) + \
            '->  Login Successful ('+username+'):'
        log.write(str)
        log.close()

    def get_my_followers(self):
        log = open("log.txt", 'a')

        file = self.username + "_followers_"
        list_ = open(file, "w+")
        sleep(2)

        self.driver.get('https://www.instagram.com/' + self.username + '/')
        sleep(4)
        no_f = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]").text
        fol = no_f.replace(" followers", "")
        print("followers: ", fol)
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()

        self.scroll_followers_list(int(fol))
        scroll_box = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        links = scroll_box.find_elements_by_tag_name('a')
        usernames = [name.text for name in links if name.text != '']

        list_.writelines(["%s\n" % follower for follower in usernames])
        list_.close()
        str_ = "\n\tTask "+str(self.task)+": Fetched " + str(len(usernames)) + \
            '/' + str(fol) + " followers of "+self.username
        log.write(str_)
        print("Done extracting")
        log.close()

    def get_followers_of(self, username):
        log = open("log.txt", 'a')
        file = username + "_followers_"
        list_ = open(file, "w+")
        sleep(2)
        self.driver.get('https://www.instagram.com/' + username + '/')
        sleep(4)

        no_f = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]").text
        fol = no_f.replace(" followers", "")
        print("followers: ", fol)
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()

        self.scroll_followers_list(int(fol))
        scroll_box = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        links = scroll_box.find_elements_by_tag_name('a')
        usernames = [name.text for name in links if name.text != '']
        list_.writelines(["%s\n" % follower for follower in usernames])
        list_.close()

        str_ = "\n\tTask "+str(self.task)+": Fetched " + str(len(usernames)) + '/' + str(fol) + " followers of " + username
        log.write(str_)
        print("Done extracting")
        log.close()

    def scroll_followers_list(self, followers):
        print("Scrolling the list upto:", followers,
              "users. Dont close the window")
        sleep(5)
        scroll_element = self.driver.find_element_by_xpath(
            "//div[@class='isgrP']")
        length = 0
        sleep(3)
        self.driver.execute_script(
            "return arguments[0].scrollIntoView();", scroll_element)

        while length < followers-1:

            sleep(3)
            elements = scroll_element.find_elements_by_tag_name('button')[-10:]
            for element in elements:
                try:
                    self.driver.execute_script(
                        "return arguments[0].scrollIntoView();", element)
                    sleep(0.15)
                except:
                    continue

            while len(scroll_element.find_elements_by_xpath("//div[@class='By4nA']")) > 0:
                print("sleeping")
                sleep(1)

            sleep(1)
            length = len(scroll_element.find_elements_by_tag_name('button'))
        print('scroll complete')

    def focus_and_click(self, element):
        self.driver.execute_script(
            "return arguments[0].scrollIntoView();", element)
        self.driver.execute_script("arguments[0].click();", element)

    def follow_followers_of(self, username, target=0):
        log = open("log.txt", 'a')
        self.task += 1
        self.driver.get('https://www.instagram.com/' + username + '/')
        sleep(5)

        no_f = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]").text
        fol = no_f.replace(" followers", "")
        fol = int(fol.replace(",", ""))
        print("followers: ", fol)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        sleep(2)
        count = 0
        if target == 0:
            target = int(input("Enter max people to follow: "))

        log.write("\n\tTask "+str(self.task)+": Following " +
                  str(target) + " followers of "+username)
        print("\nNow following the users~~~~~~~~\n")
        batch = 1
        while count < target:
            batch_size = min((target-count), 100)
            self.scroll_followers_list(batch_size)
            print("Batch", batch, "of size", batch_size)
            count += self.follow_button_click(batch_size)
            string = '\n\t\tFollowed ' + \
                str(count)+' users till batch '+str(batch)
            print(string)
            log.write(string)
            batch += 1

        log.write("\n\tTask "+str(self.task)+": Followed " +
                  str(count) + " followers of "+username)
        self.count += count
        log.close()

    def follow_users_followed_by(self, username, target=0):
        log = open("log.txt", 'a')
        self.task += 1
        log.write("\n\tTask "+str(self.task) +
                  ": Following users followed by "+username)
        self.driver.get('https://www.instagram.com/' + username + '/')
        sleep(5)

        no_f = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]").text
        fol = no_f.replace(" followers", "")
        fol = int(fol.replace(",", ""))
        print("followers: ", fol)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        sleep(2)
        count = 0
        if target == 0:
            target = int(input("Enter max people to follow: "))

        print("\nNow following the users~~~~~~~~\n")
        batch = 1
        while count < target:
            batch_size = min((target-count), 100)
            self.scroll_followers_list(batch_size)
            print("Batch", batch, "of size", batch_size)
            count += self.follow_button_click(batch_size, 'following')
            string = '\n\t\tFollowed ' + \
                str(count)+' users in batch '+str(batch)
            print(string)
            log.write(string)
            batch += 1

        log.write("\n\tTask "+str(self.task)+": Followed " +
                  str(count) + " users followed by "+username)
        self.count += count
        log.close()

    def follow_button_click(self, target, type_='followers', scroll_element="//div[@class='isgrP']"):
        count = 0
        scroll_element = self.driver.find_element_by_xpath(scroll_element)
        buttons = scroll_element.find_elements_by_tag_name('button')
        for button in buttons:
            try:
                self.driver.execute_script(
                    "return arguments[0].scrollIntoView();", button)
                if button.text == 'Follow':
                    self.focus_and_click(button)
                    count += 1
                    print("Followed: ", count, end='\r')

                    if count >= target:
                        print('Target met.\n')
                        break
                    elif count == 25:
                        sleep(10)
                    elif count == 50:
                        sleep(20)
                    elif count == 100:
                        sleep(30)
                    sleep(6)
                tries = 0
                while tries < 20:
                    if button.text == 'Follow':
                        sleep(6)
                        if button.text == 'Follow':
                            self.focus_and_click(button)
                            tries += 1
                    elif button.text == 'Following' or button.text == 'Requested':
                        break
                    sleep(1)
                    try:
                        if scroll_element.find_element_by_tag_name('button').text == 'Unfollow':
                            scroll_element.find_element_by_tag_name(
                                'button').click()
                            break
                    except:
                        pass
                    if tries == 20:
                        sleep(60)
            except:
                pass
        return count

    def follow_likers(self):
        log = open("log.txt", 'a')
        username = input('Enter target username: ')
        self.driver.get('https://www.instagram.com/' + username + '/')
        sleep(2)

        print('Open the post to scavenge likes. After the post is opened enter "scrap" to continue')

        _ = input('Continue? ')

        count = 0

        div = self.driver.find_element_by_xpath("//div[@class ='Nm9Fw']")
        bttn = div.find_element_by_xpath(
            "//button[contains(text(), 'others')]")
        bttn.click()
        sleep(5)
        batch = 0

        target = int(input("Enter max people to follow: "))
        log.write("\n\tTask "+str(self.task)+": Following " +
                  str(target) + " likers of a post by "+username)

        while count < target:
            batch_size = min((target-count), 100)
            count = self.follow_button_click(batch_size, 'following', 'likers')
            buttons = self.driver.find_elements_by_tag_name('button')
            for button in buttons:
                try:
                    self.driver.execute_script(
                        "return arguments[0].scrollIntoView();", button)
                    if button.text == 'Follow':
                        self.focus_and_click(button)
                        count += 1
                        print("Followed: ", count, end='\r')

                        if count >= target:
                            print('Target met.')
                            break
                        if count == 50:
                            sleep(20)
                        elif count == 100:
                            sleep(30)
                        sleep(3)
                except:
                    pass

            string = '\n\t\tFollowed ' + \
                str(count)+' users in batch '+str(batch)
            print(string)
            log.write(string)
            batch += 1
            sleep(1)

        self.task += 1
        log.write("\n\t Task "+str(self.task)+": Followed " +
                  str(count) + " followers from "+username+"'s post")
        self.count += count
        log.close()

    def __del__(self):
        log = open("log.txt", 'a')
        print("Bot is terminated! :(")
        print('Followed ', self.count, ' Users')
        log.write("\n\n\tFollowed total "+str(self.count) +
                  ' users and performed '+str(self.task)+' tasks \n__Session_End__ \n\n')
        log.close()


def main():
    print("Fetching Username, Password ")
    pw = protected.pw
    usr = protected.username
    mybot = InstaBot(usr, pw)
    sleep(0.5)

    print("""\n\tEnter 
          \t1 to get your followers 
          \t2 to follow followers of @xyz 
          \t3 To follow likers of some post 
          \t4 to get @username's followers
          \t5 to follow users followed by @xyz
          \t6 to queue tasks
          \t\t OR 
          \t 00 to terminate Bot""")

    while True:
        ip = input("\tChoice: ")
        if(ip == '1'):
            mybot.get_my_followers()

        elif(ip == '2'):
            user = input("Username of account to be scrapped: ")
            mybot.follow_followers_of(user)

        elif(ip == '3'):
            sleep(1)
            mybot.follow_likers()

        elif(ip == '4'):
            sleep(1)
            user = input("Username of account to be scrapped: ")
            mybot.get_followers_of(user)

        elif ip == '5':
            sleep(1)
            user = input("Username of account to be scrapped: ")
            mybot.follow_users_followed_by(user)

        elif ip == '6':
            print("\n\tQueue task by entering index of the task \n\t\t\t1 -to get your followers \n\t\t\t2 -to follow followers of @xyz \n\t\t\t3 -to get @username's followers\n\t\t\t99 -to stop queuing")
            queue = []
            while True:
                choice = input('\t\t\tEnter task: ')
                if choice == '99' or choice == 99:
                    break
                if(choice == '1'):
                    queue.append((1, 0))

                elif(choice == '2'):
                    user = input("Username of account to be scrapped: ")
                    target = input("Enter max people to follow: ")
                    queue.append((2, user, target))

                elif(choice == '3'):
                    user = input("Username of account to be scrapped: ")
                    queue.append((3, user))

            for task in queue:
                if task[0] == 1:
                    mybot.get_my_followers()
                if task[0] == 2:
                    mybot.follow_followers_of(task[1], task[2])
                elif task[0] == 3:
                    mybot.get_followers_of(task[1])
            print('Queue completed successfully')

        elif ip == '00':
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
        print('You terminated the operation Manually')
