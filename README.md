## Dependencies

The `Pipfile` in this repository describes the runtime dependencies. For
development, most users will want to use `pipenv`.

## Deployment

The provided `Dockerfile` can build a self-contained container to run the
server, only needing an external database server. Refer to
`decbot_web/settings_container.py` to see how it can be configured with
environment variables. Command-line options are passed directly to `gunicorn`,
so for instance to run the server listening on all network interfaces, port
8000:

```
docker run registry.gitlab.com/cemetech/decbot_web:stable -b 0.0.0.0:8000
```
