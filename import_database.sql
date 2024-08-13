BEGIN TRANSACTION;

COPY FlowTable FROM '/path/to/Flowtable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY URGFlagTable FROM '/path/to/URGFlagTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY PSHFlagTable FROM '/path/to/PSHFlagTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY RatioTable FROM '/path/to/RatioTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY ActivityTable FROM '/path/to/ActivityTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY ProtocolNameTable FROM '/path/to/ProtocolNameTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY ProtocolTable FROM '/path/to/ProtocolTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY SubflowTable FROM '/path/to/SubflowTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY LabelTable FROM '/path/to/LabelTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY IATTable FROM '/path/to/IATTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY WindowTable FROM '/path/to/WindowTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY TCPFlagTable FROM '/path/to/TCPFlagTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY BulkRateTable FROM '/path/to/BulkRateTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY PacketSizeTable FROM '/path/to/PacketSizeTable_db.csv'  WITH DELIMITER ',' CSV HEADER;
COPY LengthTable FROM '/path/to/LengthTable_db.csv'  WITH DELIMITER ',' CSV HEADER;

UPDATE FlowTable SET timestamp = TO_TIMESTAMP(timestamp, 'DD/MM/YYYYHH24:MI:SS');

END TRANSACTION;
