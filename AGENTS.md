# Repository guidelines

- Configuration lives in `webapp/config/settings.py`. Do not create additional config files.
- All Python modules, including the polling bot, reside inside the `webapp` package.
- Use 4 spaces for indentation.
- Run syntax checks before committing:

```bash
python3 -m py_compile manage.py webapp/monitor/*.py webapp/config/settings.py
```

- Static assets (fonts, images) belong in `webapp/monitor/zbxTelegram_files`.

