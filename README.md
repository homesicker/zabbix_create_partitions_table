# zabbix_create_partitions_table
create tsql queries for zabbix partitioning, pgsql 12

generate tsql CREATE queries for zabbix partitioning, generate part for one week

and you need this query

CREATE TABLE public.history_max PARTITION OF public.history FOR VALUES FROM (#CHANGE THIS TO YOU MAX DATE IN UNIX TIME) TO (MAXVALUE);

CREATE TABLE public.history_min PARTITION OF public.history FOR VALUES FROM (MINVALUE) TO (#CHANGE THIS TO YOU MIN DATE IN UNIX TIME);
