import os
import random
from scrapy.conf import settings
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        print "Generating Random Choice"
        ua  = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')
