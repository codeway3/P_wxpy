import json
import time
from wxpy import *


def getdiff():
    # init
    group = bot.groups().search(u'九')[0]
    group.update_group(members_details=True)
    num = len(group)
    print('群组人数：', num)

    # get old & save new
    try:
        old_list = json.load(open('record.json', 'r'))
    except:
        old_list = {}
    fp = open('record.json', 'w')
    new_list = {}
    for member in group:
        new_list[member.puid] = member.name
    json.dump(new_list, fp, ensure_ascii=False)
    fp.close()

    # diff & save result
    difflist_lost = []
    difflist_new = []
    for i in old_list:
        if i not in new_list:
            difflist_lost.append((i, old_list[i]))
    for i in new_list:
        if i not in old_list:
            difflist_new.append((i, new_list[i]))
    if difflist_lost != [] or difflist_new != []:
        print('-:', difflist_lost)
        print('+:', difflist_new)
        filename = 'difflog_' + time.strftime("%Y%m%d", time.localtime()) + '.json'
        fp = open(filename, 'w')
        json.dump((difflist_lost, difflist_new), fp)
        fp.close()
    else:
        print('No Change!')


bot = Bot(cache_path=True, console_qr=True)
bot.enable_puid('wxpy_puid.pkl')
getdiff()
embed()
