from flask import Flask, request, jsonify, make_response
from config import const
import WanKeYunApi
from LogHelper import LogHelper
app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'code': '404', 'msg': 'api not found'}), 404)


@app.errorhandler(500)
def server_err(error):
    return make_response(jsonify({'code': '500', 'msg': 'system error,%s' % error.original_exception.args[0]}), 500)


def resp(data=None):
    return jsonify({'code': '0', 'msg': 'success', 'data': data})


logger = LogHelper('ZiMuZuHelper', cmdLevel='INFO', fileLevel="DEBUG").logger
onething = WanKeYunApi.WanKeYunApi(logger)
bok = onething.LoginEx(const.OTC_USERNAME, const.OTC_PASSWORD)
if bok == False:
    exit(0)
bok = onething.GetUSBInfo()
if bok is False:
    exit(0)
bok = onething.RemoteDlLogin()
if bok is False:
    exit(0)
bok = onething.GetRemoteDlInfo()
if bok is False:
    exit(0)


@app.route('/')
def index():
    aaa = open("index.html").read()
    return aaa


@app.route('/userInfo', methods=['GET'])
def get_user_info():
    return resp(client.get_user_info())


@app.route('/deviceInfo', methods=['GET'])
def get_device_info():
    return resp(client.get_device_info())


@app.route('/taskInfo', methods=['GET'])
def get_task_info():
    return resp(client.get_task_info())


@app.route('/taskList', methods=['GET'])
def get_task_list():
    aaa = onething.GetRemoteDlInfo()
    return onething.user_info
    # return resp(client.get_cloud_task_list())


# @app.route('/urlResolve', methods=['POST'])
# def url_resolve():
#     url = request.form.get('url')
#     check_args('url', url)
#     return resp(client.url_resolve(url))


@app.route('/taskCreate', methods=['POST'])
def create_task():
    url = getdata("url")
    urls = getdata("urls")
    # bok, mediaInfo = onething.UrlResolve(url)
    # taskInf = mediaInfo['taskInfo']
    # name = taskInf['name']
    # url = taskInf['url']
    # size = taskInf['size']
    JobList = []
    if urls != None:
        for i in urls:
            OneJob3 = {
                "filesize": 0,
                "url": url
            }
            JobList.append(OneJob3)
    else:
        OneJob3 = {
            "filesize": 0,
            "url": url
        }
        JobList.append(OneJob3)
    ret = onething.AddDownloadTasks(JobList)
    return onething.user_info


def getdata(name):
    data = request.data.decode('utf-8')
    import json
    aa = json.loads(data)
    return aa[name]


@app.route('/taskDel', methods=['POST'])
def del_task():
    task_id = getdata('id')
    onething.DelRemoteDl(task_id)
    return onething.user_info


@app.route('/taskStart', methods=['POST'])
def start_task():
    task_id = getdata('id')
    onething.StartRemoteDl(taskid=task_id)
    return onething.user_info


@app.route('/taskPause', methods=['POST'])
def pause_task():
    task_id = getdata('id')
    onething.PauseRemoteDl(taskid=task_id)
    return onething.user_info


def check_args(key, value):
    if value is None or '' == value:
        raise Exception('ERR:-1,MSG:%s could not be blank!' % key)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=const.GLOBAL_PORT, debug=False)
    # client.close()
