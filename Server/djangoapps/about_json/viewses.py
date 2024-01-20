import json, calendar, datetime
from django.conf import settings
from django.http import HttpResponse
import os

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
def get_host_and_current_time(json_content):
    host = json_content.get("client", {}).get("host")
    current_time = json_content.get("server", {}).get("current_time")
    return host, current_time

def about_json(request):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_directory, 'about.json')

    with open(json_file_path) as json_file:
        json_content = json.load(json_file)
        json_content['client'] = get_client_ip(request)
        json_content['server']['current_time'] = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
        json_string = json.dumps(json_content, indent=4)
    return HttpResponse(json_string, content_type='application/json')