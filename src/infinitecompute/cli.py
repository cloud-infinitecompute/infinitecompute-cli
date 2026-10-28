"""`ic`: the Infinite Compute command line.

A thin layer over the client generated from the public API contract
(`_api/`, from openapi-v1.json; regenerate with `make generate`). Every command
prints a table, or JSON with `--json`. API errors print the API's message and
request id and exit 1.

The API key comes from INFINITECOMPUTE_API_KEY, else the OS keyring (`ic login`).
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import time
import uuid
from collections.abc import Callable, Iterable, Sequence
from typing import Any

import httpx
import typer

from infinitecompute import __version__
from infinitecompute._api.api.catalog import list_images_images_get, list_server_types_server_types_get
from infinitecompute._api.api.keys import me_me_get
from infinitecompute._api.api.servers import (
    close_ssh_servers_server_id_ssh_delete,
    create_server_servers_post,
    create_ssh_key_ssh_keys_post,
    delete_server_servers_server_id_delete,
    delete_ssh_key_ssh_keys_name_delete,
    get_server_servers_server_id_get,
    get_ssh_servers_server_id_ssh_get,
    list_servers_servers_get,
    list_ssh_keys_ssh_keys_get,
    open_ssh_servers_server_id_ssh_put,
    server_action_servers_server_id_actions_post,
)
from infinitecompute._api.api.usage import get_usage_usage_get
from infinitecompute._api.api.volumes import (
    attach_volume_volumes_volume_id_attach_post,
    create_volume_volumes_post,
    delete_volume_volumes_volume_id_delete,
    detach_volume_volumes_volume_id_detach_post,
    list_backups_volumes_volume_id_backups_get,
    list_volumes_volumes_get,
    restore_backup_backups_backup_id_restore_post,
)
from infinitecompute._api.client import AuthenticatedClient
from infinitecompute._api.models import (
    BackupRestore,
    ServerAction,
    ServerCreate,
    SshKeyCreate,
    VolumeAttach,
    VolumeCreate,
)

DEFAULT_API_URL = "https://cloud.infinitecompute.ai/api/public/v1"
KEY_ENV = "INFINITECOMPUTE_API_KEY"
URL_ENV = "INFINITECOMPUTE_API_URL"
KEYRING_SERVICE = "infinitecompute"
KEYRING_USER = "api-key"
PAGE = 200

app = typer.Typer(help="Infinite Compute from the command line.", no_args_is_help=True)
servers_app = typer.Typer(help="GPU servers.", no_args_is_help=True)
volumes_app = typer.Typer(help="Volumes.", no_args_is_help=True)
backups_app = typer.Typer(help="Volume backups.", no_args_is_help=True)
ssh_keys_app = typer.Typer(help="Your SSH keys.", no_args_is_help=True)
app.add_typer(servers_app, name="servers")
app.add_typer(volumes_app, name="volumes")
app.add_typer(backups_app, name="backups")
app.add_typer(ssh_keys_app, name="ssh-keys")


class State:
    api_url: str = DEFAULT_API_URL
    as_json: bool = False
    transport: httpx.BaseTransport | None = None  # tests inject a mock transport


state = State()


@app.callback()
def main(
    api_url: str = typer.Option(None, "--api-url", envvar=URL_ENV, help="API base URL"),
    as_json: bool = typer.Option(False, "--json", help="Print JSON instead of tables"),
    version: bool = typer.Option(False, "--version", help="Print the version"),
) -> None:
    if version:
        typer.echo(__version__)
        raise typer.Exit()
    state.api_url = (api_url or DEFAULT_API_URL).rstrip("/")
    state.as_json = as_json


# --- plumbing ---------------------------------------------------------------------------


def fail(message: str, code: int = 1) -> None:
    typer.echo(f"error: {message}", err=True)
    raise typer.Exit(code)


def api_key() -> str:
    key = os.environ.get(KEY_ENV, "").strip()
    if key:
        return key
    try:
        import keyring

        key = (keyring.get_password(KEYRING_SERVICE, KEYRING_USER) or "").strip()
    except Exception:  # noqa: BLE001 - no keyring backend on this machine
        key = ""
    if not key:
        fail(f"no API key: run `ic login`, or set {KEY_ENV}")
    return key


def client() -> AuthenticatedClient:
    c = AuthenticatedClient(
        base_url=state.api_url,
        token=api_key(),
        headers={"User-Agent": f"infinitecompute-cli/{__version__}"},
        timeout=httpx.Timeout(60.0),
    )
    if state.transport is not None:
        c.set_httpx_client(
            httpx.Client(
                base_url=state.api_url,
                headers={"Authorization": f"Bearer {api_key()}"},
                transport=state.transport,
            )
        )
    return c


def call(fn: Any, **kwargs: Any) -> Any:
    """Run a generated endpoint; on an error print the API's message and exit 1."""
    try:
        resp = fn.sync_detailed(client=client(), **kwargs)
    except httpx.HTTPError as e:
        fail(f"can't reach the API at {state.api_url}: {type(e).__name__}")
    except ValueError:
        fail("the API answered with something that isn't JSON; try again later")
    status = int(resp.status_code)
    if status >= 400:
        try:
            err = json.loads(resp.content)["error"]
            fail(f"{err['message']} ({err['code']}, request {err['request_id']})")
        except (ValueError, KeyError, TypeError):
            fail(f"HTTP {status}")
    return resp.parsed


