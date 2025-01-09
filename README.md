## Django Starter Template

#### Change Me
- Rename the settings folder to your project name

```sh
mv rename_me project_name
```

- Relace with your project name

```sh
ROOT_URLCONF = '<project_name>.urls'  # settings.py
```

```sh
WSGI_APPLICATION = '<project_name>.wsgi.application'  # settings.py
```

```sh
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '<project_name>.settings') # asgi.py, wsgi.py and manage.py
```