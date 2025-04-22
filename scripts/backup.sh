#!/bin/bash
set -e

# Получение текущей даты
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="/backups"

# Создание временных директорий
mkdir -p ${BACKUP_DIR}/postgres
mkdir -p ${BACKUP_DIR}/media

# Пути к файлам резервных копий
POSTGRES_BACKUP="${BACKUP_DIR}/postgres/db_backup_${TIMESTAMP}.sql.gz"
MEDIA_BACKUP="${BACKUP_DIR}/media/media_backup_${TIMESTAMP}.tar.gz"

echo "Создание резервной копии базы данных PostgreSQL..."
pg_dump -h db -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-foodplan} | gzip > ${POSTGRES_BACKUP}

echo "Создание резервной копии медиа-файлов..."
tar -czf ${MEDIA_BACKUP} -C /media_backup .

echo "Резервные копии созданы:"
echo "  - База данных: ${POSTGRES_BACKUP}"
echo "  - Медиа-файлы: ${MEDIA_BACKUP}"

# Создание симлинков на последние резервные копии
ln -sf ${POSTGRES_BACKUP} ${BACKUP_DIR}/postgres/latest.sql.gz
ln -sf ${MEDIA_BACKUP} ${BACKUP_DIR}/media/latest.tar.gz

# Удаление старых резервных копий (по умолчанию хранятся 7 дней)
find ${BACKUP_DIR}/postgres -name "db_backup_*.sql.gz" -type f -mtime +${BACKUP_KEEP_DAYS:-7} -delete
find ${BACKUP_DIR}/media -name "media_backup_*.tar.gz" -type f -mtime +${BACKUP_KEEP_DAYS:-7} -delete

echo "Старые резервные копии удалены (старше ${BACKUP_KEEP_DAYS:-7} дней)"
echo "Резервное копирование завершено успешно!" 