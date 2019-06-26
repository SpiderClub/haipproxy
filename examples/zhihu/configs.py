# haipproxy client settings, which should be the same with
# settings for haipproxy server
LONGEST_RESPONSE_TIME = 10

LOWEST_SCORE = 6

LOWEST_TOTAL_PROXIES = 6

DATA_ALL = 'haipproxy:all'

TEMP_HTTP_QUEUE = 'haipproxy:http:temp'
TEMP_HTTPS_QUEUE = 'haipproxy:https:temp'
TEMP_ZHIHU_QUEUE = 'haipproxy:zhihu:temp'

VALIDATED_HTTP_QUEUE = 'haipproxy:validated:http'
VALIDATED_HTTPS_QUEUE = 'haipproxy:validated:https'
VALIDATED_ZHIHU_QUEUE = 'haipproxy:validated:zhihu'

TTL_VALIDATED_RESOURCE = 2  # minutes
TTL_HTTP_QUEUE = 'haipproxy:ttl:http'
TTL_HTTPS_QUEUE = 'haipproxy:ttl:https'
TTL_ZHIHU_QUEUE = 'haipproxy:ttl:zhihu'

SPEED_HTTP_QUEUE = 'haipproxy:speed:http'
SPEED_HTTPS_QUEUE = 'haipproxy:speed:https'
SPEED_ZHIHU_QUEUE = 'haipproxy:speed:zhihu'

SCORE_QUEUE_MAPS = {
    'http': VALIDATED_HTTP_QUEUE,
    'https': VALIDATED_HTTPS_QUEUE,
    'zhihu': VALIDATED_ZHIHU_QUEUE
}

TTL_QUEUE_MAPS = {
    'http': TTL_HTTP_QUEUE,
    'https': TTL_HTTPS_QUEUE,
    'zhihu': TTL_ZHIHU_QUEUE
}

SPEED_QUEUE_MAPS = {
    'http': SPEED_HTTP_QUEUE,
    'https': SPEED_HTTPS_QUEUE,
    'zhihu': SPEED_ZHIHU_QUEUE
}

# custom settings for your project
TOTAL_SUCCESS_REQUESTS = 'zhihu:success:request'
