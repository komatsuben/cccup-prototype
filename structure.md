CCCUP/
├── app/
│   ├── __init__.py         # Application factory, config loading, db initialization, blueprint registration
│   ├── models.py           # SQLAlchemy models for users, registrations, coupons, competitions, etc.
│   ├── main/               # Blueprint for public-facing views (registration, competition pages)
│   │   ├── __init__.py     # Create and register the 'main' blueprint
│   │   └── routes.py       # Public routes (e.g., homepage, registration form)
│   ├── admin/              # Blueprint for admin panel
│   │   ├── __init__.py     # Create and register the 'admin' blueprint (optionally integrate flask-admin here)
│   │   └── routes.py       # Admin routes (manage registrations, coupons, competitions)
│   ├── competition/        # Optional: If you want a separate blueprint for competition logic
│   │   ├── __init__.py     
│   │   └── routes.py       
│   ├── static/             # Static files: CSS, JS, images
│   └── templates/          # HTML templates (you might create subfolders for main and admin templates)
│       ├── base.html
│       ├── main/
│       │    └── index.html
│       └── admin/
│            └── dashboard.html
├── config.py               # Application configuration (database URI, secret key, etc.)
├── run.py                  # Entry point for running the application
└── requirements.txt        # List of project dependencies

If there's a flask blueprint admin conflict issue go to(i think it will help):
https://stackoverflow.com/questions/22064871/how-do-i-add-flask-admin-to-a-blueprint