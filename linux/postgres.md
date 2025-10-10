* https://www.pgconfig.org/
* Docker
    * https://hub.docker.com/_/postgres/
    * https://github.com/docker-library/postgres
* Backup: WAL-G
    * https://habr.com/ru/articles/506610/


```shell
docker exec -it postgres psql
# View cluster information
docker exec -it postgres pg_controldata -D /var/lib/postgres/data
```

```sql
-- List all databases
\list
-- connect to a db (or \c)
\connect gitlabhq_production
-- list all tables in the current database using search_path
\dt
-- list all tables in the current database regardless of search_path
\dt *
-- list users
\du
-- list users adding description column
\du+

-- turn off pager
\pset pager off
```

### Optimization
```SQL
-- View index size
-- It is optimal if `shared_buffers = nGB` in postgres.conf allows to fit all indexes
SELECT
   relname  as table_name,
   pg_size_pretty(pg_total_relation_size(relid)) As "Total Size",
   pg_size_pretty(pg_indexes_size(relid)) as "Index Size",
   pg_size_pretty(pg_relation_size(relid)) as "Actual Table Size"
   FROM pg_catalog.pg_statio_user_tables 
ORDER BY pg_total_relation_size(relid) DESC LIMIT 20;
```

### pg_upgrade
* https://github.com/tianon/docker-postgres-upgrade
* https://dev.to/rafaelbernard/postgresql-pgupgrade-from-10-to-12-566i


### Patroni
* https://patroni.readthedocs.io/en/latest/
* https://github.com/patroni/patroni
* :bulb: https://www.mydbops.com/blog/convert-your-postgresql-database-to-a-patroni-cluster/
* :grey_question: https://www.percona.com/blog/administering-a-patroni-managed-postgresql-cluster/

```shell
docker exec -it postgres patronictl -c /var/lib/postgres/patroni.yml list
docker exec -it postgres patronictl -c /var/lib/postgres/patroni.yml switchover --master gitlab-test-db-03 --candidate gitlab-test-db-01 --force
# https://patroni.readthedocs.io/en/latest/pause.html
docker exec -it postgres patronictl -c /var/lib/postgres/patroni.yml pause --wait
```

#### Debug

patroni.yml
```yaml
log:
  level: DEBUG
```

```shell
docker exec -it -e PATRONI_LOG_LEVEL=DEBUG postgres patronictl -c /var/lib/postgres/patroni.yml list
```
### Transaction wraparound

* https://www.rockdata.net/tutorial/troubleshooting-txn-wraparound/#fix-transaction-wraparound
* https://www.tigerdata.com/blog/how-to-fix-transaction-id-wraparound

```sql
-- Select dead tuples data (need to be connected to a DB)
SELECT 
  t.relname, 
  t.n_dead_tup, 
  c.reltuples AS total_estimated_rows,
  ROUND(
    CASE 
      WHEN c.reltuples > 0 THEN (t.n_dead_tup::numeric / c.reltuples::numeric) * 100
      ELSE 0
    END, 2
  ) AS dead_tup_percent
FROM 
  pg_stat_user_tables t
JOIN 
  pg_class c ON c.oid = t.relid
ORDER BY 
  t.n_dead_tup DESC LIMIT 10;
```
