# GitHub Actions Workflow - Инструкция по настройке

## Описание

Workflow автоматически:
1. **Собирает Docker образ** при пуше в ветки `main` или `master`
2. **Публикует образ** в GitHub Container Registry (ghcr.io)
3. **Деплоит приложение** на удаленный сервер через SSH

## Необходимые секреты

Настройте следующие секреты в настройках репозитория GitHub:
**Settings → Secrets and variables → Actions → New repository secret**

### Обязательные секреты:

1. **`SSH_HOST`** - IP адрес или доменное имя вашего сервера
   - Пример: `192.168.1.100` или `example.com`

2. **`SSH_USER`** - Имя пользователя для SSH подключения
   - Пример: `root` или `deploy`

3. **`SSH_PRIVATE_KEY`** - Приватный SSH ключ для подключения к серверу
   - Содержимое приватного ключа (например, `~/.ssh/id_rsa`)
   - **ВАЖНО**: Не забудьте добавить соответствующий публичный ключ на сервер в `~/.ssh/authorized_keys`

### Опциональные секреты:

4. **`SSH_PORT`** - Порт SSH (по умолчанию: `22`)
   - Пример: `2222`

5. **`PORT`** - Порт на сервере для проброса контейнера (по умолчанию: `8000`)
   - Пример: `8080`

## Настройка SSH ключа

### На локальной машине:

```bash
# Генерация SSH ключа (если еще нет)
ssh-keygen -t rsa -b 4096 -C "github-actions"

# Скопируйте публичный ключ на сервер
ssh-copy-id -p <SSH_PORT> <SSH_USER>@<SSH_HOST>

# Или вручную:
cat ~/.ssh/id_rsa.pub | ssh -p <SSH_PORT> <SSH_USER>@<SSH_HOST> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### Добавление приватного ключа в GitHub:

1. Скопируйте содержимое приватного ключа:
   ```bash
   cat ~/.ssh/id_rsa
   ```

2. В GitHub: **Settings → Secrets → Actions → New repository secret**
   - Name: `SSH_PRIVATE_KEY`
   - Value: вставьте содержимое приватного ключа

## Требования на сервере

На удаленном сервере должен быть установлен Docker:

```bash
# Проверка установки Docker
docker --version

# Если не установлен, установите:
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

## Проверка работы

После настройки секретов:

1. Сделайте коммит и пуш в ветку `main` или `master`
2. Перейдите в **Actions** в вашем GitHub репозитории
3. Следите за выполнением workflow
4. После успешного деплоя проверьте контейнер на сервере:
   ```bash
   ssh <SSH_USER>@<SSH_HOST> "docker ps | grep fastapi-time-app"
   ```

## Ручной запуск

Workflow можно запустить вручную через:
**Actions → Build and Deploy → Run workflow**
