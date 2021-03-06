# # 调用腾讯域名检测接口
# # 返回参数：
# # type	int	0	检测类型，0拦截，1-3通过
# # result	string	已被拦截	检测结果
# # explain	string	该网站含有未经证实的信息	检测说明
# # organization	string	北京微播视界科技有限公司	ICP主体信息
# # icpnumber	string	京ICP备16016397号-3	网站ICP备案编号
# # url	string	https://douyin.com	域名或链接
#
# import urllib.request
# import json
#
# APIKEY = 'bb910578d9412fed4cc8a0bef946b64a'
# url = 'https://www.baidu.com'
# path = 'http://api.tianapi.com/txapi/qqurlcheck/index?key=' + APIKEY + '&url=' + url
#
# resp = urllib.request.urlopen(path)
# content = resp.read().decode("utf-8")
#
# if content:
#     result = json.loads(content)
#     # 连接正常，返回type
#     if result['code'] == 200:
#         type_code = result['newslist'][0]['type']
#         print(type_code)
#         return type_code
#     else:
#         print("连接检测接口失败！错误码： " + result['code'])
