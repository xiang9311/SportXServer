import jpush as jpush
AK = 'bf99a2c43d8865abe4875bb6'
SK = '594a8bba8661d9a037daafd1'

def pushToUser(userId,userName):
    userId_str = str(userId)
    _jpush = jpush.JPush(AK, SK)
    _jpush.set_logging("DEBUG")
    push = _jpush.create_push()
    push.audience = jpush.audience(
                jpush.alias(userId_str)
            )
    push.notification = jpush.notification(alert="新消息")
    push.smsmessage=jpush.smsmessage(userName+"评论了你的动态",0)
    push.platform = jpush.all_
    print (push.payload)
    push.send()