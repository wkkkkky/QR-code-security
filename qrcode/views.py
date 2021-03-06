from django.shortcuts import HttpResponse
from django.views import View
from django.conf import settings
from predict import detect_img
from urllib.parse import urlparse
from qrcode.models import *
from yolo import YOLO

import urllib.request
import json

yolo = YOLO()


# 获取域名地址
def get_url(url):
    res = urlparse(url)
    scheme = res.scheme
    netloc = res.netloc
    res_url = scheme + "://" + netloc + "/"
    return res_url


# 调用腾讯域名检测接口
# 返回参数：
# type	int	0	检测类型，0拦截，1-3通过
# result	string	已被拦截	检测结果
# explain	string	该网站含有未经证实的信息	检测说明
# organization	string	北京微播视界科技有限公司	ICP主体信息
# icpnumber	string	京ICP备16016397号-3	网站ICP备案编号
# url	string	https://douyin.com	域名或链接
def api_detect(url):
    APIKEY = 'bb910578d9412fed4cc8a0bef946b64a'
    path = 'http://api.tianapi.com/txapi/qqurlcheck/index?key=' + APIKEY + '&url=' + url

    resp = urllib.request.urlopen(path)
    content = resp.read().decode("utf-8")
    if content:
        result = json.loads(content)
        # 连接正常，返回type
        if result['code'] == 200:
            type_code = result['newslist'][0]['type']
            print(type_code)
            return type_code
        else:
            print("连接检测接口失败！错误码： " + str(result['code']))
            return 4


# 将识别结果保存到数据库中
def save_url(code, url):
    if code == 1:
        # 安全网址
        level = Level.objects.get(id=1)
    elif code == 2:
        # 危险网址
        level = Level.objects.get(id=2)
    else:
        # 未知网址
        level = Level.objects.get(id=3)
    black = Black(black_host=url, black_level=level)
    black.save()
    pass


class test(View):
    def get(self, request):
        return HttpResponse('GET方法')

    def post(self, request):
        # 获取传递的url信息
        all_url = request.POST.get("url")
        url = get_url(all_url)

        # 使用接口检测
        type_code = api_detect(url)
        if type_code == 0:
            print("Result：危险网站")
            return HttpResponse("危险")
        if type_code == 3:
            print("Result：安全网站")
            return HttpResponse("安全")

        # 使用黑名单检测
        black_result = Black.objects.filter(black_host=url)
        if black_result:
            # 检测到黑名单中有数据就直接返回安全等级
            result = str(black_result[0].black_level)
            print("Result: ", result)
            return HttpResponse(result)

        # 获取上传的图片并将其存储
        image = request.FILES.get("file")
        if not image:
            return HttpResponse("图片上传失败")
        save_path = '%s/templates/images/%s' % (settings.BASE_DIR, image.name)
        with open(save_path, 'wb') as f:
            for content in image.chunks():
                f.write(content)
        path = './templates/images/' + image.name

        # 加载模型，进行logo识别
        result = detect_img(yolo, path)

        if result:
            # 识别成功，将识别结果进行验证
            max_id = None
            max_score = 0
            for i in result:
                if i[1] > max_score:
                    max_id = i[0]
                    max_score = i[1]
            query = Logo.objects.filter(logo_id=max_id)
            if query:
                print(query[0].logo_host)
                if query[0].logo_host == url:
                    # 验证成功，有相应数据
                    print("Result: 安全")
                    code = 1
                    save_url(code, url)
                    return HttpResponse("安全")
                else:
                    # 验证失败，没有相应数据
                    print("Result: 危险")
                    code = 2
                    save_url(code, url)
                    return HttpResponse("危险")
            else:
                print("Result: error")
                return HttpResponse("error")
        else:
            # 识别失败，返回未知
            print("Result: 未知")
            code = 3
            save_url(code, url)
            return HttpResponse("未知")
