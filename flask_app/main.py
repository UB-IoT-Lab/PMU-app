from asyncio.subprocess import PIPE
import base64
import io
import json
import os
#from requests import request
import sqlite3 as sql
from datetime import datetime

#import seaborn as sns
import numpy as np
import pandas as pd
import requests
from dateutil import parser
from flask import (Flask, Response, flash, jsonify, redirect, render_template,
                   request)
import subprocess
import logging
logging.basicConfig(filename='logs/server.log', level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

#import numpy as np
#import seaborn as sns


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def root():
    if request.method == 'GET':

        if request.args:
            if request.args.get('pmu') == None:
                pmu = 1
            else:
                pmu = request.args.get('pmu')
            test = request.args.get('test')
        else:
            pmu = 1
            test = 1
        print(pmu, test)
        try:
            con = sql.connect("db/pmu_database")
            con.row_factory = sql.Row

            cur = con.cursor()
            if test == '':
                test = cur.execute(
                    "select DISTINCT ident from data2 WHERE pmu_ident=={} ".format(pmu)).fetchall()

                rows = cur.execute(
                    "select * from data2 where pmu_ident=={} and ident = {}".format(pmu, test[0]["ident"])).fetchall()
            else:
                rows = cur.execute(
                    "select * from data2 where pmu_ident=={} and ident = {}".format(pmu, test)).fetchall()
            idents = cur.execute(
                "select distinct ident from data2 where pmu_ident=={}".format(pmu)).fetchall()
            pmus = cur.execute(
                "select distinct pmu_ident from data2").fetchall()
            # print(len(res))
            # print(idents)
            #start = datetime(2022,4,13,18,16,00)
            #end = datetime(2022,4,13,18,20,20)
            # rows =[]
            # for i in range(len(res)):
            # if parser.parse((res[i]["time_stamp"]))>start and parser.parse((res[i]["time_stamp"]))<end:
            # if ((res[i]["ident"]))==1:
            #     rows.append(res[i])
            # print(idents)
            con.close()

            # print(len(rows))
            # print(stamp>present)
            return render_template("list.html", rows=rows, len=len, idents=idents, pmus=pmus)
        except:

            print("error in list operation")
            con.close()


@app.route("/graph", methods=['GET', 'POST'])
def graph():
    if request.method == 'GET':
        if request.args:
            if request.args.get('pmu') == None:
                pmu = 1
            else:
                pmu = request.args.get('pmu')
            test = request.args.get('test')
        else:
            pmu = 1
            test = 1
        #print(pmu, test)
        delay = []
        distdata = []
        arrivdata = []
        arriv_dist = []
        try:
            con = sql.connect("db/pmu_database")
            con.row_factory = sql.Row

            cur = con.cursor()
            if test == '':
                test = cur.execute(
                    "select DISTINCT ident from data2 WHERE pmu_ident=={} ".format(pmu)).fetchall()

                res = cur.execute(
                    "select * from data2 where pmu_ident=={} and ident = {}".format(pmu, test[0]["ident"])).fetchall()
            else:
                res = cur.execute(
                    "select * from data2 where pmu_ident=={} and ident = {}".format(pmu, test)).fetchall()
            idents = cur.execute(
                "select distinct ident from data2 where pmu_ident=={}".format(pmu)).fetchall()
            pmus = cur.execute(
                "select distinct pmu_ident from data2").fetchall()
            #start = datetime(2022,4,13,18,16,00)
            #end = datetime(2022,4,13,18,20,20)

            # for i in range(len(res)):
            #     #if parser.parse((res[i]["time_stamp"]))>start and parser.parse((res[i]["time_stamp"]))<end:
            #     delay.append(res[i]["diff"])
            #     r_m.append(res[i]["roll_mean"])
            for i in range(len(res)-1):
                eachData = {}
                eachData['delay'] = res[i]["diff"]
                eachData['pakno'] = i
                eachData['type'] = 1
                delay.append(eachData)
                # r_m.append([i,res[i]["roll_mean"]])
                eachData = {}
                eachData['delay'] = res[i]["roll_mean"]
                eachData['pakno'] = i
                eachData['type'] = 2
                delay.append(eachData)
                distdata.append(res[i]["diff"])
                if i in range(200, 250):
                    eachData = {}
                    eachData['ard'] = res[i]["arduino_sec"]
                    eachData['serv'] = res[i]["server_sec"]
                    arrivdata.append(eachData)

                if res[i+1]["server_sec"]-res[i]["server_sec"] > 0:
                    arriv_dist.append(
                        res[i+1]["server_sec"]-res[i]["server_sec"])
            con.close()
        except:
            print("error in sql operation")
            con.close()
        #plot = create_figure(delay,r_m)

        return render_template("graph.html", delay=delay, distdata=distdata, arrivdata=arrivdata, arriv_dist=arriv_dist, idents=idents, pmus=pmus)


@app.route("/livetest", methods=['GET', 'POST'])
def livetest():
    # devices = {}
    # devices[1] = 1673622
    # devices[2] = 1662974
    # devices[3] = 1783679
    # devices[4] = 1842496

    if request.method == 'POST':
        # status = request.form["status"]
        # message = request.form["message"]
        # print(status)
        # if(status == "start"):

        p1 = subprocess.Popen(
            ["python3", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # r1 = subprocess.run(["lsof", "-i", "UDP:7777"],
        #                     capture_output=True)
        #print(subprocess.check_output(['lsof', "-ti", "UDP:7777"]).decode())

        # print(r1)

        #  BELOW CODE IS FOR SENDING MESSAGE TO DEVICE VIA API
        # if request.form.get("pmu4"):
        #     status = request.form["status"]
        #     message = request.form["message"]

        #     dictToSend = {
        #         "deviceids": [devices[4]],
        #         "protocol": "TCP",
        #         "port": 4010,
        #         "data": '{{status:"{status}",message:"{message}"}}'.format(status=status, message=message)
        #     }
        #     print(dictToSend)
        #     headers = {'Authorization': 'Basic YXBpa2V5OjhvOGliT0ZrYVROaGZseXJuR3hva0RFUVdVNXJPeg==',
        #                'Content-Type': 'application/json'}
        #     res = requests.post('https://dashboard.hologram.io/api/1/devices/messages',
        #                         params={'deviceids': devices[4],
        #                                 'protocol': 'TCP', 'port': '4010'},
        #                         headers=headers,
        #                         data=json.dumps(dictToSend))
        #     print(res.url)
        #     print(res)

    return render_template("live_test.html")


@app.route("/livetestStop", methods=['GET', 'POST'])
def livetestStop():
    if request.method == 'POST':
        p2 = subprocess.run(
            ["bash", "kill.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(p2)
    return render_template("live_test.html")


@app.route("/issues", methods=['GET', 'POST'])
def issues():
    return render_template("issues.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
