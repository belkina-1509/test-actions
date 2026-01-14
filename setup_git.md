# Инструкция по подключению к GitHub

## Шаг 1: Установка Git
1. Скачайте Git с https://git-scm.com/download/win
2. Установите с настройками по умолчанию
3. Перезапустите терминал после установки

## Шаг 2: Создание Personal Access Token на GitHub
GitHub больше не принимает пароли для HTTPS. Нужно создать токен:

1. Перейдите на https://github.com/settings/tokens
2. Нажмите "Generate new token" → "Generate new token (classic)"
3. Название: "My Local Machine"
4. Выберите срок действия (например, 90 дней)
5. Отметьте галочку `repo` (полный доступ к репозиториям)
6. Нажмите "Generate token"
7. **ВАЖНО**: Скопируйте токен сразу (он показывается только один раз!)

## Шаг 3: Настройка Git

Откройте PowerShell в папке проекта и выполните:

```powershell
# Настройка имени и email
git config --global user.name "Ваше Имя"
git config --global user.email "barmina1509@gmail.com"

# Инициализация репозитория
git init

# Добавление файлов
git add .

# Первый коммит
git commit -m "Initial commit: FastAPI server time application"

# Добавление удаленного репозитория (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/Actions.git

# Отправка на GitHub (используйте токен вместо пароля)
git push -u origin main
```

При запросе пароля:
- Username: ваш GitHub username
- Password: вставьте Personal Access Token (не пароль!)

## Альтернатива: Создание репозитория через веб-интерфейс

1. Зайдите на https://github.com/new
2. Название репозитория: `Actions`
3. Выберите Public или Private
4. **НЕ** отмечайте "Initialize this repository with a README"
5. Нажмите "Create repository"
6. Скопируйте URL репозитория и используйте его в команде `git remote add origin`
