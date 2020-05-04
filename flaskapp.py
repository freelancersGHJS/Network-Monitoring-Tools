import json,csv,os,re
import random
import time
from datetime import datetime

from flask import Flask, Response, render_template,request

application = Flask(__name__)
random.seed()  # Initialize the random number generator


@application.route('/')
def index():
    return render_template('indexindex1.html')

@application.route('/chart-data',methods=['POST','GET'])
def chart_data():
    if request.method=="POST":
	 ####################################################################getting net address and second 
        net_address1 = request.form['net_address']
        web_ping = os.popen("ping " + net_address1).read()
        global val
        val=0
        val=request.form['secs']
        return render_template('indexindex1.html', data="yes", )
    sec = int(val)
    def generate_random_data(sec):
        plotfile = "plots.csv"
        ####################################################################clear csv
        imp = open(plotfile, 'r')
        out = open(plotfile, 'w')
        writer = csv.writer(out)
        for row in csv.reader(imp):
            writer.writerow(row)
        sec_iter =  sec
 #################################################################### each iteration sending plots to ui
        while True:
 ####################################################################first netstat ouput
            con = ""
            msg = os.popen("netstat -e").read()
            netstat = "".join(re.sub(r"[\n\t]*", "", msg))
            for i in range(0, len(netstat)):
                try:
                    if (int(netstat[i]) >= 0) and (int(netstat[i]) <= 9):
                        con += netstat[i]
                        if netstat[i + 1] == " ":
                            break
                except:
                    pass
            n1_sec = int(con)
 ####################################################################second netstat output
            con = ""
            msg = os.popen("netstat -e").read()
            netstat = "".join(re.sub(r"[\n\t]*", "", msg))
            for i in range(0, len(netstat)):
                try:
                    if (int(netstat[i]) >= 0) and (int(netstat[i]) <= 9):
                        con += netstat[i]
                        if netstat[i + 1] == " ":
                            break
                except:
                    pass
            n2_sec = int(con)
            con = ""
 ####################################################################calculating difference
            plot = abs(n1_sec - n2_sec) / 1024
 ####################################################################saving plots and second in csv
            rows = [[sec, plot]]
            plotfile = "plots.csv"
            #######append plot to csv
            with open(plotfile, 'a', newline="") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(rows)
            json_data = json.dumps(
                {'time': sec, 'value': plot})
            yield f"data:{json_data}\n\n"
            time.sleep(3)
 ####################################################################iterating second
            sec +=sec_iter
    return Response(generate_random_data(sec),mimetype="text/event-stream")

if __name__ == '__main__':
    application.run(debug=True, threaded=True)