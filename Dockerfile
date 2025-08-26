FROM python:3.13-slim

# Указываем необходимые переменные
ARG ARCH=amd64

ENV PYTHONPATH=/qaguru_advanced/ \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Копируем файлы
WORKDIR /qaguru_advanced
COPY . .

# Устанавливаем зависимости через uv с кешированием
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --all-groups

#
#CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# fastapi нужно добавлять через uv add fastapi --extra standard. Иначе не запустится командой ниже
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
