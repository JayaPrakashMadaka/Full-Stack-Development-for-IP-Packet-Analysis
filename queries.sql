-- 1. Find all apps for which data is available

SELECT ProtocolName
FROM ProtocolNameTable
ORDER BY ProtocolName;

-- 2. Find apps using longest flows in flowDuration at a given timestamp.

SELECT ProtocolNameTable.ProtocolName, FlowTable.flowDuration , FlowTable.timestamp
FROM FlowTable,ProtocolTable,ProtocolNameTable
WHERE FlowTable.flowId =  ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
ORDER BY flowDuration DESC
LIMIT 10;

-- 3. Count number of flows for each protocol

SELECT protocol, COUNT(*) AS numFlows
FROM FlowTable
GROUP BY protocol;

--- 4. Calculate the average and standard deviation of the total length of forward packets for each protocol:

SELECT protocol, AVG(totalLengthOfFwdPackets) AS avgFwdLength, STDDEV(totalLengthOfFwdPackets) AS stdFwdLength
FROM LengthTable
JOIN FlowTable ON LengthTable.flowId = FlowTable.flowId
GROUP BY protocol;


--- 5. Identify top 20 apps with a high number of FIN flags:

SELECT ProtocolNameTable.ProtocolName, SUM(FINFlagCount)
FROM TCPFlagTable , ProtocolTable , ProtocolNameTable
WHERE TCPFlagTable.flowId = ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
GROUP BY ProtocolNameTable.ProtocolName
ORDER BY SUM(FINFlagCount) DESC
LIMIT 20;


--- 6. Apps having flows with a high number of subflows at a given timestamp.

SELECT ProtocolNameTable.ProtocolName, SubflowTable.SubflowFwdPackets, SubflowTable.SubFlowBwdPackets , FlowTable.timestamp
FROM SubflowTable,ProtocolTable,ProtocolNameTable,FlowTable
WHERE SubflowTable.flowId = FlowTable.flowId AND FlowTable.flowId = ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol AND SubflowTable.SubflowFwdPackets + SubflowTable.SubFlowBwdPackets > 10000;

--- 7. Calculate the average and standard deviation of the flow inter-arrival time for each protocol

SELECT protocol, AVG(flowIATMean) AS avgIAT, STDDEV(flowIATMean) AS stdIAT
FROM IATTable
JOIN FlowTable ON IATTable.flowId = FlowTable.flowId
GROUP BY protocol;


--8 Time used by apps

SELECT ProtocolNameTable.ProtocolName , SUM(FlowTable.flowDuration) AS total_time_used
FROM FlowTable,ProtocolTable,ProtocolNameTable
WHERE FlowTable.flowId = ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
GROUP BY ProtocolNameTable.ProtocolName
ORDER BY SUM(FlowTable.flowDuration) DESC LIMIT 10;


-- 9. Find the top 10 most active Apps in terms of maximum active time
SELECT ProtocolNameTable.ProtocolName, ActivityTable.ActiveMax
FROM ActivityTable,ProtocolTable,ProtocolNameTable
WHERE ActivityTable.flowid = ProtocolTable.flowid AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
ORDER BY ActiveMax DESC
LIMIT 10;

--10 Potential Threats for Non UDP,TCP Protocols

SELECT *  FROM FlowTable
WHERE protocol NOT IN (6, 17);


--11 Potential Threats which are FTP , Telnet , SNMP

SELECT *
FROM FlowTable,ProtocolNameTable,ProtocolTable
WHERE FlowTable.flowId = ProtocolTable.flowId AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol AND ProtocolName IN ('FTP', 'Telnet', 'SNMP');

--12 To optimize resource allocation, we could analyze network usage and identify areas where resources can be reallocated to improve performance and reduce costs.

SELECT sourcePort, destinationPort, COUNT(*) AS numFlows FROM FlowTable
GROUP BY sourcePort, destinationPort
ORDER BY numFlows DESC
LIMIT 10;

--13 query to find the source/destination pairs that have the longest average flow duration (network optimization)

SELECT sourceIp, destinationIp, AVG(flowDuration) AS avgDuration FROM FlowTable
GROUP BY sourceIp, destinationIp
ORDER BY avgDuration DESC
LIMIT 10;

--14 A lower average idle time could indicate a more active network flow, while a higher average idle time could suggest a less active or stalled flow.

SELECT ProtocolNameTable.ProtocolName , AVG(ActivityTable.IdleMean) AS avg_idle_time
FROM ActivityTable,FlowTable,ProtocolNameTable,ProtocolTable
WHERE FlowTable.flowDuration > 10 AND ActivityTable.flowId = FlowTable.flowID AND FlowTable.flowID = ProtocolTable.flowID AND ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
GROUP BY ProtocolNameTable.ProtocolName
ORDER BY AVG(ActivityTable.IdleMean) DESC
LIMIT 10;


