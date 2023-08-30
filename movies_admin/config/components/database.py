from config.settings import env


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST", "127.0.0.1"),
        "PORT": env.int("DB_PORT", 5432),
        "OPTIONS": {"options": "-c search_path=public,content"},
    }
}
