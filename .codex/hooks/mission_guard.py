"""Workspace mission, observed revisions and evidence checks. Not a security broker."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlsplit

REQUIRED_DELIVERY = ("octacom_credit", "single_article", "404")


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False).encode()).hexdigest()


def read_json(path: Path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Champ JSON dupliqué : {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def site_identity(url: str) -> str:
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username or parts.password or parts.query or parts.fragment:
        raise ValueError("SITE_URL doit identifier exactement un site HTTP(S), sans secret ni query")
    host = parts.hostname.lower()
    port = parts.port
    authority = host if port is None or (parts.scheme, port) in {("https", 443), ("http", 80)} else f"{host}:{port}"
    return f"{parts.scheme}://{authority}{parts.path.rstrip('/')}"


def local_root(workspace: Path) -> Path:
    workspace = workspace.absolute()
    root = workspace / ".octacom"
    if root.exists() and (root.is_symlink() or root.resolve().parent != workspace.resolve() or getattr(root.stat(), "st_file_attributes", 0) & 1024):
        raise ValueError(".octacom doit être un dossier réel propre au workspace")
    root.mkdir(exist_ok=True)
    for name in ("mission.json", "state.sqlite3"):
        child = root / name
        if child.exists() and child.resolve().parent != root.resolve():
            raise ValueError(f"État partagé interdit : {name}")
    return root


def load_mission(workspace: Path) -> tuple[dict, str]:
    mission = read_json(local_root(workspace) / "mission.json")
    if not isinstance(mission, dict) or mission.get("format") != 1:
        raise ValueError("Fiche mission format 1 requise")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", mission.get("mission_id", "")):
        raise ValueError("mission_id invalide")
    for name in ("authorization_source", "scope", "completion_criteria"):
        if not mission.get(name):
            raise ValueError(f"Champ mission requis : {name}")
    if "REPLACE" in json.dumps(mission):
        raise ValueError("Fiche exemple incomplète : remplacer par les faits confirmés")
    target = mission.get("target", {})
    target["site_url"] = site_identity(target.get("site_url", ""))
    if not re.fullmatch(r"(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}", target.get("final_domain", "")):
        raise ValueError("Domaine final confirmé requis, distinct de SITE_URL")
    if not re.fullmatch(r"mcp__[A-Za-z0-9_]+_", target.get("connector", "")):
        raise ValueError("Préfixe MCP exact requis, terminé par _")
    if not re.fullmatch(r"6\.[0-9]+(?:\.[0-9]+)?(?:[-+][A-Za-z0-9.-]+)?", target.get("builder_version", "")):
        raise ValueError("Version Oxygen 6 exacte requise")
    if target.get("consistency") not in {"serial_observed", "atomic_revision"}:
        raise ValueError("Mode de révision explicite requis")
    if type(mission.get("max_observation_age_seconds")) is not int or not 1 <= mission["max_observation_age_seconds"] <= 300:
        raise ValueError("Fenêtre de fraîcheur requise, entre 1 et 300 secondes")
    sources = mission.get("sources")
    if not isinstance(sources, list) or not sources or any(not isinstance(s, dict) or not s.get("id") or not s.get("reference") or not s.get("version") for s in sources):
        raise ValueError("Sources confirmées et versionnées requises")
    if len({s["id"] for s in sources}) != len(sources):
        raise ValueError("Source dupliquée")
    resources = mission.get("resources")
    if not isinstance(resources, dict) or not resources:
        raise ValueError("Objets autorisés requis")
    for key, resource in resources.items():
        if not re.fullmatch(r"(?:post:[1-9][0-9]*|global:[a-z_]+|create:[a-z_]+)", key) or not isinstance(resource, dict) or not resource.get("owner"):
            raise ValueError("Objet et propriétaire exacts requis")
        operations = resource.get("operations")
        if not isinstance(operations, list) or not operations or any(not isinstance(op, str) or not op.startswith("oxygen_") for op in operations):
            raise ValueError("Opérations exactes requises par objet")
    figma = mission.get("figma", {})
    if not isinstance(figma, dict) or type(figma.get("required")) is not bool:
        raise ValueError("Applicabilité Figma explicite requise")
    refs = figma.get("references", [])
    if not isinstance(refs, list) or any(not isinstance(r, dict) or not r.get("id") or not r.get("file_key") or not r.get("node_id") or not r.get("version") or not r.get("states") for r in refs):
        raise ValueError("Références Figma complètes requises")
    if figma["required"] and not refs:
        raise ValueError("Références Figma absentes")
    return mission, digest(mission)


@contextmanager
def state(workspace: Path, mission_digest: str):
    connection = sqlite3.connect(local_root(workspace) / "state.sqlite3", timeout=3)
    connection.row_factory = sqlite3.Row
    try:
        connection.executescript("""
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS bindings (session TEXT PRIMARY KEY, owner TEXT);
        CREATE TABLE IF NOT EXISTS sites (session TEXT PRIMARY KEY, connector TEXT, url TEXT, version TEXT, observed REAL);
        CREATE TABLE IF NOT EXISTS snapshots (resource TEXT PRIMARY KEY, revision TEXT, session TEXT, observed REAL);
        CREATE TABLE IF NOT EXISTS expected (resource TEXT PRIMARY KEY, revision TEXT);
        CREATE TABLE IF NOT EXISTS epochs (resource TEXT PRIMARY KEY, value INTEGER);
        CREATE TABLE IF NOT EXISTS attempts (call TEXT PRIMARY KEY, resource TEXT, status TEXT, argument_digest TEXT, session TEXT);
        CREATE TABLE IF NOT EXISTS evidence (id TEXT PRIMARY KEY, resource TEXT, epoch INTEGER, revision TEXT, payload TEXT, status TEXT);
        CREATE TABLE IF NOT EXISTS builder (resource TEXT PRIMARY KEY, epoch INTEGER, revision TEXT, source TEXT);
        """)
        connection.execute("BEGIN IMMEDIATE")
        if "session" not in {row[1] for row in connection.execute("PRAGMA table_info(attempts)")}:
            connection.execute("ALTER TABLE attempts ADD COLUMN session TEXT")
            connection.execute("UPDATE attempts SET status='unknown' WHERE status='pending'")
        old = connection.execute("SELECT value FROM meta WHERE key='mission'").fetchone()
        if old is None or old[0] != mission_digest:
            for table in ("sites", "snapshots", "expected", "bindings", "builder"):
                connection.execute(f"DELETE FROM {table}")
            connection.execute("UPDATE evidence SET status='stale'")
            connection.execute("UPDATE attempts SET status='unknown' WHERE status='pending'")
            connection.execute("INSERT OR REPLACE INTO meta VALUES ('mission',?)", (mission_digest,))
        yield connection
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
    finally:
        connection.close()


def epoch(db, resource: str) -> int:
    row = db.execute("SELECT value FROM epochs WHERE resource=?", (resource,)).fetchone()
    return row[0] if row else 0


def invalidate(db, resource: str):
    resources = [r[0] for r in db.execute("SELECT resource FROM epochs")] if resource.startswith("global:") or resource.startswith("create:") else [resource]
    for key in set(resources + [resource]):
        db.execute("INSERT OR REPLACE INTO epochs VALUES (?,?)", (key, epoch(db, key) + 1))
    if resource.startswith(("global:", "create:")):
        db.execute("UPDATE evidence SET status='stale'")
        db.execute("DELETE FROM snapshots")
        db.execute("DELETE FROM expected")
    else:
        db.execute("UPDATE evidence SET status='stale' WHERE resource=?", (resource,))
        db.execute("DELETE FROM snapshots WHERE resource=?", (resource,))
        db.execute("DELETE FROM expected WHERE resource=?", (resource,))


def response_data(response) -> dict:
    if not isinstance(response, dict) or ("isError" in response and response["isError"] is not False):
        raise ValueError("Résultat MCP absent ou échoué")
    data = response.get("structuredContent")
    if not isinstance(data, dict) or not data:
        content = response.get("content", [])
        objects = []
        for item in content if isinstance(content, list) else []:
            if isinstance(item, dict) and item.get("type") == "text":
                try:
                    candidate = json.loads(item.get("text", ""))
                    if isinstance(candidate, dict) and candidate:
                        objects.append(candidate)
                except (ValueError, TypeError):
                    pass
        if len(objects) != 1:
            raise ValueError("Objet JSON de résultat non ambigu requis")
        data = objects[0]
    if data.get("success") is False or data.get("error") or data.get("isError"):
        raise ValueError("Résultat d'outil échoué")
    return data


def mutation_check(db, mission, session: str, connector: str, operation: str, resource: str, call: str, arguments: dict):
    target = mission["target"]
    if target["connector"] != connector:
        raise ValueError("Mauvais connecteur MCP")
    site = db.execute("SELECT * FROM sites WHERE session=?", (session,)).fetchone()
    now = time.time()
    age = mission["max_observation_age_seconds"]
    if not site or now - site["observed"] > age or site["connector"] != connector or site["url"] != target["site_url"] or site["version"] != target["builder_version"]:
        raise ValueError("Relire oxygen_site_info : identité/version absente, différente ou périmée")
    if target["consistency"] == "atomic_revision":
        raise ValueError("Révision atomique indisponible : ces outils ne proposent aucun CAS serveur")
    if mission.get("unresolved_conflicts"):
        raise ValueError("Conflit de sources non résolu")
    annotations = mission.get("figma", {})
    if annotations.get("required") and (annotations.get("annotations_status") != "reviewed" or not annotations.get("annotations_evidence")):
        raise ValueError("FIGMA_ANNOTATIONS_REVIEWED non établi")
    scope = mission["resources"].get(resource)
    binding = db.execute("SELECT owner FROM bindings WHERE session=?", (session,)).fetchone()
    if not scope or operation not in scope["operations"] or not binding or binding[0] != scope["owner"]:
        raise ValueError("Objet, opération ou propriétaire hors périmètre confirmé")
    if not isinstance(call, str) or not call or db.execute("SELECT 1 FROM attempts WHERE call=?", (call,)).fetchone():
        raise ValueError("Identité d'appel absente ou déjà consommée")
    if pending_overlap(db, resource):
        raise ValueError("Tentative encore en cours sans résultat : attendre sa clôture et réconcilier")
    if not resource.startswith("create:"):
        snapshot = db.execute("SELECT * FROM snapshots WHERE resource=?", (resource,)).fetchone()
        expected = db.execute("SELECT revision FROM expected WHERE resource=?", (resource,)).fetchone()
        if not snapshot or snapshot["session"] != session or now - snapshot["observed"] > age or not expected or snapshot["revision"] != expected[0]:
            raise ValueError("Révision observée absente/périmée ou différente de la révision attendue")
    invalidate(db, resource)
    # The historical column name is retained, but the digest binds the whole action.
    db.execute("INSERT INTO attempts (call,resource,status,argument_digest,session) VALUES (?,?,?,?,?)",
        (call, resource, "pending", action_digest(session, connector, operation, resource, arguments), session))


def action_digest(session: str, connector: str, operation: str, resource: str, arguments: dict) -> str:
    return digest({"session": session, "connector": connector, "operation": operation,
        "resource": resource, "arguments": arguments})


def pending_overlap(db, resource: str) -> bool:
    return any(row[0] == resource or row[0].startswith(("global:", "create:"))
        or resource.startswith(("global:", "create:"))
        for row in db.execute("SELECT resource FROM attempts WHERE status='pending'"))


def finish_unobserved_attempts(event: dict) -> int:
    if event.get("hook_event_name") not in {"Stop", "UserPromptSubmit", "SessionStart"}:
        return 0
    workspace = Path(event.get("cwd", ""))
    session = event.get("session_id")
    if not workspace.is_absolute() or not isinstance(session, str) or not session or not (workspace / ".octacom/mission.json").is_file():
        return 0
    _, mission_digest = load_mission(workspace)
    with state(workspace, mission_digest) as db:
        for row in db.execute("SELECT resource FROM attempts WHERE status='pending' AND session=?", (session,)).fetchall():
            invalidate(db, row[0])
        return db.execute("UPDATE attempts SET status='unknown' WHERE status='pending' AND session=?", (session,)).rowcount


def evidence_check(db, mission) -> dict:
    problems = []
    if db.execute("SELECT 1 FROM attempts WHERE status='pending'").fetchone():
        problems.append("Mutation encore en cours : résultat et lectures après effet requis avant livraison")
    current = []
    for row in db.execute("SELECT * FROM evidence"):
        payload = json.loads(row["payload"])
        snapshot = db.execute("SELECT revision FROM snapshots WHERE resource=?", (row["resource"],)).fetchone()
        observation = db.execute("SELECT * FROM snapshots WHERE resource=?", (row["resource"],)).fetchone()
        valid = row["status"] == "recorded" and row["epoch"] == epoch(db, row["resource"]) and observation and row["revision"] == observation["revision"] and time.time() - observation["observed"] <= mission["max_observation_age_seconds"]
        for file in payload.get("files", []):
            path = Path(file["path"])
            valid = valid and path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == file["sha256"]
        if valid:
            current.append(payload)
        else:
            problems.append(f"Preuve périmée ou altérée : {row['id']}")
    for kind in REQUIRED_DELIVERY:
        if not any(p.get("kind") == kind for p in current):
            problems.append(f"Preuve obligatoire manquante : {kind}")
    for source in mission.get("figma", {}).get("references", []):
        for frame_state in source.get("states", []):
            if not any(p.get("kind") == "visual" and p.get("figma_reference") == source["id"] and p.get("figma_version") == source["version"] and p.get("state") == frame_state for p in current):
                problems.append(f"Comparaison actuelle manquante : {source['id']} / {frame_state}")
    for resource in mission["resources"]:
        opened = db.execute("SELECT * FROM builder WHERE resource=?", (resource,)).fetchone()
        snapshot = db.execute("SELECT revision FROM snapshots WHERE resource=?", (resource,)).fetchone()
        if opened and (opened["epoch"] != epoch(db, resource) or not snapshot or opened["revision"] != snapshot[0]):
            problems.append(f"Builder périmé : {resource}, recharger et vérifier")
    if mission.get("unresolved_conflicts"):
        problems.append("Conflit de sources non résolu")
    return {"mechanical_pass": not problems, "problems": problems,
        "visual_certification": False, "review_assertions_only": True,
        "consistency": mission["target"]["consistency"], "remote_cas": False}


def register_evidence(workspace: Path, db, mission, manifest: dict):
    if manifest.get("mission_digest") != digest(mission):
        raise ValueError("Version de fiche différente de la capture/revue")
    resource = manifest.get("resource")
    if resource not in mission["resources"]:
        raise ValueError("Objet de preuve hors mission")
    if pending_overlap(db, resource):
        raise ValueError("Mutation en cours : aucune preuve enregistrable avant résultat et nouvelle lecture")
    snapshot = db.execute("SELECT revision FROM snapshots WHERE resource=?", (resource,)).fetchone()
    if not snapshot or manifest.get("observed_revision") != snapshot[0] or manifest.get("epoch") != epoch(db, resource):
        raise ValueError("Preuve sur révision/epoch périmée")
    kind = manifest.get("kind")
    if kind not in (*REQUIRED_DELIVERY, "visual", "technical") or not manifest.get("reviewer") or not manifest.get("review_source") or manifest.get("open_differences") != []:
        raise ValueError("Revue précise et aucun écart ouvert requis")
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError("Pièces de preuve absentes")
    for file in files:
        path = (workspace / file["path"]).resolve()
        if not path.is_relative_to(workspace.resolve()) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != file.get("sha256"):
            raise ValueError("Pièce absente, hors workspace ou empreinte différente")
        file["path"] = str(path)
    if kind == "visual":
        reference = next((s for s in mission.get("figma", {}).get("references", []) if s["id"] == manifest.get("figma_reference")), None)
        if not reference or manifest.get("figma_version") != reference["version"] or manifest.get("state") not in reference["states"]:
            raise ValueError("Référence Figma version/état hors mission")
        if site_identity(manifest.get("front_url", "")) != site_identity(mission["resources"][resource].get("front_url", "")):
            raise ValueError("URL front différente")
        viewport = manifest.get("viewport", {})
        if not all(isinstance(viewport.get(k), (int, float)) and not isinstance(viewport[k], bool) and viewport[k] > 0 for k in ("width", "height", "dpr", "zoom")) or viewport["zoom"] != 100:
            raise ValueError("Viewport exact/DPR/zoom requis")
        comparison_path = (workspace / manifest.get("comparison", "")).resolve()
        if str(comparison_path) not in {f["path"] for f in files}:
            raise ValueError("comparison.json doit être une pièce empreintée")
        comparison = read_json(comparison_path)
        provenance = {key: manifest.get(key) for key in ("mission_digest", "resource", "observed_revision", "epoch", "figma_reference", "figma_version", "state", "front_url", "viewport")}
        if comparison.get("provenance") != provenance:
            raise ValueError("Comparaison sans provenance identique à la preuve")
        declared = {f["path"]: f["sha256"] for f in files}
        for image in list(comparison.get("inputs", {}).values()) + list(comparison.get("outputs", {}).values()):
            if declared.get(str(Path(image["path"]).resolve())) != image["sha256"]:
                raise ValueError("Toutes captures et comparaisons empreintées requises")
        if set(comparison.get("inputs", {})) != {"figma", "front"} or set(comparison.get("outputs", {})) != {"side_by_side", "overlay", "difference"}:
            raise ValueError("Supports de comparaison complets requis")
    identity = manifest.get("id", "")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", identity):
        raise ValueError("Identifiant preuve invalide")
    db.execute("INSERT INTO evidence VALUES (?,?,?,?,?,?)", (identity, resource, manifest["epoch"], snapshot[0], json.dumps(manifest), "recorded"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("mission-check")
    commands.add_parser("status")
    commands.add_parser("delivery-check")
    bind = commands.add_parser("bind-session")
    bind.add_argument("--session", required=True)
    bind.add_argument("--owner", required=True)
    accept = commands.add_parser("accept-snapshot")
    accept.add_argument("--resource", required=True)
    accept.add_argument("--revision", required=True)
    builder = commands.add_parser("builder-reloaded")
    builder.add_argument("--resource", required=True)
    builder.add_argument("--source", required=True)
    evidence = commands.add_parser("register-evidence")
    evidence.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    workspace = args.workspace.absolute()
    try:
        mission, mission_digest = load_mission(workspace)
        with state(workspace, mission_digest) as db:
            if args.command == "bind-session":
                if args.owner not in {r["owner"] for r in mission["resources"].values()}:
                    raise ValueError("Propriétaire hors fiche")
                db.execute("INSERT OR REPLACE INTO bindings VALUES (?,?)", (args.session, args.owner))
            elif args.command == "accept-snapshot":
                if pending_overlap(db, args.resource):
                    raise ValueError("Mutation en cours : attendre la clôture puis relire avant acceptation")
                row = db.execute("SELECT revision FROM snapshots WHERE resource=?", (args.resource,)).fetchone()
                if not row or row[0] != args.revision:
                    raise ValueError("Accepter seulement l'empreinte réellement observée")
                db.execute("INSERT OR REPLACE INTO expected VALUES (?,?)", (args.resource, args.revision))
            elif args.command == "builder-reloaded":
                row = db.execute("SELECT revision FROM snapshots WHERE resource=?", (args.resource,)).fetchone()
                if not row:
                    raise ValueError("Lecture actuelle de l'objet requise avant confirmation de reload")
                db.execute("INSERT OR REPLACE INTO builder VALUES (?,?,?,?)", (args.resource, epoch(db, args.resource), row[0], args.source))
            elif args.command == "register-evidence":
                register_evidence(workspace, db, mission, read_json(args.manifest))
            result = {"mission_id": mission["mission_id"], "mission_digest": mission_digest,
                "snapshots": [dict(r) | {"epoch": epoch(db, r["resource"])} for r in db.execute("SELECT * FROM snapshots")],
                "delivery": evidence_check(db, mission)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if args.command == "delivery-check" and not result["delivery"]["mechanical_pass"] else 0
    except (OSError, ValueError, TypeError, KeyError, sqlite3.Error) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
