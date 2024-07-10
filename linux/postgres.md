```shell
docker exec -it postgres psql
```

```sql
-- List all databases
\list
-- connect to a db
\c gitlabhq_production
-- list all tables in the current database using search_path
\dt
-- list all tables in the current database regardless of search_path
\dt *
```
