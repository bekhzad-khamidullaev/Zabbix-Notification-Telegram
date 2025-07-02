# Repository guidelines

- Configuration is stored in `webapp/settings.py`. Update this file instead of creating new config modules.
- The Django project lives in `webapp`. When adding Python code use 4 spaces for indentation.
- Run basic syntax checks before committing:

```bash
python3 -m py_compile bot.py webapp/manage.py webapp/monitor/*.py webapp/settings.py
```

