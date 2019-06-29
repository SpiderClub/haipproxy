# haipproxy client settings, which should be the same with
# settings for haipproxy server
LONGEST_RESPONSE_TIME = 10

LOWEST_SCORE = 6

LOWEST_TOTAL_PROXIES = 6

DATA_ALL = 'haipproxy:all'

TEMP_HTTP_Q = 'haipproxy:http:temp'
TEMP_HTTPS_Q = 'haipproxy:https:temp'
TEMP_ZHIHU_Q = 'haipproxy:zhihu:temp'

VALIDATED_HTTP_Q = 'haipproxy:validated:http'
VALIDATED_HTTPS_Q = 'haipproxy:validated:https'
VALIDATED_ZHIHU_Q = 'haipproxy:validated:zhihu'

TTL_VALIDATED_RESOURCE = 2  # minutes
TTL_HTTP_Q = 'haipproxy:ttl:http'
TTL_HTTPS_Q = 'haipproxy:ttl:https'
TTL_ZHIHU_Q = 'haipproxy:ttl:zhihu'

SPEED_HTTP_Q = 'haipproxy:speed:http'
SPEED_HTTPS_Q = 'haipproxy:speed:https'
SPEED_ZHIHU_Q = 'haipproxy:speed:zhihu'

SCORE_QUEUE_MAPS = {
    'http': VALIDATED_HTTP_Q,
    'https': VALIDATED_HTTPS_Q,
    'zhihu': VALIDATED_ZHIHU_Q
}

TTL_QUEUE_MAPS = {
    'http': TTL_HTTP_Q,
    'https': TTL_HTTPS_Q,
    'zhihu': TTL_ZHIHU_Q
}

SPEED_QUEUE_MAPS = {
    'http': SPEED_HTTP_Q,
    'https': SPEED_HTTPS_Q,
    'zhihu': SPEED_ZHIHU_Q
}

# custom settings for your project
TOTAL_SUCCESS_REQUESTS = 'zhihu:success:request'
