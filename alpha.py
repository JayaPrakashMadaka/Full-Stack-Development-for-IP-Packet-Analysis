import psycopg2
import webbrowser
from flask import Flask, render_template, request, redirect, url_for
from jinja2 import Environment, FileSystemLoader
app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host = "10.17.50.87",
        database = "group_32",
        user = "group_32",
        password ="rM6I8Z7sw8lfsUdkp",
        port = "5432"
    )
    return conn

@app.route('/')
def index():
    return render_template("main_model.html")



@app.route('/main_model',methods=['POST','GET'])
def main():
    val=request.form.get('net')
    print(val)
    if(val=="1"):
        return list_Apps()
    if(val=="2"):
        return table_q2()
    if(val=="3"):
        return table_q3()
    if(val=="4"):
        return graph_avg_std()
    if(val=="5"):
        return graph_FIN()
    if(val=="6"):
        return table_q6()
    if(val=="7"):
        return graph_avg_std_iat()
    if(val=="8"):
        return time_apps()
    if(val=="9"):
        return graph_ActiveApps()
    if(val=="10"):
        return table_q10()
    if(val=="11"):
        return table_q11()
    if(val=="12"):
        return table_q12()
    if(val=="13"):
        return table_q13()
    if(val=="14"):
        return avg_idle_time_apps()
    if(val=="15"):
        return avg_pkt_15()
    if(val=="16"):
        return table_q16()
    if(val=="17"):
        return table_q17()
    # if(val=="18"):
    #     return count_18()
    if(val=="18"):
        return edit_18()
    if(val=="19"):
        return table_q19()
    if(val=="21"):
        return graph_21()

    if(val=="22"):
        return table_q22()
    # if(val=="23"):
    #     return pie_23()
    if(val=="23"):
        return edit_23()
    # if(val=="24"):
    #     return pie_24()
    if(val=="24"):
        return edit_24()
    # if(val=="25"):
    #     return table_q25()
    if(val=="25"):
        return edit_21()
    if(val=="26"):
        return pie_26()
    else:
        return render_template("main_model.html")
@app.route('/main_model',methods=['POST','GET'])
def edit_18():
    return render_template('edit_18.html')
@app.route('/main_model',methods=['POST','GET'])
def edit_21():
    return render_template('edit_21.html')
@app.route('/main_model',methods=['POST','GET'])
def edit_23():
    return render_template('edit_23.html')
@app.route('/main_model',methods=['POST','GET'])
def edit_24():
    return render_template('edit_24.html')

@app.route('/edit_21',methods=['POST','GET'])
def editnew_21():
    conn = get_db_connection()
    cur = conn.cursor()
    start=request.form.get('start')
    end=request.form.get('end')
    end2=request.form.get('end2')
    #graph's data of FIN getting from the data of 75 apps
    input_sql="""WITH RECURSIVE ReachableNodes AS (
                  SELECT DISTINCT destinationIp, timestamp
                  FROM FlowTable
                  WHERE sourceIp = {}
                  AND timestamp >= {}
                  AND timestamp <= {}

                  UNION

                  SELECT DISTINCT FlowTable.destinationIp, FlowTable.timestamp
                  FROM FlowTable
                  JOIN ReachableNodes ON ReachableNodes.destinationIp = FlowTable.sourceIp
                  AND ReachableNodes.timestamp = FlowTable.timestamp
                )
                SELECT timestamp, ARRAY_AGG(DISTINCT destinationIp) AS reachable_nodes
                FROM ReachableNodes
                GROUP BY timestamp
                ORDER BY timestamp;""" .format('$$'+start+'$$','$$'+end+'$$','$$'+end2+'$$')
    cur.execute(input_sql)
    table_q25 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    # bwd=[]
    # timestamp=[]
    for a in table_q25:
        print(a)
        protocalNames.append(str(a[0]))
        s=''
        for b in a[1]:
            s=s+'| '+str(b)+' '
        fwd.append(s[1:])
        # bwd.append(str(a[2]))
        # timestamp.append(str(a[2]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q25.html',protocalNames=protocalNames,fwd=fwd)

