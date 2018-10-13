# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@author: bei
@file: main_server.py
@time: 18-5-8 下午3:29
'''

from __future__ import division
import numpy as np
import datetime,json,logging,requests,copy,multiprocessing,traceback,time,collections
from flask import Flask, render_template, Response
from flask_cors import CORS
from logging.handlers import TimedRotatingFileHandler
from gevent.pywsgi import WSGIServer
from gevent import monkey


# set logger
log_file_handler = TimedRotatingFileHandler(filename="/home/admin/UMC_bgy_jifen_deploy/log/main_server.log",
                                            when="D", interval=1, backupCount=10)
log_fmt = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
log.addHandler(log_file_handler)
log.info("####8888####")


def umc_main(mplist_status,mplist_shoppingcart):

    with open('class_file.json','r')as f:
        labels_dict = json.load(f)

    with open('labels.json','r')as f:
        labels_dic = json.load(f)

    with open('umc_config.json','r')as f :
        umc_config_dic = json.load(f)

    with open('layer_config.json','r')as f :
        layer_config_dic = json.load(f)

    with open('sensor_config_full.json','r')as f:
        sensor_config = json.load(f)
        ipcam_configdict_list = sensor_config['ipcam_config']

    def _init_status():
        status_len = len(ipcam_configdict_list)//umc_config_dic['ipcam_per_layer']
        # status_len = 1
        status_list = [{'id':'%d'%(i+1),
                        'status':'init',
                        'goods_list': [],
                        #'pred_stable':[],
                        #'pred_now':[],
                        'weight_stable':0,
                        'weight_pre':0,
                        'goods_num':0,
                        'weight_now':[]} for i in range(status_len)]
        return status_list


    def get_mean_predlist(pred_lists):
        x_list = ['_'.join(list(map(str, sorted(p)))) for p in pred_lists]
        tmp_dic = {}
        for x in x_list:
            try:
                tmp_dic[x] += 1
            except:
                tmp_dic[x] = 1
        tmp_list = tmp_dic.items()
        tmp_list = sorted(tmp_list, key=lambda x: x[1], reverse=True)
        # log.info tmp_list
        if tmp_list[0][0] == '':
            return []
        else:
            return list(map(int,list(map(float, tmp_list[0][0].split('_')))))



    status_list = _init_status()

    log.info("---====1111====---")
    while True:
        # try:
        #pred_list = json.loads(requests.get('http://0.0.0.0:8101/pred').text)['result']
        #pred_list = [list(np.concatenate(pred_list[umc_config_dic['ipcam_per_layer']*i:umc_config_dic['ipcam_per_layer']*(i+1)])) for i in range(len(pred_list)//umc_config_dic['ipcam_per_layer'])]
        #pred_list = [[int(ii) for ii in i ] for i in pred_list]
        weight_list = json.loads(requests.get('http://0.0.0.0:8101/weight').text)['result']
        weight_list = [np.sum(weight_list[umc_config_dic['weight_per_layer']*i:umc_config_dic['weight_per_layer']*(i+1)]) for i in range(len(weight_list)//umc_config_dic['weight_per_layer'])]

        log.info("====1111====")
        if status_list[0]['status'] == 'init':
            log.info("len(weight_list)==" + str(len(weight_list)))
            log.info("len(status_list)==" + str(len(status_list)))
            for idx in range(len(status_list)):
                # log.info status_list[idx]['pred_now']
                # log.info pred_list
                # log.info pred_list[idx]
                #status_list[idx]['pred_now'].append(pred_list[idx])
                status_list[idx]['weight_now'].append(weight_list[idx])
                if len(status_list[idx]['weight_now']) >= umc_config_dic['cache_len']:
                    status_list[idx]['status'] = 'init_done'
            time.sleep(0.5)
            log.info("====2222====")
            continue


        # log.info json.dumps(status_list)
        # log.info(json.dumps(mplist_shoppingcart[:]))


        # 读takein takeout
        takeout_list, takein_list = copy.deepcopy(mplist_shoppingcart[:])


        # loop to minimum object
        log.info("====3333====")
        for idx in range(len(status_list)):
            log.info("@@@@1111@@@@" + str((status_list[idx])))
            weight_mean_before = np.mean((status_list[idx]['weight_now']))
            log.info("@@@@2222@@@@")
            #status_list[idx]['pred_now'].append(pred_list[idx])
            status_list[idx]['weight_now'].append(weight_list[idx])
            log.info("@@@@3333@@@@")
            #del status_list[idx]['pred_now'][0]
            del status_list[idx]['weight_now'][0]


            log.info("@@@@4444@@@@")
            weight_var = np.var((status_list[idx]['weight_now']))

            log.info("@@@@5555@@@@")
            weight_mean = np.mean((status_list[idx]['weight_now']))
            log.info("@@@@6666@@@@=weight_mean=" + str(weight_mean))
            weight_var_percentage = abs(weight_var/(weight_mean+0.00001))
            log.info("@@@@7777@@@@")
            weight_var_value = abs(weight_mean-weight_mean_before)
            log.info("@@@@8888@@@@")
            #pred_mean = get_mean_predlist(status_list[idx]['pred_now'])

            if (weight_var_percentage >= umc_config_dic['weightchanging_percentage_threshold'] or weight_var_value >= umc_config_dic['weightchanging_value_threshold']) \
                and weight_mean > umc_config_dic['empty_dish_threshold']:
                status_list[idx]['status'] = 'weight_changing'
                log.info("====4444====")
                continue

            # weight_stable not empty
            elif weight_mean > umc_config_dic['empty_dish_threshold']:
                #pred_mean_weights = np.sum([labels_dict[str(i)]['weight'] for i in pred_mean])
                #weight_toletation_percentage = abs((weight_mean-layer_config_dic[str(1)])/(weight_mean+0.00001))
                weight_toletation_value = 10000-weight_mean

                #log.info("++++1111++++" + str(datetime.datetime.now()))
                log.info('[id:%d]pred_mean_weights: %.4f, weight_mean: %.4f'%(idx,layer_config_dic[str(1)],weight_mean))

                if weight_toletation_value >= umc_config_dic['weight_toleration_percentage_value']:
                #if weight_toletation_percentage <= umc_config_dic['weight_toleration_percentage_threshold'] or weight_toletation_value <= umc_config_dic['weight_toleration_percentage_value']:

                    log.info("++++2222++++" + str(datetime.datetime.now()))
                    num_now = round(weight_mean / layer_config_dic[str(1)])
                    num_before = round(status_list[idx]['weight_pre'] / layer_config_dic[str(1)])
                    status_list[idx]['status'] = 'stable_' + labels_dic[str(1)]
                    status_list[idx]['weight_stable'] = weight_mean
                    status_list[idx]['goods_num'] = num_now
                    status_list[idx]['goods_list'] = []
                    log.info("++++2222++++" + str(datetime.datetime.now()) + "    num_now=" + str(num_now) + "    num_before=" + str(num_before))
                    for i in range(int(num_now)):
                        status_list[idx]['goods_list'].append(1)

                    if num_now < num_before:
                        change_num = num_before - num_now

                        log.info("++++3333++++" + str(datetime.datetime.now()) + "    change_num=" + str(change_num))
                        for i in range(int(change_num)):
                            takeout_list.append(1)
                    elif num_now == num_before:
                        pass
                    elif num_now > num_before:
                        change_num = num_now - num_before
                        log.info("++++4444++++" + str(datetime.datetime.now()) + "    change_num=" + str(change_num))
                        for i in range(int(change_num)):
                            takein_list.append(1)

                    log.info("++++5555++++" + str(datetime.datetime.now()) + "    takeout_list=" + str(takeout_list)+ "    takein_list=" + str(takein_list))
                    tmp_takeout,tmp_takein = check_bill(takeout_list, takein_list)
                    if tmp_takeout != [] and tmp_takein != []:
                        log.info('tmp_takeout,tmp_takein: ',[labels_dict[str(i)]['name'] for i in tmp_takeout],[labels_dict[str(i)]['name'] for i in tmp_takein])


                    log.info("++++6666++++" + str(datetime.datetime.now()))
                    # takeout_list += tmp_takeout
                    takeout_list = tmp_takeout
                    # takein_list += tmp_takein
                    takein_list = tmp_takein

                    status_list[idx]['weight_pre'] = weight_mean
                    log.info("====5555====weight_mean=" + str(weight_mean))
                    log.info("====1111@@@@status_list[" + str(idx) + "]=" + str((status_list[idx])))
                    continue

                else:
                    status_list[idx]['status'] = 'error'
                    log.info("====6666====")
                    continue

            elif weight_mean < umc_config_dic['empty_dish_threshold']:
                if status_list[idx]['status'] == 'stable_emptydish':
                    #status_list[idx]['pred_stable'] = []
                    status_list[idx]['goods_list'] = []
                    status_list[idx]['weight_stable'] = 0
                    log.info("====7777====")
                    continue

                # elif status_list[idx]['status'] == 'stable' or status_list[idx]['status'] == 'weight_changing':
                else:

                    takeout_list += status_list[idx]['goods_list']

                    status_list[idx]['goods_list'] = []
                    #status_list[idx]['pred_stable'] = []
                    status_list[idx]['weight_stable'] = weight_mean
                    status_list[idx]['status'] = 'stable_emptydish'
                    log.info("====8888====")
                    continue

                # elif status_list[idx]['status'] == 'error':


        mplist_status[0] = status_list
        mplist_shoppingcart[0] = takeout_list
        mplist_shoppingcart[1] = takein_list


        # except Exception as e:
        #     logging.error('[umc_main]Unexpected Error.')
        #     tmp_traceback = traceback.format_exc()
        #     logging.error("[umc_main]Error Message. %s \n %s" % (str(e), tmp_traceback))
        log.info("====9999====")
        time.sleep(0.6)



def get_storage(status_list):
    storage_list = []
    for status in status_list:
        storage_list += status['goods_list']
    storage_list = [classes_dic[str(i)]['online_code'] for i in storage_list]

    return storage_list






# 结算购物车
def check_bill(takeout_goods_list,takein_goods_list):
    bill_list = []
    takein_list = copy.deepcopy(takein_goods_list)
    for takeout_goods in takeout_goods_list:
        try:
            takein_list.remove(takeout_goods)
        except:
            bill_list.append(takeout_goods)
    return bill_list,takein_list


#详见readme
def api():
    app = Flask(__name__)
    CORS(app)

    @app.route("/bill", methods=['GET'])
    def bill():
        try:

            takeout_list,takein_list = mplist_shoppingcart[:]

            takeout_list = [classes_dic[str(i)]['online_code'] for i in takeout_list]
            takein_list = [classes_dic[str(i)]['online_code'] for i in takein_list]

            # takeout_list = [classes_dic[str(i)]['name'] for i in takeout_list]
            # takein_list = [classes_dic[str(i)]['name'] for i in takein_list]

            bill_list,fillup_list = check_bill(takeout_list, takein_list)

            log.info('bill_list: ',bill_list)
            log.info('fillup_list: ',fillup_list)


            return json.dumps({'success': True,
                               'takeout_list':takeout_list,
                               'takein_list':takein_list,
                               'bill_list':bill_list,
                               'fillup_list':fillup_list,
                               'storage_list':get_storage(mplist_status[0])})
        except:
            return json.dumps({'success':False})


    @app.route("/bill_clear", methods=['GET'])
    def bill_clear():
        try:
            while True:
                for i in range(4):
                    mplist_shoppingcart[0] = []
                    mplist_shoppingcart[1] = []
                    time.sleep(0.1)

                if (mplist_shoppingcart[0] == []) and (mplist_shoppingcart[1] == []):
                    break
                else:
                    continue

            return json.dumps({'success':True})
        except:
            return json.dumps({'success':False})


    @app.route("/storage_list", methods=['GET'])
    def storage_list():
        # try:
        return json.dumps({'success': True,
                           'storage_list':get_storage(mplist_status[0])})
        # except:
        #     return json.dumps({'success':False})



    @app.route("/status_list", methods=['GET'])
    def status_list():
        # try:
        return json.dumps({'success': True,
                           'status_list': mplist_status[0]})
        # except:
        #     return json.dumps({'success':False})




    return app




def wsgi_api(app):
    log.info("[img_server]: Start gevent WSGI server")
    http = WSGIServer(('', 8201), app.wsgi_app)
    http.serve_forever()


# wsgi_api(api())


log.info("----1111----")
mp_manager = multiprocessing.Manager()
log.info("----2222----")
mp_dic = mp_manager.dict()
log.info("----3333----")
mplist_status = mp_manager.list()
log.info("----4444----")
mplist_status.append([])

log.info("----5555----")
mplist_shoppingcart = mp_manager.list()
log.info("----6666----")
mplist_shoppingcart.append([])
log.info("----7777----")
mplist_shoppingcart.append([])

log.info("----8888----")
with open('class_file.json','r')as f:
    classes_dic = json.load(f)

log.info("----9999----")
pool = multiprocessing.Pool(processes=3)
# umc_main(mplist_status,mplist_shoppingcart)
log.info("----0000----")
# pool.apply(umc_main(mplist_status,mplist_shoppingcart))
pool.apply_async(umc_main,(mplist_status,mplist_shoppingcart))
log.info("----00001111----")


wsgi_api(api())




