# from webpush import send_user_notification,send_group_notification

def is_user_doctor(user):
    return user.groups.filter(name='doctor').exists()
def is_user_patient(user):
    return user.groups.filter(name='patient').exists()

def sendnoti(user,data):
    pass
    # try:
    #     # user_id = id
    #     # user = get_object_or_404(User, pk=user_id)
    #     payload = {"head": data["head"], "body": data["body"], 
    #             "icon":"/static/images/favicon.ico", "url": data["url"]}
    #     send_user_notification(user=user, payload=payload, ttl=1000)
    # except Exception as e:
    #     print(e)
    #     return e