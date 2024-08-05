* Docker
    * https://hub.docker.com/_/postgres/
    * https://github.com/docker-library/postgres
* Backup: WAL-G
    * https://habr.com/ru/articles/506610/


```shell
docker exec -it postgres psql
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
