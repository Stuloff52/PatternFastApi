# Frontend - Интернет-магазин

Современный фронтенд для интернет-магазина на React + TypeScript + Tailwind CSS.

## 🚀 Особенности

- ⚛️ React 18 с TypeScript
- 🎨 Tailwind CSS для стилизации
- 🛣️ React Router для навигации
- 🔐 JWT аутентификация
- 📱 Адаптивный дизайн
- ⚡ Vite для быстрой разработки

## 📋 Требования

- Node.js 18+
- npm или yarn

## 🛠️ Установка

```bash
cd frontend
npm install
```

## 🏃 Запуск

```bash
# Режим разработки
npm run dev

# Сборка для продакшена
npm run build

# Просмотр собранного приложения
npm run preview
```

Приложение будет доступно на http://localhost:3000

## 🔧 Настройка

Создайте файл `.env` в папке `frontend`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 📁 Структура

```
frontend/
├── src/
│   ├── components/     # Переиспользуемые компоненты
│   ├── pages/          # Страницы приложения
│   ├── context/        # React Context (Auth)
│   ├── lib/            # Утилиты и API клиент
│   └── App.tsx         # Главный компонент
├── public/             # Статические файлы
└── package.json
```

