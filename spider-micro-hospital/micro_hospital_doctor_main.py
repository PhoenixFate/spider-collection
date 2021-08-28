import requests
import json
from pprint import pprint
from save_doctor import save_to_mongo


def save_json(json_result):
    # 将json数据保存在当前目录文件news.json 便于查看返回的数据类型
    with open("doctor.json", "w", encoding="utf-8") as f:
        # json.dumps 能够把python类型转成json字符串
        # unicode字符串转成中文
        # indent  缩进
        f.write(json.dumps(json_result, ensure_ascii=False, indent=4))


def get_doctor():
    session = requests.session()
    # 首页新闻数据
    doctor_url = "https://api-gateway.guahao.com/modulesearch/doctor/doctorsearch/list.json"
    headers = {
        "weiyi-appid": "p_h5_weiyi",
        "content-type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}

    request_data = {
        "area": "",
        "bar": 1,
        "cityName": "",
        "consult": 6,
        "doctorQualityLabel": None,
        "dynamicFilter": 1,
        "pageNo": 1,
        "pageSize": 20,
        "scene": 9,
        "sort": "general_consult_rank",
        "standardDepartment": "",
        "standardDepartmentName": "综合",
        "useIpArea": True
    }
    response = session.post(url=doctor_url, data=json.dumps(request_data, indent=4), headers=headers)
    print(response.status_code)
    # json.loads 把字符串转成python类型
    json_result = json.loads(response.content.decode("utf-8"))
    print("获得数据成功！")
    # pretty print
    pprint(json_result)
    # pprint(json_result["data"]["dataList"]["contentsList"])
    # 保存一份在本地文件
    save_json(json_result)
    # 保存新闻json对象到mongo
    save_to_mongo(json_result["items"])


if __name__ == '__main__':
    print("spider of micro hospital starts successfully")
    get_doctor()
