# ic: the Infinite Compute command line


```bash
pipx install infinitecompute
ic login                      # paste an API key from the console (Account → API keys)
ic whoami
ic server-types
ic images --gpu h100
ic ssh-keys add laptop ~/.ssh/id_ed25519.pub
ic servers create train --type <server type> --image <image> --ssh-key laptop --wait
ic ssh train                  # opens SSH access if needed, then runs ssh
ic servers park train         # frees the GPU, keeps the disk
ic servers resume train --wait
ic volumes create data --size-gb 100 --site <site id>
ic volumes attach <volume id> train
ic usage --month 2026-10
ic servers delete train
```

Every command takes `--json`. The key comes from `INFINITECOMPUTE_API_KEY` if set, else the
OS keyring (`ic login` / `ic logout`). `--api-url` or `INFINITECOMPUTE_API_URL` overrides the
API address.

## Development

The API client in `src/infinitecompute/_api/` is generated from `openapi-v1.json`, the public
API contract (`/api/public/v1/openapi.json`). Never edit it by
hand: copy the new contract in and run `make generate`. The commands live in
`src/infinitecompute/cli.py`.

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
make test lint
```