def as_dict(obj: Any) -> Any:
    if obj is None:
        return None
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return obj


def all_pages(fn: Any, **kwargs: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    cursor = None
    while True:
        page = call(fn, limit=PAGE, cursor=cursor, **kwargs) if cursor else call(fn, limit=PAGE, **kwargs)
        out.extend(as_dict(x) for x in page.data)
        cursor = page.next_cursor if isinstance(page.next_cursor, str) else None
        if not cursor:
            return out


def _cell(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        return ", ".join(_cell(v) for v in value) or "-"
    if isinstance(value, dict):
        return str(value.get("name") or value.get("id") or json.dumps(value))
    return str(value)


def show(rows: Any, columns: Sequence[tuple]) -> None:
    """rows: a dict or a list of dicts; columns: (header, getter or key)."""
    if state.as_json:
        typer.echo(json.dumps(rows, indent=2, default=str))
        return
    items = rows if isinstance(rows, list) else [rows]
    if not items:
        typer.echo("(none)")
        return
    table = [[h for h, _ in columns]]
    for r in items:
        table.append([_cell(g(r) if callable(g) else r.get(g)) for _, g in columns])
    widths = [max(len(row[i]) for row in table) for i in range(len(columns))]
    for row in table:
        typer.echo("  ".join(c.ljust(w) for c, w in zip(row, widths, strict=True)).rstrip())


def find_server(ref: str) -> dict[str, Any]:
    """A server by id or exact name."""
    servers = all_pages(list_servers_servers_get)
    hits = [s for s in servers if ref in (s["id"], s.get("name"))]
    if not hits:
        fail(f"no server {ref!r}")
    if len(hits) > 1:
        fail(f"several servers are called {ref!r}; use its id")
    return hits[0]


def wait_for(get: Callable[[], dict[str, Any]], want: Iterable[str], timeout: int) -> dict[str, Any]:
    want = set(want)
    deadline = time.monotonic() + timeout
    while True:
        item = get()
        status = item.get("status")
        if status in want:
            return item
        if status == "error":
            fail(f"failed: {item.get('error_reason') or 'error'}")
        if time.monotonic() > deadline:
            fail(f"still {status} after {timeout} s")
        time.sleep(5)


# --- account -----------------------------------------------------------------------------


@app.command()
def login(
    key: str = typer.Option(..., prompt="API key", hide_input=True, help="ic_ck_... from the console"),
) -> None:
    """Check an API key and store it in the OS keyring."""
    key = key.strip()
    os.environ[KEY_ENV] = key
    me = as_dict(call(me_me_get))
    import keyring

    keyring.set_password(KEYRING_SERVICE, KEYRING_USER, key)
    typer.echo(f"Logged in as {me['user']['name']} (key {me['key']['prefix']}, {me['key']['scope']}).")


@app.command()
def logout() -> None:
    """Remove the stored API key from the OS keyring."""
    import keyring
    from keyring.errors import PasswordDeleteError

    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_USER)
    except PasswordDeleteError:
        pass
    typer.echo("Logged out.")


@app.command()
def whoami() -> None:
    """The project, person and key behind your API key."""
    me = as_dict(call(me_me_get))
    show(
        me,
        [
            ("PROJECT", "project_id"),
            ("USER", lambda r: r["user"]["name"]),
            ("KEY", lambda r: r["key"]["prefix"]),
            ("SCOPE", lambda r: r["key"]["scope"]),
            ("EXPIRES", lambda r: r["key"]["expires_at"]),
        ],
    )


# --- catalog -----------------------------------------------------------------------------


@app.command("server-types")
def server_types() -> None:
    """Server types your project can launch."""
    rows = all_pages(list_server_types_server_types_get)
    show(
        rows,
        [
            ("NAME", "name"),
            ("GPU", lambda r: f"{r['gpu']['count']}x {r['gpu']['name']}" if r.get("gpu") else "CPU"),
            ("VCPUS", "vcpus"),
            ("RAM_GB", "ram_gb"),
            ("SITE", "site"),
            (
                "PRICE/H",
                lambda r: f"{r['price']['amount']} {r['price']['currency']}" if r.get("price") else None,
            ),
        ],
    )


@app.command()
def images(
    gpu: str | None = typer.Option(None, "--gpu", help="Only images for this GPU model, or none"),
) -> None:
    """Images you can launch from."""
    rows = all_pages(list_images_images_get)
    if gpu:
        rows = [r for r in rows if gpu.lower() in r.get("gpu_models", [])]
    show(
        rows,
        [
            ("NAME", "name"),
            ("ID", "id"),
            ("GPU_MODELS", "gpu_models"),
            ("MIN_DISK_GB", "min_disk_gb"),
            ("LOGIN", "login_user"),
        ],
    )


# --- SSH keys ----------------------------------------------------------------------------

KEY_COLUMNS = [("NAME", "name"), ("FINGERPRINT", "fingerprint")]


@ssh_keys_app.command("list")
def ssh_keys_list() -> None:
    """Your SSH keys."""
    show(all_pages(list_ssh_keys_ssh_keys_get), KEY_COLUMNS)


@ssh_keys_app.command("add")
def ssh_keys_add(
    name: str,
    public_key_file: typer.FileText = typer.Argument(..., help="Your .pub file"),
) -> None:
    """Add an SSH public key (OpenSSH format)."""
    text = public_key_file.read().strip()
    if "PRIVATE KEY" in text:
        fail("that's a private key: give the .pub file")
    key = call(create_ssh_key_ssh_keys_post, body=SshKeyCreate(name=name, public_key=text))
    show(as_dict(key), KEY_COLUMNS)


@ssh_keys_app.command("delete")
def ssh_keys_delete(name: str) -> None:
    """Remove one of your SSH keys."""
    call(delete_ssh_key_ssh_keys_name_delete, name=name)
    typer.echo(f"Deleted SSH key {name}.")


# --- servers -----------------------------------------------------------------------------

SERVER_COLUMNS = [
    ("NAME", "name"),
    ("ID", "id"),
    ("STATUS", "status"),
    ("TYPE", "server_type"),
    ("SITE", "site"),
    ("IP", lambda r: [a["ip"] for a in r.get("addresses") or []]),
]


def _server(server_id: str) -> dict[str, Any]:
    return as_dict(call(get_server_servers_server_id_get, server_id=server_id))


@servers_app.command("list")
def servers_list() -> None:
    """The project's servers, newest first."""
    show(all_pages(list_servers_servers_get), SERVER_COLUMNS)


@servers_app.command("show")
def servers_show(server: str) -> None:
    """One server, by name or id."""
    show(_server(find_server(server)["id"]), SERVER_COLUMNS + [("ERROR", "error_reason")])


@servers_app.command("create")
def servers_create(
    name: str,
    server_type: str = typer.Option(..., "--type", help="A server type's name (ic server-types)"),
    image: str = typer.Option(..., "--image", help="Image name or id (ic images)"),
    ssh_key: str = typer.Option(..., "--ssh-key", help="One of your SSH keys (ic ssh-keys list)"),
    disk_gb: int | None = typer.Option(None, "--disk-gb", help="System disk size (default 50)"),
    user_data: typer.FileText | None = typer.Option(None, "--user-data", help="cloud-init file"),
    keep_disk: bool = typer.Option(False, "--keep-disk", help="Keep the system disk when deleted"),
    wait: bool = typer.Option(False, "--wait", help="Wait until the server is active"),
    timeout: int = typer.Option(1200, "--timeout", help="Seconds to wait"),
    idempotency_key: str | None = typer.Option(None, "--idempotency-key", help="Default: random"),
) -> None:
    """Launch a server. Safe to retry with the same --idempotency-key."""
    body = ServerCreate(
        name=name,
        server_type=server_type,
        image=image,
        ssh_key=ssh_key,
        delete_disk_with_server=not keep_disk,
    )
    if disk_gb is not None:
        body.disk_gb = disk_gb
    if user_data is not None:
        body.user_data = user_data.read()
    key = idempotency_key or f"ic-cli-{uuid.uuid4()}"
    created = as_dict(call(create_server_servers_post, body=body, idempotency_key=key))
    if wait:
        created = wait_for(lambda: _server(created["id"]), {"active"}, timeout)
    show(created, SERVER_COLUMNS)


def _action(
    server: str,
    action: str,
    hard: bool = False,
    wait_status: str | None = None,
    wait: bool = False,
    timeout: int = 1200,
) -> None:
    sid = find_server(server)["id"]
    body = ServerAction(action=action)
    if hard:
        body.hard = True
    out = as_dict(call(server_action_servers_server_id_actions_post, server_id=sid, body=body))
    if wait and wait_status:
        out = wait_for(lambda: _server(sid), {wait_status}, timeout)
    show(out, SERVER_COLUMNS)


WAIT = typer.Option(False, "--wait", help="Wait until it's done")
TIMEOUT = typer.Option(1200, "--timeout", help="Seconds to wait")


@servers_app.command("start")
def servers_start(server: str, wait: bool = WAIT, timeout: int = TIMEOUT) -> None:
    """Start a stopped server."""
    _action(server, "start", wait_status="active", wait=wait, timeout=timeout)


@servers_app.command("stop")
def servers_stop(server: str, wait: bool = WAIT, timeout: int = TIMEOUT) -> None:
    """Stop a server (it keeps its GPU and stays billed; park to release it)."""
    _action(server, "stop", wait_status="stopped", wait=wait, timeout=timeout)


@servers_app.command("reboot")
def servers_reboot(
    server: str, hard: bool = typer.Option(False, "--hard"), wait: bool = WAIT, timeout: int = TIMEOUT
) -> None:
    """Reboot a server."""
    _action(server, "reboot", hard=hard, wait_status="active", wait=wait, timeout=timeout)


@servers_app.command("park")
def servers_park(server: str, wait: bool = WAIT, timeout: int = TIMEOUT) -> None:
    """Park a server: frees the GPU and stops GPU billing, keeps the disk."""
    _action(server, "park", wait_status="parked", wait=wait, timeout=timeout)


@servers_app.command("resume")
def servers_resume(server: str, wait: bool = WAIT, timeout: int = TIMEOUT) -> None:
    """Resume a parked server."""
    _action(server, "resume", wait_status="active", wait=wait, timeout=timeout)


@servers_app.command("delete")
def servers_delete(server: str, yes: bool = typer.Option(False, "--yes", "-y", help="Don't ask")) -> None:
    """Delete a server."""
    s = find_server(server)
    if not yes:
        typer.confirm(f"Delete server {s['name']} ({s['id']})?", abort=True)
    show(as_dict(call(delete_server_servers_server_id_delete, server_id=s["id"])), SERVER_COLUMNS)


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def ssh(
    ctx: typer.Context,
    server: str,
    identity: str | None = typer.Option(None, "-i", help="Private key file for ssh"),
    close: bool = typer.Option(False, "--close", help="Close SSH access instead"),
) -> None:
    """SSH into a server: opens access if needed, then runs ssh. Extra args go to ssh."""
    sid = find_server(server)["id"]
    if close:
        call(close_ssh_servers_server_id_ssh_delete, server_id=sid)
        typer.echo("SSH access closed.")
        return
    access = as_dict(call(get_ssh_servers_server_id_ssh_get, server_id=sid))
    if access.get("state") != "open":
        access = as_dict(call(open_ssh_servers_server_id_ssh_put, server_id=sid))
        typer.echo("SSH access opened; it can take up to a minute to answer.", err=True)
    argv = ["ssh", "-p", str(access["port"])]
    if identity:
        argv += ["-i", identity]
    argv += [*ctx.args, f"{access['user']}@{access['host']}"]
    if state.as_json:
        typer.echo(json.dumps({**access, "argv": argv}, indent=2))
        return
    exe = shutil.which("ssh")
    if not exe:
        fail("ssh isn't installed: " + " ".join(argv))
    os.execv(exe, argv)


# --- volumes and backups -----------------------------------------------------------------

VOLUME_COLUMNS = [
    ("NAME", "name"),
    ("ID", "id"),
    ("SIZE_GB", "size_gb"),
    ("STATUS", "status"),
    ("SITE", "site"),
    ("ATTACHED_TO", "attached_to"),
]


@volumes_app.command("list")
def volumes_list() -> None:
    """The project's volumes."""
    show(all_pages(list_volumes_volumes_get), VOLUME_COLUMNS)


@volumes_app.command("create")
def volumes_create(
    name: str,
    size_gb: int = typer.Option(..., "--size-gb"),
    site: str = typer.Option(..., "--site", help="Site id (see ic server-types)"),
) -> None:
    """Create an empty volume at a site."""
    body = VolumeCreate(name=name, size_gb=size_gb, site=site)
    out = call(create_volume_volumes_post, body=body, idempotency_key=f"ic-cli-{uuid.uuid4()}")
    show(as_dict(out), VOLUME_COLUMNS)


@volumes_app.command("delete")
def volumes_delete(volume_id: str, yes: bool = typer.Option(False, "--yes", "-y")) -> None:
    """Delete a volume (detach it first)."""
    if not yes:
        typer.confirm(f"Delete volume {volume_id}?", abort=True)
    show(as_dict(call(delete_volume_volumes_volume_id_delete, volume_id=volume_id)), VOLUME_COLUMNS)


@volumes_app.command("attach")
def volumes_attach(volume_id: str, server: str) -> None:
    """Attach a volume to a server at the same site."""
    sid = find_server(server)["id"]
    out = call(
        attach_volume_volumes_volume_id_attach_post, volume_id=volume_id, body=VolumeAttach(server_id=sid)
    )
    show(as_dict(out), VOLUME_COLUMNS)


@volumes_app.command("detach")
def volumes_detach(volume_id: str) -> None:
    """Detach a volume from its server."""
    show(as_dict(call(detach_volume_volumes_volume_id_detach_post, volume_id=volume_id)), VOLUME_COLUMNS)


@backups_app.command("list")
def backups_list(volume_id: str) -> None:
    """Backups of a volume."""
    rows = all_pages(list_backups_volumes_volume_id_backups_get, volume_id=volume_id)
    show(
        rows,
        [
            ("NAME", "name"),
            ("ID", "id"),
            ("STATUS", "status"),
            ("SIZE_GB", "size_gb"),
            ("INCREMENTAL", "incremental"),
            ("TAKEN", "data_timestamp"),
        ],
    )


@backups_app.command("restore")
def backups_restore(backup_id: str, name: str | None = typer.Option(None, "--name")) -> None:
    """Restore a backup into a new volume on the backup's site."""
    body = BackupRestore()
    if name:
        body.name = name
    out = call(
        restore_backup_backups_backup_id_restore_post,
        backup_id=backup_id,
        body=body,
        idempotency_key=f"ic-cli-{uuid.uuid4()}",
    )
    show(as_dict(out), VOLUME_COLUMNS)


# --- usage -------------------------------------------------------------------------------


@app.command()
def usage(month: str | None = typer.Option(None, "--month", help="YYYY-MM; default this month")) -> None:
    """GPU-hours and charges for a month."""
    u = as_dict(call(get_usage_usage_get, month=month) if month else call(get_usage_usage_get))
    if state.as_json:
        show(u, [])
        return
    show(
        u["servers"],
        [
            ("SERVER", "name"),
            ("TYPE", "server_type"),
            ("GPU", "gpu_model"),
            ("GPU_HOURS", "gpu_hours"),
            ("DELETED", "deleted"),
        ],
    )
    typer.echo(f"\nTotal {u['total_gpu_hours']} GPU-hours in {u['month']}.")
    spend = u.get("spend")
    if spend:
        typer.echo(
            f"Charges: {spend['amount']} {spend['currency']} (rated until {spend.get('rated_until')})."
        )


def run() -> None:
    try:
        app()
    except KeyboardInterrupt:
        sys.exit(130)
