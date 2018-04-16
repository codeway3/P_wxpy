# -*- coding：utf-8 -*-
import os
import time
import json
from wxpy import Bot, embed


LOG_FOLDER = './difflog/'
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)


def getdiff():
    # init
    group = bot.groups().search(u'九')[0]
    group.update_group(members_details=True)
    num = len(group)
    print('群组人数：', num)

    # get old & save new
    try:
        old_dict = json.load(open('record.json', 'r'))
    except:
        old_dict = {}
    fp = open('record.json', 'w')
    new_dict = {}
    for member in group:
        new_dict[member.puid] = member.name
    json.dump(new_dict, fp, ensure_ascii=False)
    fp.close()

    # diff & save result
    difflist_lost = []
    difflist_new = []
    for i in old_dict:
        if i not in new_dict and not old_dict[i] in new_dict.values():
            difflist_lost.append((i, old_dict[i]))
    for i in new_dict:
        if i not in old_dict and not new_dict[i] in old_dict.values():
            difflist_new.append((i, new_dict[i]))
    if difflist_lost != [] or difflist_new != []:
        print('-:', difflist_lost)
        print('+:', difflist_new)
        filename = LOG_FOLDER + time.strftime("%Y%m%d", time.localtime()) + '.json'
        fp = open(filename, 'w')
        json.dump((difflist_lost, difflist_new), fp, ensure_ascii=False)
        fp.close()
    else:
        print('No Change!')


bot = Bot(cache_path=True, console_qr=True)
bot.enable_puid('wxpy_puid.pkl')
getdiff()
embed()
