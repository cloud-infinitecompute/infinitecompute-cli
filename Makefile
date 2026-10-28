# Regenerate the API client from the contract. First save the latest contract from
# <api>/api/public/v1/openapi.json as openapi-v1.json. Never edit src/infinitecompute/_api by hand.
.PHONY: generate test lint

generate:
	openapi-python-client generate --path openapi-v1.json --config gen.yml --meta none \
	  --output-path src/infinitecompute/_api --overwrite

test:
	pytest -q

lint:
	ruff check .