@app.route('/edit_18',methods=['POST','GET'])
def editnew_18():
    conn = get_db_connection()
    cur = conn.cursor()
    start=request.form.get('start')
    end=request.form.get('end')
    print("#########################################################")
    print(start)
    print(end)
    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName, SUM(FlowTable.flowDuration) AS count
                    FROM FlowTable
                    INNER JOIN ProtocolTable ON FlowTable.flowID = ProtocolTable.flowID
                    INNER JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                    WHERE timestamp >= {} AND timestamp < {}
                    GROUP BY ProtocolNameTable.ProtocolName
                    ORDER BY count DESC;
                    """.format('$$'+start+'$$','$$'+end+'$$')
    cur.execute(input_sql)
    time_data = cur.fetchall()
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        print(a)
        protocalNames.append(a[0])
        sum_time.append(float(a[1]))

    print(protocalNames)
    print(sum_time)
    # webbrowser.open_new_tab('login.html')
    return render_template('count_18.html',protocalNames=protocalNames,sum_time=sum_time)

@app.route('/edit_23',methods=['POST','GET'])
def editnew_23():
    conn = get_db_connection()
    cur = conn.cursor()
    app=request.form.get('start')
    #graph's data of FIN getting from the data of 75 apps
    input_sql="""
    SELECT
        date_trunc('day', (substring(FlowTable.timestamp from 1 for 19) || 'UTC')::timestamp AT TIME ZONE substring(FlowTable.timestamp from 21)) AS day,
        SUM(FlowTable.flowDuration) AS time_used
    FROM
        FlowTable
        JOIN ProtocolTable ON FlowTable.flowId = ProtocolTable.flowId
        JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
    WHERE
        ProtocolNameTable.ProtocolName = {}
        AND FlowTable.timestamp BETWEEN '2017-04-26 03:03:25+05:30' AND '2017-05-15 11:31:48+05:30'
    GROUP BY
        ProtocolNameTable.ProtocolName,
        date_trunc('day', (substring(FlowTable.timestamp from 1 for 19) || 'UTC')::timestamp AT TIME ZONE substring(FlowTable.timestamp from 21))
    ORDER BY
        day ASC;""".format('$$'+app+'$$')
    cur.execute(input_sql)
    time_data = cur.fetchall()
    name=[app]
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        print(a)
        protocalNames.append(str(a[0]))
        sum_time.append(int(a[1]))

    print(protocalNames)
    print(sum_time)
    # webbrowser.open_new_tab('login.html')
    return render_template('pie_23.html',name=name,protocalNames=protocalNames,sum_time=sum_time)
@app.route('/edit_24',methods=['POST','GET'])
def editnew_24():
    conn = get_db_connection()
    cur = conn.cursor()
    app=request.form.get('start')
    day=request.form.get('end')
    #graph's data of FIN getting from the data of 75 apps
    input_sql="""
    SELECT
        ProtocolNameTable.ProtocolName AS protocol_name,
        date_trunc('hour', to_timestamp(substring(FlowTable.timestamp, 1, 19), 'YYYY-MM-DD HH24:MI:SS')) AS hour,
        SUM(FlowTable.flowDuration) AS time_used
    FROM
        FlowTable
        JOIN ProtocolTable ON FlowTable.flowId = ProtocolTable.flowId
        JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
    WHERE
        ProtocolNameTable.ProtocolName = {}
        AND substring(FlowTable.timestamp, 1, 10) = {}
    GROUP BY
        ProtocolNameTable.ProtocolName,
        hour
    ORDER BY
        hour ASC;""".format('$$'+app+'$$','$$'+day+'$$')
    cur.execute(input_sql)
    time_data = cur.fetchall()
    name=[app]
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        print(a)
        protocalNames.append(str(a[1]))
        sum_time.append(int(a[2]))

    print(protocalNames)
    print(sum_time)
    # webbrowser.open_new_tab('login.html')
    return render_template('pie_24.html',name=name,protocalNames=protocalNames,sum_time=sum_time)

#1
@app.route('/main_model',methods=['POST','GET'])
def list_Apps():
    print("hats")
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolName
                FROM ProtocolNameTable
                ORDER BY ProtocolName"""
    cur.execute(input_sql)
    Names_data = cur.fetchall()
    protocalNames=[]
    # print(Names_data)
    for a in Names_data:
        protocalNames.append(a[0])


    return render_template('All_APPS.html',apps_list=protocalNames)

#2
@app.route('/main_model',methods=['POST','GET'])
def table_q2():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName, FlowTable.flowDuration , FlowTable.timestamp
                    FROM FlowTable,ProtocolTable,ProtocolNameTable
                    WHERE FlowTable.flowId =  ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                    ORDER BY flowDuration DESC
                    LIMIT 10;"""
    cur.execute(input_sql)
    table_q6 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    # bwd=[]
    timestamp=[]
    for a in table_q6:

        protocalNames.append(str(a[0]))
        fwd.append(int(a[1]))
        # bwd.append(str(a[2]))
        timestamp.append(str(a[2]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q2.html',protocalNames=protocalNames,fwd=fwd,timestamp=timestamp)
#3
@app.route('/main_model',methods=['POST','GET'])
def table_q3():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT protocol, COUNT(*) AS numFlows
                    FROM FlowTable
                    GROUP BY protocol"""
    cur.execute(input_sql)
    table_q6 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    # bwd=[]
    # timestamp=[]
    for a in table_q6:
        print(a)
        protocalNames.append(int(a[0]))
        fwd.append(int(a[1]))
        # bwd.append(str(a[2]))
        # timestamp.append(str(a[2]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q3.html',protocalNames=protocalNames,fwd=fwd)

#4
@app.route('/main_model',methods=['POST','GET'])
def graph_avg_std():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT protocol, AVG(totalLengthOfFwdPackets) AS avgFwdLength, STDDEV(totalLengthOfFwdPackets) AS stdFwdLength
                    FROM LengthTable
                    JOIN FlowTable ON LengthTable.flowId = FlowTable.flowId
                    GROUP BY protocol;"""
    cur.execute(input_sql)
    avgstd_data = cur.fetchall()
    protocolNames=[]
    avg=[]
    std=[]
    p1=[]
    p2=[]
    p3=[]
    for a in avgstd_data:
        print(a)
        protocolNames.append(int(a[0]))
        avg.append(float(a[1]))
        std.append(float(a[2]))
    p1.append(avg[2])
    p1.append(std[2])
    p2.append(avg[1])
    p2.append(std[1])
    p3.append(avg[0])
    p3.append(std[0])
    print(protocolNames)
    print(avg)
    print(std)
    # webbrowser.open_new_tab('login.html')
    return render_template('avg_std_graph.html',protocolNames=protocolNames,avg=avg,std=std,p1=p1,p2=p2,p3=p3)

#5
@app.route('/main_model',methods=['POST','GET'])
def graph_FIN():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName, SUM(FINFlagCount)
                FROM TCPFlagTable , ProtocolTable , ProtocolNameTable
                WHERE TCPFlagTable.flowId = ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                GROUP BY ProtocolNameTable.ProtocolName
                ORDER BY SUM(FINFlagCount) DESC
                LIMIT 20"""
    cur.execute(input_sql)
    FIN_data = cur.fetchall()
    protocalNames=[]
    sum_FIN=[]
    for a in FIN_data:
        print(a)
        protocalNames.append(a[0])
        sum_FIN.append(int(a[1]))

    print(protocalNames)
    print(sum_FIN)
    return render_template('FIN_graph.html',protocalNames=protocalNames,sum_FIN=sum_FIN)
#6
@app.route('/main_model',methods=['POST','GET'])
def table_q6():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName, SubflowTable.SubflowFwdPackets, SubflowTable.SubFlowBwdPackets , FlowTable.timestamp
                FROM SubflowTable,ProtocolTable,ProtocolNameTable,FlowTable
                WHERE SubflowTable.flowId = FlowTable.flowId AND FlowTable.flowId = ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol AND SubflowTable.SubflowFwdPackets + SubflowTable.SubFlowBwdPackets > 10000;
                """
    cur.execute(input_sql)
    table_q6 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    bwd=[]
    timestamp=[]
    for a in table_q6:
        print(a)
        protocalNames.append(a[0])
        fwd.append(int(a[1]))
        bwd.append(int(a[2]))
        timestamp.append(str(a[3]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q6.html',protocalNames=protocalNames,fwd=fwd,bwd=bwd,timestamp=timestamp)
#7
@app.route('/main_model',methods=['POST','GET'])
def graph_avg_std_iat():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT protocol, AVG(flowIATMean) AS avgIAT, STDDEV(flowIATMean) AS stdIAT
                    FROM IATTable
                    JOIN FlowTable ON IATTable.flowId = FlowTable.flowId
                    GROUP BY protocol;"""
    cur.execute(input_sql)
    avgstd_data = cur.fetchall()
    protocolNames=[]
    avg=[]
    std=[]
    p1=[]
    p2=[]
    p3=[]
    for a in avgstd_data:
        print(a)
        protocolNames.append(int(a[0]))
        avg.append(float(a[1]))
        std.append(float(a[2]))
    p1.append(avg[2])
    p1.append(std[2])
    p2.append(avg[1])
    p2.append(std[1])
    p3.append(avg[0])
    p3.append(std[0])
    print(protocolNames)
    print(avg)
    print(std)
    return render_template('avg_std_IAT_graph.html',protocolNames=protocolNames,avg=avg,std=std,p1=p1,p2=p2,p3=p3)
#8
@app.route('/main_model',methods=['POST','GET'])
def time_apps():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName , SUM(FlowTable.flowDuration) AS total_time_used
                    FROM FlowTable,ProtocolTable,ProtocolNameTable
                    WHERE FlowTable.flowId = ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                    GROUP BY ProtocolNameTable.ProtocolName
                    ORDER BY SUM(FlowTable.flowDuration) DESC LIMIT 10;"""
    cur.execute(input_sql)
    time_data = cur.fetchall()
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        print(a)
        protocalNames.append(a[0])
        sum_time.append(int(a[1]))

    print(protocalNames)
    print(sum_time)
    # webbrowser.open_new_tab('login.html')
    return render_template('time_apps.html',protocalNames=protocalNames,sum_time=sum_time)
#9
@app.route('/main_model',methods=['POST','GET'])
def graph_ActiveApps():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName, ActivityTable.ActiveMax
                    FROM ActivityTable,ProtocolTable,ProtocolNameTable
                    WHERE ActivityTable.flowid = ProtocolTable.flowid AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                    ORDER BY ActiveMax DESC
                    LIMIT 10"""
    cur.execute(input_sql)
    ActiveApps_data = cur.fetchall()
    AppsNames=[]
    Top_ActiveApps=[]
    for a in ActiveApps_data:
        print(a)
        AppsNames.append(a[0])
        Top_ActiveApps.append(int(a[1]))

    print(AppsNames)
    print(Top_ActiveApps)
    # webbrowser.open_new_tab('login.html')
    return render_template('ActiveApps_graph.html',protocalNames=AppsNames,sum_FIN=Top_ActiveApps)
#10
@app.route('/main_model',methods=['POST','GET'])
def table_q10():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT *  FROM FlowTable
                WHERE protocol NOT IN (6, 17)"""
    cur.execute(input_sql)
    table_q10 = cur.fetchall()

    # protocalNames=[]
    # fwd=[]
    # # bwd=[]
    # timestamp=[]

    table1=[]
    table2=[]
    table3=[]
    table4=[]
    table5=[]
    table6=[]
    table7=[]
    table8=[]


    for a in table_q10:

        table1.append(int(a[0]))
        table2.append(str(a[1]))
        table3.append(int(a[2]))
        table4.append(str(a[3]))
        table5.append(int(a[4]))
        table6.append(int(a[5]))
        table7.append(str(a[6]))
        table8.append(int(a[7]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q10.html',
        table1=table1,
        table2=table2,
        table3=table3,
        table4=table4,
        table5=table5,
        table6=table6,
        table7=table7,
        table8=table8
        )
#11
@app.route('/main_model',methods=['POST','GET'])
def table_q11():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT *
FROM FlowTable,ProtocolNameTable,ProtocolTable
WHERE FlowTable.flowId = ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol AND ProtocolName IN ('FTP', 'Telnet', 'SNMP')"""
    cur.execute(input_sql)
    table_q11 = cur.fetchall()

    # protocalNames=[]
    # fwd=[]
    # # bwd=[]
    # timestamp=[]

    flowid=[]
    sourceip=[]
    sourceport=[]
    destinationip=[]
    destinationport=[]
    protocol=[]
    timestamp=[]
    flowduration=[]
    l7protocol=[]
    protocolname=[]
    flowid2 =[]
    l7protocol2=[]


    for a in table_q11:
        # print(a)
        flowid.append(int(a[0]))
        sourceip.append(str(a[1]))
        sourceport.append(int(a[2]))
        destinationip.append(str(a[3]))
        destinationport.append(int(a[4]))
        protocol.append(int(a[5]) )
        timestamp.append(str(a[6]))
        flowduration.append(int(a[7]))
        l7protocol.append(int(a[8]))
        protocolname.append(str(a[9]) )
        flowid2 .append(int(a[10]))
        l7protocol2.append(int(a[11]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q11.html',flowid=flowid,
    sourceip=sourceip,
    sourceport=sourceport,
    destinationip=destinationip,
    destinationport=destinationport,
    protocol=protocol,
    timestamp=timestamp,
    flowduration=flowduration,
    l7protocol=l7protocol,
    protocolname=protocolname,
    flowid2 =flowid2,
    l7protocol2=l7protocol2)
#12
@app.route('/main_model',methods=['POST','GET'])
def table_q12():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT sourcePort, destinationPort, COUNT(*) AS numFlows FROM FlowTable
                GROUP BY sourcePort, destinationPort
                ORDER BY numFlows DESC
                LIMIT 10;"""
    cur.execute(input_sql)
    table_q12 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    # bwd=[]
    timestamp=[]
    for a in table_q12:
        print(a)
        protocalNames.append(int(a[0]))
        fwd.append(int(a[1]))
        # bwd.append(str(a[2]))
        timestamp.append(int(a[2]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q12.html',protocalNames=protocalNames,fwd=fwd,timestamp=timestamp)

#13
@app.route('/main_model',methods=['POST','GET'])
def table_q13():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT sourceIp, destinationIp, AVG(flowDuration) AS avgDuration FROM FlowTable
                    GROUP BY sourceIp, destinationIp
                    ORDER BY avgDuration DESC
                    LIMIT 10;"""
    cur.execute(input_sql)
    table_q13 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    # bwd=[]
    timestamp=[]
    for a in table_q13:
        # print(a)
        protocalNames.append(str(a[0]))
        fwd.append(str(a[1]))
        # bwd.append(str(a[2]))
        timestamp.append(float(a[2]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q13.html',protocalNames=protocalNames,fwd=fwd,timestamp=timestamp)

#14
@app.route('/main_model',methods=['POST','GET'])
def avg_idle_time_apps():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName , AVG(ActivityTable.IdleMean) AS avg_idle_time
                FROM ActivityTable,FlowTable,ProtocolNameTable,ProtocolTable
                WHERE FlowTable.flowDuration > 10 AND ActivityTable.flowId = FlowTable.flowID AND FlowTable.flowID = ProtocolTable.flowID AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                GROUP BY ProtocolNameTable.ProtocolName
                ORDER BY AVG(ActivityTable.IdleMean) DESC
                LIMIT 10;"""
    cur.execute(input_sql)
    time_data = cur.fetchall()
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        # print(a)
        protocalNames.append(a[0])
        sum_time.append(float(a[1]))


    # webbrowser.open_new_tab('login.html')
    return render_template('avg_idle_time_apps.html',protocalNames=protocalNames,sum_time=sum_time)

#15
@app.route('/main_model',methods=['POST','GET'])
def avg_pkt_15():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName, AVG(PacketSizeTable.averagePacketSize) AS avg_packet_length
                    FROM PacketSizeTable
                    JOIN ProtocolTable ON PacketSizeTable.flowId = ProtocolTable.flowID
                    JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                    GROUP BY ProtocolNameTable.ProtocolName;"""
    cur.execute(input_sql)
    time_data = cur.fetchall()
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        print(a)
        protocalNames.append(a[0])
        sum_time.append(float(a[1]))

    print(protocalNames)
    print(sum_time)
    return render_template('avg_pkt_15.html',protocalNames=protocalNames,sum_time=sum_time)

#16
@app.route('/main_model',methods=['POST','GET'])
def table_q16():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName, IATTable.flowIATMax, FlowTable.timestamp
                    FROM ProtocolNameTable
                    INNER JOIN ProtocolTable ON ProtocolNameTable.L7Protocol = ProtocolTable.L7Protocol
                    INNER JOIN FlowTable ON ProtocolTable.flowID = FlowTable.flowID
                    INNER JOIN IATTable ON FlowTable.flowID = IATTable.flowID
                    ORDER BY IATTable.flowIATMax DESC
                    LIMIT 10;"""
    cur.execute(input_sql)
    table_q16 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    # bwd=[]
    timestamp=[]
    for a in table_q16:
        print(a)
        protocalNames.append(str(a[0]))
        fwd.append(int(a[1]))
        # bwd.append(str(a[2]))
        timestamp.append(str(a[2]))

    # print(protocalNames)
    # print(sum_FIN)
    return render_template('table_q16.html',protocalNames=protocalNames,fwd=fwd,timestamp=timestamp)
#17
@app.route('/main_model',methods=['POST','GET'])
def table_q17():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName, FlowTable.TimeStamp, RatioTable.downUpRatio
                FROM FlowTable
                JOIN ProtocolTable ON FlowTable.flowId = ProtocolTable.flowId
                JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                JOIN RatioTable ON FlowTable.flowId = RatioTable.flowId
                WHERE RatioTable.downUpRatio > 200
                ORDER BY RatioTable.downUpRatio DESC;"""
    cur.execute(input_sql)
    table_q17 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    # bwd=[]
    timestamp=[]
    for a in table_q17:
        # print(a)
        protocalNames.append(str(a[0]))
        fwd.append(str(a[1]))
        # bwd.append(str(a[2]))
        timestamp.append(int(a[2]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q17.html',protocalNames=protocalNames,fwd=fwd,timestamp=timestamp)
#18
@app.route('/main_model',methods=['POST','GET'])
def count_18():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT ProtocolNameTable.ProtocolName, SUM(FlowTable.flowDuration) AS count
                    FROM FlowTable
                    INNER JOIN ProtocolTable ON FlowTable.flowID = ProtocolTable.flowID
                    INNER JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                    WHERE timestamp >= '2017-04-27 11:00:00' AND timestamp < '2017-04-27 12:00:00'
                    GROUP BY ProtocolNameTable.ProtocolName
                    ORDER BY count DESC;
                    """
    cur.execute(input_sql)
    time_data = cur.fetchall()
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        print(a)
        protocalNames.append(a[0])
        sum_time.append(float(a[1]))

    print(protocalNames)
    print(sum_time)
    # webbrowser.open_new_tab('login.html')
    return render_template('count_18.html',protocalNames=protocalNames,sum_time=sum_time)

#19
@app.route('/main_model',methods=['POST','GET'])
def table_q19():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT *
                FROM FlowTable
                ORDER BY flowDuration DESC
                LIMIT 10;"""
    cur.execute(input_sql)
    table_q19 = cur.fetchall()

    # protocalNames=[]
    # fwd=[]
    # # bwd=[]
    # timestamp=[]

    table1=[]
    table2=[]
    table3=[]
    table4=[]
    table5=[]
    table6=[]
    table7=[]
    table8=[]


    for a in table_q19:
        table1.append(int(a[0]))
        table2.append(str(a[1]))
        table3.append(int(a[2]))
        table4.append(str(a[3]))
        table5.append(int(a[4]))
        table6.append(int(a[5]))
        table7.append(str(a[6]))
        table8.append(int(a[7]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q19.html',
        table1=table1,
        table2=table2,
        table3=table3,
        table4=table4,
        table5=table5,
        table6=table6,
        table7=table7,
        table8=table8
        )

#21
@app.route('/main_model',methods=['POST','GET'])
def graph_21():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT
                  ProtocolNameTable.ProtocolName,
                  AVG(WindowTable.InitWinbytesforward + WindowTable.InitWinbytesbackward) AS AvgInitWinBytes
                FROM
                  ProtocolTable
                  INNER JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                  INNER JOIN WindowTable ON ProtocolTable.flowId = WindowTable.flowId
                GROUP BY
                  ProtocolNameTable.ProtocolName
                ORDER BY
                  AvgInitWinBytes DESC
                LIMIT 10;"""
    cur.execute(input_sql)
    FIN_data = cur.fetchall()
    protocalNames=[]
    sum_FIN=[]
    for a in FIN_data:
        print(a)
        protocalNames.append(str(a[0]))
        sum_FIN.append(float(a[1]))
    print(protocalNames)
    print(sum_FIN)



    return render_template('graph_21.html',protocalNames=protocalNames,sum_FIN=sum_FIN)

#22
@app.route('/main_model',methods=['POST','GET'])
def table_q22():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT
  ProtocolNameTable.ProtocolName,
  AVG(WindowTable.InitWinbytesforward + WindowTable.InitWinbytesbackward) AS AvgInitWinBytes
FROM
  ProtocolTable
  INNER JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
  INNER JOIN WindowTable ON ProtocolTable.flowId = WindowTable.flowId
GROUP BY
  ProtocolNameTable.ProtocolName
having AVG(WindowTable.InitWinbytesforward + WindowTable.InitWinbytesbackward) < 0;"""
    cur.execute(input_sql)
    table_q6 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    # bwd=[]
    # timestamp=[]
    for a in table_q6:
        print(a)
        protocalNames.append(str(a[0]))
        fwd.append(float(a[1]))
        # bwd.append(str(a[2]))
        # timestamp.append(str(a[2]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q22.html',protocalNames=protocalNames,fwd=fwd)

#23
@app.route('/main_model',methods=['POST','GET'])
def pie_23():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT
                  date_trunc('day', to_timestamp(FlowTable.timestamp, 'YYYY-MM-DD HH24:MI:SSOF')) AS day,
                  SUM(FlowTable.flowDuration) AS time_used
                FROM
                  FlowTable
                  JOIN ProtocolTable ON FlowTable.flowId = ProtocolTable.flowId
                  JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                WHERE
                  ProtocolNameTable.ProtocolName = 'FACEBOOK'
                  AND to_timestamp(FlowTable.timestamp, 'YYYY-MM-DD HH24:MI:SSOF') BETWEEN '2017-04-26 03:03:25+05:30' AND '2017-05-15 11:31:48+05:30'
                GROUP BY
                  ProtocolNameTable.ProtocolName,
                  date_trunc('day', to_timestamp(FlowTable.timestamp, 'YYYY-MM-DD HH24:MI:SSOF'))
                ORDER BY
                  day ASC;
                    """
    cur.execute(input_sql)
    time_data = cur.fetchall()
    name=["FACEBOOK"]
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        print(a)
        protocalNames.append(str(a[0]))
        sum_time.append(int(a[1]))

    print(protocalNames)
    print(sum_time)
    # webbrowser.open_new_tab('login.html')
    return render_template('pie_23.html',name=name,protocalNames=protocalNames,sum_time=sum_time)

#24
@app.route('/main_model',methods=['POST','GET'])
def pie_24():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT
                    ProtocolNameTable.ProtocolName AS protocol_name,
                    date_trunc('hour', to_timestamp(FlowTable.timestamp, 'YYYY-MM-DD HH24:MI:SSOF')) AS hour,
                    SUM(FlowTable.flowDuration) AS time_used
                  FROM
                    FlowTable
                    JOIN ProtocolTable ON FlowTable.flowId = ProtocolTable.flowId
                    JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
                  WHERE
                    ProtocolNameTable.ProtocolName = 'FACEBOOK'
                    AND to_timestamp(FlowTable.timestamp, 'YYYY-MM-DD HH24:MI:SSOF')::date = '2017-04-26'::date
                  GROUP BY
                    ProtocolNameTable.ProtocolName,
                    hour
                  ORDER BY
                    hour ASC;
                    """
    cur.execute(input_sql)
    time_data = cur.fetchall()
    name=["FACEBOOK"]
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        print(a)
        protocalNames.append(str(a[1]))
        sum_time.append(int(a[2]))

    print(protocalNames)
    print(sum_time)
    # webbrowser.open_new_tab('login.html')
    return render_template('pie_24.html',name=name,protocalNames=protocalNames,sum_time=sum_time)

#25
@app.route('/main_model',methods=['POST','GET'])
def table_q25():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""WITH RECURSIVE ReachableNodes AS (
                  SELECT DISTINCT destinationIp, timestamp
                  FROM FlowTable
                  WHERE sourceIp = '192.168.180.37'
                  AND timestamp = '2017-04-26 11:12:09+05:30'

                  UNION

                  SELECT DISTINCT FlowTable.destinationIp, FlowTable.timestamp
                  FROM FlowTable
                  JOIN ReachableNodes ON ReachableNodes.destinationIp = FlowTable.sourceIp
                  AND ReachableNodes.timestamp = FlowTable.timestamp
                )
                SELECT timestamp, ARRAY_AGG(DISTINCT destinationIp) AS reachable_nodes
                FROM ReachableNodes
                GROUP BY timestamp
                ORDER BY timestamp;"""
    cur.execute(input_sql)
    table_q25 = cur.fetchall()

    protocalNames=[]
    fwd=[]
    # bwd=[]
    # timestamp=[]
    for a in table_q25:
        print(a)
        protocalNames.append(str(a[0]))
        s=''
        for b in a[1]:
            s=s+'| '+str(b)+' '
        fwd.append(s[1:])
        # bwd.append(str(a[2]))
        # timestamp.append(str(a[2]))

    # print(protocalNames)
    # print(sum_FIN)
    # webbrowser.open_new_tab('login.html')
    return render_template('table_q25.html',protocalNames=protocalNames,fwd=fwd)

#26
@app.route('/main_model',methods=['POST','GET'])
def pie_26():
    conn = get_db_connection()
    cur = conn.cursor()

    #graph's data of FIN getting from the data of 75 apps
    input_sql="""SELECT
  sourceIp,
  SUM(fwdIATTotal + BwdIATTotal) AS totalTraffic
            FROM
              FlowTable
              JOIN IATTable ON FlowTable.flowId = IATTable.flowId
            WHERE
              timestamp = '2017-04-26 11:12:09+05:30'
            GROUP BY
              sourceIp
            ORDER BY
              totalTraffic DESC
            LIMIT
              10;"""
    cur.execute(input_sql)
    time_data = cur.fetchall()
    protocalNames=[]
    sum_time=[]
    for a in time_data:
        print(a)
        protocalNames.append(str(a[0]))
        sum_time.append(int(a[1]))

    print(protocalNames)
    print(sum_time)
    # webbrowser.open_new_tab('login.html')
    return render_template('pie_26.html',protocalNames=protocalNames,sum_time=sum_time)
# list_Apps()


# if __name__ == '__main__':
#     # Render the HTML and write it to a file
#     html = table_q25()
#     with open('output_25.html', 'w') as f:
#         f.write(html)
#     webbrowser.open_new_tab('output_25.html')






if __name__ == '__main__':
    app.run(debug=True)
# graph_FIN()



# if __name__ == '__main__':
#     # Render the HTML and write it to a file
#     html = graph_FIN()
#     with open('output.html', 'w') as f:
#         f.write(html)


# webbrowser.open_new_tab('login.html')
