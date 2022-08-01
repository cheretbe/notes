```shell
# Run shell (sqlite runs version 2.x)
sqlite3
```

```
 create table f1(id,user_id,message_id,rate);
 create table f2(id,type,timestamp);

 .separator ,
 .import 'file_1.txt' f1
 .import 'file_2.txt' f2

 CREATE INDEX i1 ON f1(message_id ASC); -- optional
 CREATE INDEX i2 ON f2(id ASC);         -- optional

 .output 'output.txt'
 .separator ,

 SELECT f1.id, f1.user_id, f1.message_id, f1.rate, f2.timestamp
   FROM f1
   JOIN f2 ON f2.id = f1.message_id;

 .output stdout
 .q
```
