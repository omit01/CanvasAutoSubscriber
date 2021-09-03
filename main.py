import requests
import sched, time

s = sched.scheduler(time.time, time.sleep)

api_url = "https://tilburguniversity.instructure.com/api/v1/"
token = "<YOUR TOKEN>"
headers = {'Authorization': 'Bearer ' + token}

bot_token = "<YOUR TELEGRAM BOT TOKEN>"
bot_chatID = "<YOUR CHAT ID>"

subedGroups = []
courseIDME = 8934
courseIDLA = 8961
courseIDIA = 8953
num = 1

# Function to Sub to a group based on id
def subtogroup(id):
    responsetosub = requests.post(api_url + 'groups/' + str(id) + '/memberships', headers=headers, params={'user_id': 'self'})
    if responsetosub.status_code == 200:
        print('subbed to:')
        print(id)
        telegram_bot_sendnewsignup(id)
    else:
        print('Error subbing to:' + str(id))

# Function to check groups signed up to
def checksubedgroups():
    global subedGroups
    subedGroups = []
    responsesubbed = requests.get(api_url + 'users/self/groups', headers=headers)
    print('Now subed to:')
    for group in responsesubbed.json():
        subedGroups.append(group['id'])
        print(group['id'])

#Function to inform user on group signup based on id
def telegram_bot_sendnewsignup(id):
    groupInfo = requests.get(api_url + 'groups/' + str(id), headers=headers).json()
    courseInfo = requests.get(api_url + 'courses/' + str(groupInfo['course_id']), headers=headers).json()
    bot_message = 'Signed up to: ' + courseInfo['name'] + '\n' + groupInfo['name']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

#Looping maintask
def maintask(sc):
    print('')
    global num
    print("LOOP " + str(num))

    checksubedgroups()

    # Macro-Economie
    print('STARTING MACRO ECONOMIE')
    # Get al groups from Macro Economics
    response = requests.get(api_url + 'courses/' + str(courseIDME) + '/groups', headers=headers)
    #For each group, check if not subscribed and if not full, then subscribe
    for groupME in response.json():
        if groupME['id'] in subedGroups:
            continue
        elif groupME['max_membership'] == groupME['members_count']:
            print(str(groupME['id']) + ' is full, checking again in 10 seconds!')
            continue
        else:
            subtogroup(groupME['id'])

    # Lineare algebra
    print('')
    print('STARTING LINEARE ALGEBRA')
    response = requests.get(api_url + 'courses/' + str(courseIDLA) + '/groups', headers=headers)
    #For LA also check if couse is EN and if it's second lesson in the week (as I only want to attend that one)
    for groupLA in response.json():
        if groupLA['id'] in subedGroups:
            continue
        if not 'EN' in groupLA['name']:
            continue
        elif not '.2' in groupLA['name']:
            continue
        elif groupLA['max_membership'] == groupLA['members_count']:
            print(str(groupLA['id']) + ' is full, checking again in 10 seconds!')
            continue
        else:
            subtogroup(groupLA['id'])

    num += 1
    #Repeat every 10 seconds
    s.enter(10, 1, maintask, (sc,))

#Start
s.enter(0, 1, maintask, (s,))
s.run()
