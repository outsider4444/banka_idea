from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from notifications.models import Notifications


def get_notifications(request):
    notification_list = Notifications.objects.filter(user=request.user)

    for notification in notification_list:
        notification.status = True
        notification.save()

    context = {
        "notification_list":notification_list,
    }
    return render(request, "notifications/notifications_list.html", context)


def count_new_notifications(request):
    notification_list = Notifications.objects.filter(user=request.user).filter(status=False)
    new_notification = len(notification_list)
    data = {
        "msg": new_notification,
    }
    return JsonResponse(data)