--15 Query to find the average packet length for each protocol

SELECT ProtocolNameTable.ProtocolName, AVG(PacketSizeTable.averagePacketSize) AS avg_packet_length
FROM PacketSizeTable
JOIN ProtocolTable ON PacketSizeTable.flowId = ProtocolTable.flowID
JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
GROUP BY ProtocolNameTable.ProtocolName;


--16 This query can be used to identify flows that have unusually long inter-arrival times between packets, which could be indicative of certain types of applications or activities.

SELECT ProtocolNameTable.ProtocolName, IATTable.flowIATMax, FlowTable.timestamp
FROM ProtocolNameTable
INNER JOIN ProtocolTable ON ProtocolNameTable.L7Protocol = ProtocolTable.L7Protocol
INNER JOIN FlowTable ON ProtocolTable.flowID = FlowTable.flowID
INNER JOIN IATTable ON FlowTable.flowID = IATTable.flowID
ORDER BY IATTable.flowIATMax DESC
LIMIT 10;


--17  This table can be useful for analyzing network traffic patterns and identifying potential network congestion or bandwidth issues.
--    For example, a high down/up ratio for a particular flow could indicate that the flow is consuming more downlink bandwidth than uplink bandwidth, which could lead to network congestion or other performance issues. Network administrators can use this information to identify and resolve such issues.

SELECT ProtocolNameTable.ProtocolName, FlowTable.TimeStamp, RatioTable.downUpRatio
FROM FlowTable
JOIN ProtocolTable ON FlowTable.flowId = ProtocolTable.flowId
JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
JOIN RatioTable ON FlowTable.flowId = RatioTable.flowId
WHERE RatioTable.downUpRatio > 200
ORDER BY RatioTable.downUpRatio DESC;


--18 For a particular time range which app uses time.

SELECT ProtocolNameTable.ProtocolName, SUM(FlowTable.flowDuration) AS count
FROM FlowTable
INNER JOIN ProtocolTable ON FlowTable.flowID = ProtocolTable.flowID
INNER JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
WHERE timestamp >= '2017-04-27 11:00:00' AND timestamp < '2017-04-27 12:00:00'
GROUP BY ProtocolNameTable.ProtocolName
ORDER BY count DESC;


--19 Top 10 flows with longest avgDuration
SELECT *
FROM FlowTable
ORDER BY flowDuration DESC
LIMIT 10;


--20

WITH RECURSIVE paths AS (

  SELECT
    FlowTable.flowId,
    FlowTable.sourceIp,
    FlowTable.destinationIp,
    FlowTable.timestamp,
    ARRAY[FlowTable.flowId] AS flowIds
  FROM
    FlowTable
  WHERE
    FlowTable.sourceIp = '192.168.180.37'
    AND FlowTable.destinationIp = '10.200.7.7'

  UNION ALL

  SELECT
    f.flowId,
    p.sourceIp,
    f.destinationIp,
    f.timestamp,
    p.flowIds || f.flowId
  FROM
    paths p
    INNER JOIN FlowTable f ON p.destinationIp = f.sourceIp
    AND p.timestamp = f.timestamp
    AND array_length(p.flowIds,1) < 100
  WHERE
     NOT (f.flowId = ANY(p.flowIds))
)

SELECT
  flowIds
FROM
  paths
WHERE
  destinationIp = '10.200.7.7'

LIMIT 1;


--21 protocols having avg(initial window) in desc
SELECT
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
LIMIT 10;

--22 protocols having avg(initial window) negative

SELECT
  ProtocolNameTable.ProtocolName,
  AVG(WindowTable.InitWinbytesforward + WindowTable.InitWinbytesbackward) AS AvgInitWinBytes
FROM
  ProtocolTable
  INNER JOIN ProtocolNameTable ON ProtocolTable.L7Protocol = ProtocolNameTable.L7Protocol
  INNER JOIN WindowTable ON ProtocolTable.flowId = WindowTable.flowId
GROUP BY
  ProtocolNameTable.ProtocolName
having AVG(WindowTable.InitWinbytesforward + WindowTable.InitWinbytesbackward) < 0;


--23 daily activeness in 6 days

SELECT
  ProtocolNameTable.ProtocolName AS protocol_name,
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


--24 hourly activeness in a given day

  SELECT
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


--25 reachable ip from the given ip address in a given time TimeStamp

WITH RECURSIVE ReachableNodes AS (
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
ORDER BY timestamp;


--26 in a given TimeStamp which source ip has highest traffic

  SELECT
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
  10;
