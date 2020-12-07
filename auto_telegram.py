import time
import telepot
from util.log import init
from db.telegram import TelegramDB
# from multiprocessing import Process
from telepot.loop import MessageLoop
from db.myredis import mset, mget, mdelete
from config import TelegramConf, LogDefine
from telepot.namedtuple import ReplyKeyboardMarkup, ForceReply


def handle_message(msg):
    try:
        from_chat_id, from_user, text, chat_type = msg['from']['id'], msg['from']['first_name'], msg.get('text', ''), msg['chat']['type']
        chat_id, chat_name = msg['chat']['id'], msg['chat']['first_name'] if chat_type == 'private' else msg['chat']['title']
        print(f'telegram机器人收到消息: [{chat_name}] =>> [{text}]', 0, 'telegram', LogDefine.telegram_log_file.format(time.strftime("%Y-%m-%d", time.localtime())))

        if TelegramConf.help in text:
            bot.sendMessage(chat_id, '/register 注册\n/channel_info 查询通道信息\n/plateform_info 查询平台信息\n/recharge 平台充值\n/mute 取消通知!')
        elif TelegramConf.register in text:
            with TelegramDB() as db:
                resp = db.add(chat_name, chat_id, chat_type)
            bot.sendMessage(chat_id, resp)
        elif TelegramConf.channel_info in text:
            with TelegramDB() as db:
                r = db.get_auth_by_chatid(chat_id, only_auth=True, need_all=False)
                if r and r[0] == 1:
                    bot.sendMessage(chat_id, db.get_channel_info())
                else:
                    bot.sendMessage(chat_id, '您无此权限, 请联系管理员添加权限!')
        elif TelegramConf.plateform_info in text:
            with TelegramDB() as db:
                r = db.get_auth_by_chatid(chat_id, only_auth=True, need_all=False)
                if r and r[0] == 1:
                    bot.sendMessage(chat_id, db.get_plateform_info())
                else:
                    bot.sendMessage(chat_id, '您无此权限, 请联系管理员添加权限!')
        elif TelegramConf.recharge in text:
            with TelegramDB() as db:
                r = db.get_auth_by_chatid(chat_id, only_auth=True, need_all=False)
                if r and r[0] == 1:
                    mset(TelegramConf.recharge_redis_key.format(from_chat_id, chat_id), 'start', 60)
                    with TelegramDB() as db:
                        mark_up = ReplyKeyboardMarkup(keyboard=db.get_plateform_info(need_handle_message=False), one_time_keyboard=True,)
                        bot.sendMessage(chat_id, text='请选择平台!', reply_markup=mark_up)
                else:
                    bot.sendMessage(chat_id, '您无此权限, 请联系管理员添加权限!')
        elif TelegramConf.mute in text:
            with TelegramDB() as db:
                db.mute_notice(chat_id)
            bot.sendMessage(chat_id, '已取消通知!')
        else:
            if msg.get('new_chat_title', None) is not None:
                with TelegramDB() as db:
                    db.update_chat(chat_id, chat_name)
            elif msg.get('reply_to_message', None) is not None:
                if msg['reply_to_message']['text'] == '请选择平台!':
                    mset(TelegramConf.recharge_redis_key.format(from_chat_id, chat_id), text, 60)
                    mark_up = ForceReply()
                    bot.sendMessage(chat_id, text='请输入充值金额!', reply_markup=mark_up)
                elif msg['reply_to_message']['text'] == '请输入充值金额!':
                    _ = mget(TelegramConf.recharge_redis_key.format(from_chat_id, chat_id))
                    if _:
                        with TelegramDB() as db:
                            balance_after, is_success = db.recharge_plateform(text, _)
                            if is_success:
                                mdelete(TelegramConf.recharge_redis_key.format(from_chat_id, chat_id))
                                bot.sendMessage(chat_id, f'充值成功, 充值后可用余额为{balance_after}')
        # print(f'telegram机器人处理完数据', 0, 'telegram', LogDefine.telegram_log_file.format(time.strftime("%Y-%m-%d", time.localtime())))
    except Exception as e:
        print(f'telegram机器人发送消息错误, 错误原因[{e}]', 2, 'telegram', LogDefine.telegram_log_file.format(time.strftime("%Y-%m-%d", time.localtime())))


if __name__ == '__main__':
    init()
    bot = telepot.Bot(TelegramConf.bot_token)
    # bot.message_loop(handle_message)
    # Process(target=bot.message_loop, kwargs={'callback': handle_message, 'run_forever': True}, name='telegram_server').start()
    MessageLoop(bot, handle_message).run_as_thread()
    # MessageLoop(bot, handle_message).run_forever()
    # Keep the program running.
    while True:
        try:
            print(f'telegram机器人活性检测{bot.getMe()}', 0, 'telegram', LogDefine.telegram_log_file.format(time.strftime("%Y-%m-%d", time.localtime())))
        except Exception as e:
            # bot = telepot.Bot(TelegramConf.bot_token)
            print(f'telegram机器人心跳失败, 失败原因[{e}]', 2, 'telegram', LogDefine.telegram_log_file.format(time.strftime("%Y-%m-%d", time.localtime())))
        with TelegramDB() as db:
            resp = db.show_nobalance_channel()
            notice_list = db.get_notice()
        if resp:
            for i in notice_list:
                try:
                    bot.sendMessage(int(i[0]), resp)
                    time.sleep(1)
                except Exception as e:
                    print(f'telegram机器人发送消息错误, 错误原因[{e}]', 2, 'telegram', LogDefine.telegram_log_file.format(time.strftime("%Y-%m-%d", time.localtime())))
            time.sleep(60 * 2)
        else:
            time.sleep(30)

