# Restore Zabbix DB from backup

Procedure for restoring a Zabbix PostgreSQL database running in docker compose from a `postgres-backup-local` dump (gzipped plain SQL). The DB container keeps running, Zabbix server, web and backup containers are stopped, the DB is dropped, recreated and loaded from the dump.

## 0. Set variables

Adjust to the host. Service names are the compose service names, not container names.

```bash
COMPOSE_DIR=/opt/docker-configs/local/zabbix
BACKUP_DIR=/mnt/backup/zabbix              # host path mounted to /backups of the backup container
DB_CONTAINER=postgresql-server
DB_USER=zabbix
DB_NAME=zabbix
STOP_SERVICES="zabbix-server zabbix-web-nginx-pgsql postgresql-backup"
cd "$COMPOSE_DIR" && docker compose ps
```

## 1. Choose a backup

```bash
ls -lh "$BACKUP_DIR"/{last,daily,weekly,monthly}/
BACKUP=$BACKUP_DIR/daily/zabbix-YYYYMMDD-HHMMSS.sql.gz
```

## 2. Verify the backup

```bash
gzip -t "$BACKUP" && echo OK
zcat "$BACKUP" | head -30
zcat "$BACKUP" | tail -5    # must end with "PostgreSQL database dump complete"
```

**STOP** if the file is corrupt or truncated.

## 3. Check Zabbix version in the backup

```bash
zcat "$BACKUP" | grep -A3 '^COPY public.dbversion'
docker compose images zabbix-server
```

Older DB is upgraded automatically on server start. **STOP** if the backup is from a *newer* Zabbix version than the running one.

## 4. Check space on the DB data disk

```bash
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));"
docker inspect -f '{{range .Mounts}}{{.Source}} {{end}}' $DB_CONTAINER | xargs df -h
df -h "$BACKUP_DIR"
```

**STOP** if not enough space (restored DB ≈ current size; plus a safety dump in step 7).

## 5. Stop everything except the DB

```bash
docker compose stop $STOP_SERVICES
docker compose ps
docker exec $DB_CONTAINER psql -U $DB_USER -d postgres \
  -c "SELECT datname, usename, client_addr FROM pg_stat_activity WHERE datname='$DB_NAME';"
```

The backup container is stopped too, so it doesn't dump or rotate backups mid-restore.

## 6. Take a hypervisor snapshot

## 7. Dump the current DB (optional)

```bash
docker exec $DB_CONTAINER pg_dump -U $DB_USER -d $DB_NAME -Z1 \
  > "$BACKUP_DIR/pre-restore-$(date +%Y%m%d-%H%M%S).sql.gz"
gzip -t "$BACKUP_DIR"/pre-restore-*.sql.gz && echo OK
```

## 8. Drop and recreate the DB

```bash
docker exec $DB_CONTAINER psql -U $DB_USER -d postgres -c "DROP DATABASE $DB_NAME WITH (FORCE);"
docker exec $DB_CONTAINER psql -U $DB_USER -d postgres \
  -c "CREATE DATABASE $DB_NAME OWNER $DB_USER ENCODING 'UTF8' TEMPLATE template0;"
```

## 9. Restore

```bash
zcat "$BACKUP" | docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME > /tmp/zabbix-restore.log 2>&1
grep -c ERROR /tmp/zabbix-restore.log
grep ERROR /tmp/zabbix-restore.log
```

`schema "public" already exists` is harmless. **STOP** on any other error.

## 10. Verify data

```bash
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT mandatory, optional FROM dbversion;"
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT count(*) FROM hosts;"
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT to_timestamp(max(clock)) FROM history_uint;"   # ≈ backup time
docker exec $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));"
```

## 11. Start and check

```bash
docker compose up -d
docker compose ps
docker compose logs -f --tail=100 zabbix-server   # DB upgrade messages, "server #0 started"
docker compose logs --tail=20 postgresql-backup
```

- Web UI: Reports → System information, Monitoring → Latest data (new values arriving)
- When everything works: delete the pre-restore dump and the hypervisor snapshot
