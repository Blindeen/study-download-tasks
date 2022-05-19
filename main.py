import time
import requests
import wget

'''
This script allows you to download all done exercises from Dante1 or Dante2! You have to copy your hwsid and hwtoken 
from any https://dante.iis.p.lodz.pl subpages.
'''

'''
----------INSTRUCTION----------
Open your browser, then enter dante website and login. Open browser console and type "document.cookie", press enter
and replace hwsid and hwtoken values with yours. Set downloads path aswell.
'''

choice = input('Choose between Dante1 and Dante2 (type Dante1 or Dante2): ')
subject_id = ''
if choice == 'Dante1':
    subject_id = '25'
elif choice == 'Dante2':
    subject_id = '27'
else:
    print('Incorrect input')
    exit()

print('----------START----------')

try:
    cookies = {'hwsid': '', 'hwtoken': ''}
    save_path_src = ''

    rq = requests.get('https://dante.iis.p.lodz.pl/api/student/topicbrowser/getTopics?subjectid=' + subject_id, cookies=cookies)
    units = rq.json()
    units = units['Entries']

    for i in range(len(units)):
        print('------Unit%d------' % (i+1))
        time.sleep(5)
        task_number = 1

        unit = units[i]
        unit_number = unit['Number']

        tasks_url = 'https://dante.iis.p.lodz.pl/api/student/taskbrowser/getTasks?subjectid=25&topicid='+str(unit['TopicID'])
        rq = requests.get(tasks_url, cookies=cookies)
        tasks = rq.json()
        tasks = tasks['Entries']

        for j in range(len(tasks)):
            save_path = save_path_src
            task = tasks[j]
            machine_status = task['MachineStatus']

            if machine_status is not None:
                taskID = task['TaskID']
                req = requests.get('https://dante.iis.p.lodz.pl/api/student/reply/getReplyHistory?subjectid=25&taskid=' + str(taskID), cookies=cookies)

                replies = req.json()
                replies = replies['Entries']

                if (replies[0])['MachineMessage'] == 'Ok' or (replies[0])['MachineMessage'] == 'Ok.':
                    download_url = (replies[0])['MachineReport']
                    download_url = download_url.replace('index.html', 'source.zip', 1)

                    if int(unit_number) < 10:
                        save_path += '0' + unit_number + '.'
                    else:
                        save_path += unit_number + '.'

                    if task_number < 10:
                        save_path += '0' + str(task_number)
                    else:
                        save_path += str(task_number)

                    save_path += '.zip'
                    output_mess = save_path[-1:-10:-1]

                    print('\033[92m' + 'Success ' + output_mess[::-1] + '\033[0m')

                    time.sleep(1)
                    response = wget.download(download_url, save_path)

            task_number += 1

except requests.RequestException:
    print('\033[91m' + '\033[1m' + 'CONNECTION ERROR' + '\033[0m')
    print('If it\'s later than 10PM on weekdays or 9PM on weekends, remember to turn on VPN')

print('----------END----------')
