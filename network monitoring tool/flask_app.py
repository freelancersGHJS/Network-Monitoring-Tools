import json,os, re,csv
from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/')
def call_index():
   return render_template("index1.html",name = "connection not established")

@app.route('/index', methods= ['POST'])
def index_netstat():
    net_address1 = request.form['net_address']
    sec = int(request.form['secs'])
    sec_iter = sec
    ##################################################run ping with given user net address
    web_ping = os.popen("ping " + net_address1).read()
    ping = "".join(re.sub(r"[\n\t]*", "", web_ping))
    concat = ""
    plotfile = "plots.csv"
    ####################################################################clear csv
    imp = open(plotfile, 'r')
    out = open(plotfile, 'w')
    writer = csv.writer(out)
    for row in csv.reader(imp):
        writer.writerow(row)
    ##################################################finding average and connection established or not
    for i in range(len(ping) - 1, 0, -1):
        try:
            if ping[i] == "," or ping[i] == ".":
                concat = "connection not established"
                return render_template("index1.html", name=concat)

                break
            if (int(ping[i]) >= 0) and (int(ping[i]) <= 9):
                concat += ping[i]
                if ping[i - 1] == " ":
                    break
        except:
            pass
    concat = concat[::-1]
    plotfile = "plots.csv"
    ##################################################clear csv
    imp = open(plotfile, 'r')
    out = open(plotfile, 'w')
    writer = csv.writer(out)
    for row in csv.reader(imp):
        writer.writerow(row)
    #####################################################save ping result in csv
    with open(plotfile, 'a',newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(concat[::-1])
    #######################################################real time chart
    plotx_list = []
    ploty_list = []
    iteration = 0
    #######################################################real time chart generation
    while (iteration<30):
        iteration +=1
        con = ""
        #######################################################getting data flow rate
        for j in range(sec - sec_iter + 1, sec + 1):
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
            if (j == sec):
                n1_sec = int(con)
                break
            con = ""
        con = ""
        n3_sec = (sec + sec_iter)
        #######################################################getting data flow rate
        for j in range(sec + 1, sec + sec_iter + 1):
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
            if (j == n3_sec):
                n2_sec = int(con)
                break
            con = ""
        #######################################################calculating difference
        plot = abs(n1_sec - n2_sec) / 1024
        plotx_list.append(sec)
        ploty_list.append(plot)
        rows = [[sec,plot]]
        sec += sec_iter
        plotfile = "plots.csv"
        ######################################################append difference between the netstat of the plot to csv
        with open(plotfile, 'a',newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(rows)
    return render_template("index1.html", name=concat[::-1], plot_x=json.dumps(plotx_list), plot_y=json.dumps(ploty_list))

@app.route('/grl')
def saved_data():
    plotfile = "plots.csv"
    con = ""
    #######################################################ploting saved real time chart
    with open(plotfile, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        for i in your_list[0]:
            con += i
        plotx_list = []
        ploty_list = []
        for i in range(1, len(your_list)):
            plotx_list.append(int(your_list[i][0]))
            ploty_list.append(float(your_list[i][1]))
    return render_template("index2.html",name = con,plot_x=json.dumps(plotx_list), plot_y=json.dumps(ploty_list))

if __name__ == '__main__':
   app.run(debug = True)
