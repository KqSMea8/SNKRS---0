
'''
data['staticConfig']['client']
{'thirdPartyScriptMountingLocationId': 'thirdPartyScriptMountingPoint', 'servicePaths': {'api': 'https://api.nike.com', 'jCart': 'https://secure-store.nike.com', 'payment': 'https://paymentcc.nike.com', 'preview': 'https://frame.prod.commerce.nikecloud.com', 'agreement': 'https://agreementservice.svs.nike.com', 'email': 'https://www.nike.com', 'previewV2': 'https://api.nike.com', 'auth': 'https://adminops.prod.commerce.nikecloud.com', 'testApi': 'https://experience.test.commerce.nikecloud.com', 'testAuth': 'https://adminops.test.commerce.nikecloud.com'}, 'unite': {'avatarOrigin': 'https://www.nike.com/vc/profile', 'appId': 'nike-unite', 'backendEnvironment': 'identity', 'environment': 'production', 'uniteCdn': 'https://s3.nikecdn.com/unite/scripts/unite.min.js', 'api': 'https://api.nike.com', 'defaultview': 'appLanding'}, 'dreamsID': 'cloud', 'soasta': {'apiKey': 'R6SH7-84RFL-GQQ8S-CW6MF-W5RWR'}, 'newRelic': {}, 'cookiePolicyCountries': ['de', 'lu', 'at', 'be', 'gb', 'fi', 'ie', 'cz', 'dk', 'hu', 'nl', 'se', 'fr', 'it'], 'miscLinks': {'appStore': 'https://appsto.re/us/8cSt2.I', 'googlePlayStore': 'https://play.google.com/store/apps/details?id=com.nike.snkrs'}, 'applePayMerchantId': 'merchant.com.nike.payment', 'weChat': {'apiRoot': 'https://open.weixin.qq.com/connect/oauth2/authorize', 'appId': 'wx7232eec5a36b191a', 'responseType': 'code', 'scope': 'snsapi_base'}}

https://api.nike.com/launch

[*data]
['cookies', 'localize', 'externalScriptUnite', 'applePay', 'checkout', 'product', 'user', 'analytics', 'viewFeed', 'viewThread', 'router', 'staticConfig', 'device', 'preCart', 'externalScriptPaypal', 'forms', 'viewSettings', '@carts']

'''
header={'authority': 'www.nike.com',
        'method': 'GET',
        'path': '/cn/launch/',
        'scheme':'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'if-none-match': "10c4ad-qjGMF4hNZV26l6PqgcC5WGClgQw",
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}