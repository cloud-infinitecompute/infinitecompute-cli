"""ic against a mocked API (httpx MockTransport): requests sent and output shown."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import httpx
import pytest
from typer.testing import CliRunner

from infinitecompute import cli

BASE = "https://api.test/api/public/v1"
SERVER = {
    "id": "srv-1",
    "name": "train",
    "status": "active",
    "error_reason": None,
    "server_type": "gpu-x",
    "image_id": "img-1",
    "ssh_key": "laptop",
    "site": {"id": "site-a", "name": "Site A"},
    "addresses": [{"network": "net", "ip": "10.0.0.5", "version": 4}],
    "volume_ids": ["vol-boot"],
    "created_at": "2026-10-28T00:00:00Z",
    "updated_at": None,
}


class FakeApi:
    """Routes (method, path) to a handler; records every request."""

    def __init__(self) -> None:
        self.routes: dict[tuple[str, str], Callable[[httpx.Request], httpx.Response]] = {}
        self.seen: list[httpx.Request] = []

    def on(self, method: str, path: str, status: int = 200, body: Any = None) -> None:
        self.routes[(method, path)] = lambda req: httpx.Response(status, json=body)

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.seen.append(request)
        path = request.url.path.replace("/api/public/v1", "")
        handler = self.routes.get((request.method, path))
        if handler is None:
            return httpx.Response(
                404, json={"error": {"code": "not_found", "message": "Not found.", "request_id": "req-x"}}
            )
        return handler(request)

    def last(self, method: str, path: str) -> httpx.Request:
        return [r for r in self.seen if r.method == method and r.url.path.endswith(path)][-1]


@pytest.fixture
def api(monkeypatch):
    fake = FakeApi()
    monkeypatch.setenv(cli.KEY_ENV, "ic_ck_abc123def456_" + "s" * 43)
    monkeypatch.setattr(cli.state, "transport", httpx.MockTransport(fake))
    return fake


def run(*args: str):
    result = CliRunner().invoke(cli.app, ["--api-url", BASE, *args])
    return result


def page(*items: Any, nxt: Any = None) -> dict[str, Any]:
    return {"data": list(items), "next_cursor": nxt}


def test_key_is_sent_as_bearer(api):
    api.on(
        "GET",
        "/me",
        body={
            "project_id": "p1",
            "user": {"id": "u1", "name": "you"},
            "key": {"id": "k", "prefix": "ic_ck_k", "scope": "read", "expires_at": "2027-01-01T00:00:00Z"},
        },
    )
    out = run("whoami")
    assert out.exit_code == 0, out.output
    assert "ic_ck_k" in out.output
    assert api.seen[0].headers["authorization"].startswith("Bearer ic_ck_abc123def456_")


def test_no_key_is_a_clear_error(monkeypatch):
    monkeypatch.delenv(cli.KEY_ENV, raising=False)
    monkeypatch.setattr(cli, "KEYRING_SERVICE", "infinitecompute-test-nonexistent")
    out = run("whoami")
    assert out.exit_code == 1 and "ic login" in out.output


def test_api_errors_show_message_and_request_id(api):
    api.on(
        "GET",
        "/servers",
        status=403,
        body={
            "error": {
                "code": "permission_denied",
                "message": "The API isn't enabled for this project yet.",
                "request_id": "req-42",
            }
        },
    )
    out = run("servers", "list")
    assert out.exit_code == 1
    assert "isn't enabled" in out.output and "req-42" in out.output


def test_lists_follow_every_page(api):
    calls = []

    def servers(req: httpx.Request) -> httpx.Response:
        calls.append(req.url.params.get("cursor"))
        if req.url.params.get("cursor") is None:
            return httpx.Response(200, json=page(SERVER, nxt="c2"))
        return httpx.Response(200, json=page(dict(SERVER, id="srv-2", name="eval")))

    api.routes[("GET", "/servers")] = servers
    out = run("--json", "servers", "list")
    assert out.exit_code == 0, out.output
    assert [s["id"] for s in json.loads(out.output)] == ["srv-1", "srv-2"]
    assert calls == [None, "c2"]


def test_table_output(api):
    api.on("GET", "/servers", body=page(SERVER))
    out = run("servers", "list")
    assert out.exit_code == 0
    header, row = out.output.splitlines()[:2]
    assert header.split()[:3] == ["NAME", "ID", "STATUS"]
    assert "train" in row and "Site A" in row and "10.0.0.5" in row


def test_create_sends_an_idempotency_key_and_waits(api, monkeypatch):
    monkeypatch.setattr(cli.time, "sleep", lambda s: None)
    api.on("POST", "/servers", status=202, body=dict(SERVER, status="building"))
    states = iter(["building", "active"])
    api.routes[("GET", "/servers/srv-1")] = lambda req: httpx.Response(
        200, json=dict(SERVER, status=next(states))
    )
    out = run(
        "--json",
        "servers",
        "create",
        "train",
        "--type",
        "gpu-x",
        "--image",
        "img-1",
        "--ssh-key",
        "laptop",
        "--wait",
    )
    assert out.exit_code == 0, out.output
    req = api.last("POST", "/servers")
    assert req.headers["idempotency-key"].startswith("ic-cli-")
    assert json.loads(req.content) == {
        "name": "train",
        "server_type": "gpu-x",
        "image": "img-1",
        "ssh_key": "laptop",
        "delete_disk_with_server": True,
    }
    assert json.loads(out.output)["status"] == "active"


def test_create_with_options(api, tmp_path):
    ud = tmp_path / "init.yaml"
    ud.write_text("#cloud-config\n")
    api.on("POST", "/servers", status=202, body=SERVER)
    run(
        "servers",
        "create",
        "t",
        "--type",
        "x",
        "--image",
        "i",
        "--ssh-key",
        "k",
        "--disk-gb",
        "80",
        "--keep-disk",
        "--user-data",
        str(ud),
        "--idempotency-key",
        "mine",
    )
    req = api.last("POST", "/servers")
    body = json.loads(req.content)
    assert (body["disk_gb"], body["delete_disk_with_server"], body["user_data"]) == (
        80,
        False,
        "#cloud-config\n",
    )
    assert req.headers["idempotency-key"] == "mine"


@pytest.mark.parametrize(
    "command,action",
    [("start", "start"), ("stop", "stop"), ("park", "park"), ("resume", "resume"), ("reboot", "reboot")],
)
def test_actions_resolve_the_name(api, command, action):
    api.on("GET", "/servers", body=page(SERVER))
    api.on("POST", "/servers/srv-1/actions", status=202, body=dict(SERVER, status="busy"))
    out = run("servers", command, "train")
    assert out.exit_code == 0, out.output
    sent = json.loads(api.last("POST", "/actions").content)
    assert sent["action"] == action and not sent.get("hard")


def test_hard_reboot(api):
    api.on("GET", "/servers", body=page(SERVER))
    api.on("POST", "/servers/srv-1/actions", status=202, body=SERVER)
    run("servers", "reboot", "train", "--hard")
    assert json.loads(api.last("POST", "/actions").content)["hard"] is True


def test_ambiguous_name(api):
    api.on("GET", "/servers", body=page(SERVER, dict(SERVER, id="srv-2")))
    out = run("servers", "show", "train")
    assert out.exit_code == 1 and "use its id" in out.output


def test_delete_asks_unless_yes(api):
    api.on("GET", "/servers", body=page(SERVER))
    api.on("DELETE", "/servers/srv-1", status=202, body=dict(SERVER, status="deleting"))
    out = CliRunner().invoke(cli.app, ["--api-url", BASE, "servers", "delete", "train"], input="n\n")
    assert out.exit_code != 0 and not [r for r in api.seen if r.method == "DELETE"]
    assert run("servers", "delete", "train", "-y").exit_code == 0
    assert api.last("DELETE", "/servers/srv-1")


def test_ssh_opens_access_then_execs_ssh(api, monkeypatch):
    api.on("GET", "/servers", body=page(SERVER))
    api.on(
        "GET",
        "/servers/srv-1/ssh",
        body={"state": "closed", "host": None, "port": None, "user": None, "command": None},
    )
    api.on(
        "PUT",
        "/servers/srv-1/ssh",
        body={"state": "open", "host": "203.0.113.9", "port": 21000, "user": "ubuntu", "command": "ssh ..."},
    )
    ran = {}
    monkeypatch.setattr(cli.shutil, "which", lambda name: "/usr/bin/ssh")
    monkeypatch.setattr(cli.os, "execv", lambda exe, argv: ran.update(exe=exe, argv=argv))
    out = run("ssh", "train", "-i", "~/.ssh/k", "-L", "8888:localhost:8888")
    assert out.exit_code == 0, out.output
    assert ran["argv"] == [
        "ssh",
        "-p",
        "21000",
        "-i",
        "~/.ssh/k",
        "-L",
        "8888:localhost:8888",
        "ubuntu@203.0.113.9",
    ]
    assert api.last("PUT", "/ssh")


def test_ssh_key_add_refuses_a_private_key(api, tmp_path):
    f = tmp_path / "id"
    f.write_text("-----BEGIN OPENSSH PRIVATE KEY-----\n...")
    out = run("ssh-keys", "add", "laptop", str(f))
    assert out.exit_code == 1 and "private key" in out.output and not api.seen


def test_volume_create_and_attach(api):
    vol = {
        "id": "v1",
        "name": "data",
        "size_gb": 10,
        "status": "creating",
        "site": {"id": "site-a", "name": "Site A"},
        "bootable": False,
        "attached_to": [],
        "image_id": None,
        "created_at": None,
    }
    api.on("POST", "/volumes", status=202, body=vol)
    api.on("GET", "/servers", body=page(SERVER))
    api.on("POST", "/volumes/v1/attach", status=202, body=dict(vol, status="busy"))
    assert run("volumes", "create", "data", "--size-gb", "10", "--site", "site-a").exit_code == 0
    req = api.last("POST", "/volumes")
    assert json.loads(req.content) == {"name": "data", "size_gb": 10, "site": "site-a"}
    assert req.headers["idempotency-key"]
    assert run("volumes", "attach", "v1", "train").exit_code == 0
    assert json.loads(api.last("POST", "/attach").content) == {"server_id": "srv-1"}


def test_usage(api):
    api.on(
        "GET",
        "/usage",
        body={
            "month": "2026-09",
            "start": "2026-09-01T00:00:00Z",
            "end": "2026-10-01T00:00:00Z",
            "generated_at": "2026-10-28T00:00:00Z",
            "total_gpu_hours": 10.0,
            "servers": [
                {
                    "server_id": "s",
                    "name": "train",
                    "server_type": "x",
                    "gpu_model": "GPU",
                    "gpu_count": 1,
                    "sku": "gpu:x",
                    "gpu_hours": 10.0,
                    "deleted": False,
                }
            ],
            "spend": None,
        },
    )
    out = run("usage", "--month", "2026-09")
    assert out.exit_code == 0, out.output
    assert "Total 10.0 GPU-hours in 2026-09" in out.output
    assert api.last("GET", "/usage").url.params["month"] == "2026-09"


def test_unreachable_api(monkeypatch):
    def boom(request):
        raise httpx.ConnectError("refused")

    monkeypatch.setenv(cli.KEY_ENV, "ic_ck_x")
    monkeypatch.setattr(cli.state, "transport", httpx.MockTransport(boom))
    out = run("servers", "list")
    assert out.exit_code == 1 and "can't reach" in out.output
