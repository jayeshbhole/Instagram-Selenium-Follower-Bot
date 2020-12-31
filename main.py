from time import sleep
import protected
import botCommands


def main():
    print("Fetching Username, Password ")
    pw = protected.pw
    usr = protected.username
    bot = botCommands.InstaBot(usr, pw)
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
            bot.get_followers_of()

        elif(ip == '2'):
            user = input("Username of account to be scrapped: ")
            bot.follow_followers_of(user)

        elif(ip == '3'):
            sleep(1)
            bot.follow_likers()

        elif(ip == '4'):
            sleep(1)
            user = input("Username of account to be scrapped: ")
            bot.get_followers_of(user)

        elif ip == '5':
            sleep(1)
            user = input("Username of account to be scrapped: ")
            bot.follow_users_followed_by(user)

        elif ip == '6':
            print("""\n\tQueue task by entering index of the task 
                        \t\t\t1 -to get your followers 
                        \t\t\t2 -to follow followers of @xyz 
                        \t\t\t3 -to get @username's followers
                        \t\t\t99 -to stop queuing""")
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
                    bot.get_my_followers()
                if task[0] == 2:
                    bot.follow_followers_of(task[1], task[2])
                elif task[0] == 3:
                    bot.get_followers_of(task[1])
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
