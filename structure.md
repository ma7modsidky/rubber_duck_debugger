rubber_duck/
├── config/              # Django project configuration (renamed from rubber_duck)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                # All your custom Django apps live here
│   ├── debugger/        # The core logic for AI log analysis
│   │   ├── services/    # Where LangChain logic will live (Clean Architecture)
│   │   ├── models.py
│   │   └── views.py
├── static/              # Tailwind CSS and JS
├── templates/           # Global HTML templates
├── .env                 # API Keys (Never commit this!)
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt