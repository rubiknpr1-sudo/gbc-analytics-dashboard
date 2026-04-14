# GBC Analytics Dashboard

Аналитический дашборд заказов с интеграцией RetailCRM → Supabase → Vercel + Telegram-уведомления.

## 🔗 Ссылки

- **Dashboard**: [gbc-analytics-dashboard-opal.vercel.app](https://gbc-analytics-dashboard-opal.vercel.app)
- **GitHub**: [rubiknpr1-sudo/gbc-analytics-dashboard](https://github.com/rubiknpr1-sudo/gbc-analytics-dashboard)
- **Telegram Bot**: [@gbc2_analytics_dashboard_bot](https://t.me/gbc2_analytics_dashboard_bot)

## 📋 Что сделано

### Шаг 1: Аккаунты
Созданы аккаунты: RetailCRM (демо), Supabase (Free), Vercel (Hobby), Telegram Bot (BotFather).

### Шаг 2: Загрузка заказов в RetailCRM
50 тестовых заказов из `mock_orders.json` загружены через RetailCRM API (`/api/v5/orders/create`).

**Проблема**: тип заказа `eshop-individual` из mock-данных не существует в демо-CRM.  
**Решение**: запросил справочник через `/api/v5/reference/order-types`, заменил на `main`.

### Шаг 3: Пайплайн RetailCRM → Supabase
Python-скрипт забирает заказы из RetailCRM API, трансформирует данные и загружает в Supabase через REST API.

**Промпт Claude Code**: "Получи все заказы из RetailCRM API, трансформируй в формат Supabase таблицы orders и загрузи через REST API"

**Проблема**: RetailCRM не сохраняет customFields (utm_source) при создании заказа.  
**Решение**: utm_source маппится из оригинального mock_orders.json по номеру телефона.

### Шаг 4: Dashboard на Vercel
Статический HTML дашборд с Chart.js + Supabase JS SDK (через CDN). Без npm/node_modules — деплоится как static site.

**Почему не Next.js**: MacBook Air 8GB RAM — npm install убивался системой (OOM kill). Решение — статический HTML с CDN библиотеками.

**Промпт Claude Code**: "Создай аналитический дашборд на статическом HTML с Chart.js и Supabase CDN. 4 карточки метрик, 4 графика (города, UTM, выручка, товары), таблица заказов. Тёмная тема."

**Проблема**: Supabase CDN URL `@supabase/supabase-js@2/dist/umd/supabase.min.js` не резолвился.  
**Решение**: указал конкретную версию `@2.49.4`.

**Проблема**: RLS блокировал анонимный доступ к таблице.  
**Решение**: `CREATE POLICY "Allow public read" ON orders FOR SELECT TO anon USING (true);`

### Шаг 5: Telegram-уведомления
Python-скрипт `notify.py` — запрашивает заказы > 50 000 ₸ из Supabase и отправляет сводку в Telegram.

**Промпт Claude Code**: "Создай Python-скрипт без зависимостей (только urllib) который берёт заказы > 50000 из Supabase и шлёт уведомление в Telegram бота"

## 🛠 Стек

- **Frontend**: HTML + CSS + Chart.js 4 (CDN)
- **Database**: Supabase (PostgreSQL)
- **CRM**: RetailCRM API v5
- **Deploy**: Vercel (static)
- **Notifications**: Telegram Bot API + Python
- **AI Tool**: Claude Code CLI (Anthropic)

## 📊 Метрики дашборда

- Всего заказов: 50
- Общая выручка: 2 451 000 ₸
- Средний чек: 49 020 ₸
- Крупные заказы (>50K): 24
- Города: Алматы, Астана, Шымкент, Актау
- Источники: Instagram, Google, TikTok, Direct, Referral

## 🚀 Запуск уведомлений

```bash
python3 notify.py
```

## 📁 Структура

```
├── index.html      # Дашборд (Chart.js + Supabase)
├── notify.py       # Telegram-уведомления
├── vercel.json     # Конфиг деплоя
├── package.json    # Метаданные проекта
└── README.md       # Документация
```

## 🧩 Основные трудности и решения

| Проблема | Решение |
|----------|---------|
| `orderType` не существует в демо RetailCRM | Запрос справочника `/reference/order-types`, замена на `main` |
| npm killed (OOM) на 8GB MacBook | Отказ от Next.js, статический HTML + CDN |
| Supabase SDK CDN не грузился | Указание конкретной версии `@2.49.4` |
| RLS блокировал anon доступ | Политика `SELECT TO anon USING (true)` |
| customFields не сохранялись в RetailCRM | Маппинг utm_source из оригинального JSON по телефону |
| Telegram "chat not found" | Необходимо отправить `/start` боту перед уведомлениями |
