BEGIN TRANSACTION;

DROP TABLE IF EXISTS FlowTable;
DROP TABLE IF EXISTS LengthTable;
DROP TABLE IF EXISTS PacketSizeTable;
DROP TABLE IF EXISTS BulkRateTable;
DROP TABLE IF EXISTS TCPFlagTable;
DROP TABLE IF EXISTS WindowTable;
DROP TABLE IF EXISTS IATTable;
DROP TABLE IF EXISTS LabelTable;
DROP TABLE IF EXISTS SubflowTable;
DROP TABLE IF EXISTS ProtocolTable;
DROP TABLE IF EXISTS ProtocolNameTable;
DROP TABLE IF EXISTS ActivityTable;
DROP TABLE IF EXISTS RatioTable;
DROP TABLE IF EXISTS PSHFlagTable;
DROP TABLE IF EXISTS URGFlagTable;
---

CREATE TABLE FlowTable(
  flowId numeric NOT NULL,
  sourceIp varchar(20) NOT NULL,
  sourcePort numeric NOT NULL,
  destinationIp varchar(20) NOT NULL,
  destinationPort numeric NOT NULL,
  protocol numeric NOT NULL,
  timestamp varchar(30) NOT NULL,
  flowDuration numeric NOT NULL,
  PRIMARY KEY(flowId)
);

CREATE TABLE LengthTable(
  flowId numeric NOT NULL,
  totalFwdPackets numeric NOT NULL,
  totalBwdPackets numeric NOT NULL,
  totalLengthOfFwdPackets numeric NOT NULL,
  totalLengthOfBwdPackets numeric NOT NULL,
  fwdPacketsLengthMax numeric NOT NULL,
  fwdPacketsLengthMin numeric NOT NULL,
  fwdPacketsLengthMean float NOT NULL,
  fwdPacketsLengthStd float NOT NULL,
  bwdPacketsLengthMax numeric NOT NULL,
  bwdPacketsLengthMin numeric NOT NULL,
  bwdPacketsLengthMean float NOT NULL,
  bwdPacketsLengthStd float NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_length
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);

---

--- Table Structure for Packet Size Table

---

CREATE TABLE PacketSizeTable(
  flowId numeric NOT NULL,
  minPacketLength numeric NOT NULL,
  maxPacketLength numeric NOT NULL,
  packetLengthMean float NOT NULL,
  packetLengthStd float NOT NULL,
  packetLengthVariance float NOT NULL,
  averagePacketSize float NOT NULL,
  avgFwdSegmentSize float NOT NULL,
  avgBwdSegmentSize float NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_packetsize
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);

---

--- Table Structure for BulkRate TABLE

---

CREATE TABLE BulkRateTable(
  flowId numeric NOT NULL,
  fwdAvgBytesBulk float NOT NULL,
  fwdAvgPacketsBulk float NOT NULL,
  fwdAvgBulkRate float NOT NULL,
  bwdAvgBytesBulk float NOT NULL,
  bwdAvgPacketsBulk float NOT NULL,
  bwdAvgBulkRate float NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_bulk
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);
---

--- Table Structure for TCP Flag TABLE

---

CREATE TABLE TCPFlagTable(
  flowId numeric NOT NULL,
  FINFlagCount numeric NOT NULL,
  SYNFalgCount numeric NOT NULL,
  RSTFlagCount numeric NOT NULL,
  PSHFlagCount numeric NOT NULL,
  ACKFlagCount numeric NOT NULL,
  URGFlagCount numeric NOT NULL,
  CWEFlagCount numeric NOT NULL,
  ECEFlagCount numeric NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_tcpflag
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);

---

--- Table Structure for Window Table

---

CREATE TABLE WindowTable(
  flowId numeric NOT NULL,
  InitWinbytesforward numeric NOT NULL,
  InitWinbytesbackward numeric NOT NULL,
  actdatapktfwd numeric NOT NULL,
  minsegsizeforward numeric NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_window
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);

---

--- Table Structure for IAT Table

---

CREATE TABLE IATTable(
  flowId numeric NOT NULL,
  flowIATMean float NOT NULL,
  flowIATStd float NOT NULL,
  flowIATMax numeric NOT NULL,
  flowIATMin numeric NOT NULL,
  fwdIATTotal numeric NOT NULL,
  fwdIATMean float NOT NULL,
  fwdIATStd float NOT NULL,
  fwdIATMax numeric NOT NULL,
  FwdIATMin numeric NOT NULL,
  BwdIATTotal numeric NOT NULL,
  BwdIATMean float NOT NULL,
  BwdIATStd float NOT NULL,
  BwdIATMax numeric NOT NULL,
  BwdIATMin numeric NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_IAT
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);

---

--- Table Structure for Lable Table

---

CREATE TABLE LabelTable(
  flowId numeric NOT NULL,
  label varchar(6) NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_label
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);

---

--- Table Structure for Subflow Table

---

CREATE TABLE SubflowTable(
  flowId numeric NOT NULL,
  SubflowFwdPackets numeric NOT NULL,
  SubflowFwdBytes numeric NOT NULL,
  SubFlowBwdPackets numeric NOT NULL,
  SubFlowBwdBytes numeric NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_subflow
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);


---

--- Table Structure for Protocol Name TABLE

---

CREATE TABLE ProtocolNameTable(
  L7Protocol numeric NOT NULL,
  ProtocolName varchar(20),
  PRIMARY KEY(L7Protocol)
);


---

--- Table Structure For protocol Table

---

CREATE TABLE ProtocolTable(
  flowId numeric NOT NULL,
  L7Protocol numeric NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_l7protocol
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId),
  CONSTRAINT fk_name_prtocol
  FOREIGN KEY(L7Protocol)
  REFERENCES ProtocolNameTable(L7Protocol)
);

---

--- Table Structute for Activity TABLE

---

CREATE TABLE ActivityTable(
  flowId numeric NOT NULL,
  ActiveMean float NOT NULL,
  ActiveStd float NOT NULL,
  ActiveMax numeric NOT NULL,
  ActivityMin numeric NOT NULL,
  IdleMean float NOT NULL,
  IdleStd float NOT NULL,
  IdleMax numeric NOT NULL,
  IdleMin numeric NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_activity
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);

---

--- Table Structure for Ratio TABLE

---

CREATE TABLE RatioTable(
  flowId numeric NOT NULL,
  downUpRatio float NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_ratio
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);

---

--- Table Structure for PSHFalg Table

---

CREATE TABLE PSHFlagTable(
  flowId numeric NOT NULL,
  fwdPSHFlags numeric NOT NULL,
  bwdPSHFlags numeric NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_pshflag
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);

---

--- Table Structure for URGFlag TABLE

---

CREATE TABLE URGFlagTable(
  flowId numeric NOT NULL,
  fwdURGFlags numeric NOT NULL,
  bwdURGFlags numeric NOT NULL,
  PRIMARY KEY(flowId),
  CONSTRAINT fk_flow_urgflag
  FOREIGN KEY(flowId)
  REFERENCES FlowTable(flowId)
);



------------------------------------------------------

END TRANSACTION;
