run:    ; cd apps/api && pip install -q -r requirements.txt && uvicorn main:app --reload
test:   ; pip install -q -r apps/api/requirements.txt pytest && python -m pytest -q tests
docker: ; docker compose -f infra/docker-compose.yml up --build
