PUBLIC_KEY = "Marvel Public Key"
PRIVATE_KEY = "Marvel Private Key"

# Set to true when on school wifi, set False when at home
PROXY_NEEDED = False

PROXY_USER = 'ProxyUser'
PROXY_PASS = 'ProxyPass'

# END OF USER REQUIRED CONFIG
PROXY_URL = 'http://'+PROXY_USER+':'+PROXY_PASS+'@proxy2.eq.edu.au:80'
PROXY_CONFIG = {'https': PROXY_URL,
                'http': PROXY_URL}
