from django import template
from django.conf import settings
from urllib.parse import urlencode

register = template.Library()
@register.simple_tag
def get_login_qq_url():
	data = {
	    'response_type': 'code',
	    'client_id': settings.QQ_APP_ID,
	    'redirect_uri': settings.QQ_URL,
	    'state': 'zhyhdm',
	}
	return 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(data)
