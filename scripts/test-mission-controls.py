"""Exercise the real control boundary and persisted evidence in isolated workspaces."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".codex" / "hooks"))
import mission_guard as guard
import oxygen_site_gate as hook
import tool_use_gate
sys.path.insert(0, str(ROOT / ".agents/skills/wordpress-oxygen-qa/scripts"))
from compare_visuals import compare_visuals


class MissionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="octacom-controls-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        (self.workspace / ".octacom").mkdir()
        self.mission = {"format": 1, "mission_id": "fixture", "authorization_source": "test instruction",
            "scope": "post 42 only", "completion_criteria": ["verify"],
            "target": {"site_url": "https://fixture.invalid/subsite", "final_domain": "fixture.invalid",
                "builder_version": "6.0.0", "connector": "mcp__fixture__", "consistency": "serial_observed"},
            "sources": [{"id": "business", "reference": "fixture", "version": "1"}],
            "figma": {"required": False, "references": []}, "max_observation_age_seconds": 120,
            "resources": {"post:42": {"owner": "coordinator", "operations": ["oxygen_edit_post"]},
                "global:settings": {"owner": "coordinator", "operations": ["oxygen_set_global_settings"]}}}
        self.save_mission()
        self.ready()

    def save_mission(self):
        (self.workspace / ".octacom" / "mission.json").write_text(json.dumps(self.mission), encoding="utf-8")

    def db(self):
        _, fingerprint = guard.load_mission(self.workspace)
        return guard.state(self.workspace, fingerprint)

    def event(self, kind, operation, *, arguments=None, response=None, call="call-1", connector="mcp__fixture__", session="session-1"):
        return {"cwd": str(self.workspace), "session_id": session, "hook_event_name": kind,
            "tool_name": connector + operation, "tool_input": arguments or {"post_id": 42},
            "tool_response": response, "tool_use_id": call}

    def ready(self):
        hook.handle(self.event("PostToolUse", "oxygen_site_info", response={"structuredContent": {
            "site_url": "https://fixture.invalid/subsite/", "builder_version": "6.0.0"}}))
        hook.handle(self.event("PostToolUse", "oxygen_get_post_tree", response={"structuredContent": {"id": 1, "children": []}}))
        with self.db() as db:
            db.execute("INSERT OR REPLACE INTO bindings VALUES ('session-1','coordinator')")
            db.execute("INSERT OR REPLACE INTO expected SELECT resource,revision FROM snapshots")

    def edit(self, **extra):
        return hook.handle(self.event("PreToolUse", "oxygen_edit_post", **extra))

    def assertDenied(self, result):
        self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")

    def evidence(self, kind="single_article", identity="proof-1", resource="post:42"):
        path = self.workspace / "qa.txt"
        path.write_text("fixture evidence", encoding="utf-8")
        with self.db() as db:
            revision = db.execute("SELECT revision FROM snapshots WHERE resource=?", (resource,)).fetchone()[0]
            manifest = {"id": identity, "kind": kind, "resource": resource, "observed_revision": revision,
                "mission_digest": guard.digest(self.mission),
                "epoch": guard.epoch(db, resource), "reviewer": "fixture-reviewer", "review_source": "fixture receipt",
                "open_differences": [], "files": [{"path": "qa.txt", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}]}
            guard.register_evidence(self.workspace, db, self.mission, manifest)

    def test_positive_consumes_snapshot_and_invalidates_before_effect(self):
        self.evidence()
        self.assertEqual(self.edit(), {})
        with self.db() as db:
            self.assertEqual(db.execute("SELECT status FROM attempts").fetchone()[0], "pending")
            self.assertEqual(db.execute("SELECT status FROM evidence").fetchone()[0], "stale")
            self.assertEqual(db.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0], 0)
        self.assertDenied(self.edit(call="call-2"))

    def test_wrong_domain_path_version_and_connector(self):
        for url, version in [("https://other.invalid/subsite", "6.0.0"), ("https://fixture.invalid", "6.0.0"), ("https://fixture.invalid/subsite", "5.0"), ("https://fixture.invalid/subsite", "6.0.1")]:
            self.ready()
            hook.handle(self.event("PostToolUse", "oxygen_site_info", response={"structuredContent": {"site_url": url, "builder_version": version}}))
            self.assertDenied(self.edit())
        self.ready()
        self.assertDenied(self.edit(connector="mcp__other__"))

    def test_failed_empty_and_text_only_reads_revoke_previous_success(self):
        for response in [{"isError": True, "structuredContent": {"site_url": "https://fixture.invalid/subsite", "builder_version": "6.0.0"}},
                {"isError": "true", "content": [{"type": "text", "text": "OK"}]},
                {"content": [{"type": "text", "text": "ERROR unauthorized"}]},
                {"structuredContent": {"success": False}}]:
            self.ready()
            hook.handle(self.event("PostToolUse", "oxygen_site_info", response=response))
            self.assertDenied(self.edit())

    def test_read_without_result_never_reuses_previous_site(self):
        hook.handle(self.event("PreToolUse", "oxygen_site_info"))
        self.assertDenied(self.edit())

    def test_unknown_mutation_and_wrong_object_or_owner(self):
        self.assertDenied(hook.handle(self.event("PreToolUse", "oxygen_update_unreviewed")))
        self.assertDenied(self.edit(arguments={"post_id": 43}))
        with self.db() as db:
            db.execute("UPDATE bindings SET owner='page-agent'")
        self.assertDenied(self.edit())

    def test_absent_annotations_conflict_and_atomic_mode(self):
        for update in [{"unresolved_conflicts": ["business"]}, {"target": dict(self.mission["target"], consistency="atomic_revision")},
            {"figma": {"required": True, "annotations_status": "missing", "references": [{"id": "frame", "version": "1", "file_key": "F", "node_id": "1:1", "states": ["rest"]}]}}]:
            previous = copy.deepcopy(self.mission)
            self.mission.update(update)
            self.save_mission()
            self.ready()
            self.assertDenied(self.edit())
            self.mission = previous

    def test_snapshot_mismatch_failed_tree_and_expiry(self):
        with self.db() as db:
            db.execute("UPDATE expected SET revision='other'")
        self.assertDenied(self.edit())
        self.ready()
        hook.handle(self.event("PostToolUse", "oxygen_get_post_tree", response={"structuredContent": {"message": "unauthorized"}}))
        self.assertDenied(self.edit())
        self.ready()
        with self.db() as db:
            db.execute("UPDATE snapshots SET observed=0")
        self.assertDenied(self.edit())

    def test_unknown_global_results_never_become_snapshots(self):
        for operation in ("oxygen_get_global_settings", "oxygen_get_css_variables", "oxygen_get_css_selectors"):
            resource = hook.SNAPSHOT_READS[operation]
            self.mission["resources"][resource] = {"owner": "coordinator", "operations": ["oxygen_set_global_settings"]}
        self.save_mission()
        self.ready()
        for operation in ("oxygen_get_global_settings", "oxygen_get_css_variables", "oxygen_get_css_selectors"):
            result = hook.handle(self.event("PostToolUse", operation, arguments={"include_properties": True},
                response={"structuredContent": {"message": "unauthorized"}}))
            self.assertIn("Snapshot refusé", result.get("systemMessage", ""))
            with self.db() as db:
                self.assertIsNone(db.execute("SELECT revision FROM snapshots WHERE resource=?",
                    (hook.SNAPSHOT_READS[operation],)).fetchone())

    def test_explicit_other_post_and_partial_global_reads_are_refused(self):
        result = hook.handle(self.event("PostToolUse", "oxygen_get_post_tree", response={
            "structuredContent": {"post_id": 99, "tree": {"id": 1, "children": []}}}))
        self.assertIn("Snapshot refusé", result.get("systemMessage", ""))
        self.assertDenied(self.edit())
        self.mission["resources"]["global:selectors"] = {"owner": "coordinator", "operations": ["oxygen_delete_css_selectors"]}
        self.mission["resources"]["global:variables"] = {"owner": "coordinator", "operations": ["oxygen_insert_css_variables"]}
        self.save_mission()
        self.ready()
        for operation, arguments, response in [
            ("oxygen_get_css_selectors", {"include_properties": False}, {"selectors": []}),
            ("oxygen_get_css_selectors", {"include_properties": True, "search": "card"}, {"selectors": []}),
            ("oxygen_get_css_variables", {"ids": ["one"]}, {"variables": []})]:
            result = hook.handle(self.event("PostToolUse", operation, arguments=arguments,
                response={"structuredContent": response}))
            self.assertIn("Snapshot refusé", result.get("systemMessage", ""))
        for operation, arguments, response in [
            ("oxygen_get_css_selectors", {"include_properties": True}, {"selectors": []}),
            ("oxygen_get_css_variables", {}, {"variables": []})]:
            result = hook.handle(self.event("PostToolUse", operation, arguments=arguments,
                response={"structuredContent": response}))
            self.assertIn("snapshot observé", result["hookSpecificOutput"]["additionalContext"])

    def test_changed_mission_revokes_bindings_and_observations(self):
        self.evidence()
        self.mission["sources"][0]["version"] = "2"
        self.save_mission()
        self.assertDenied(self.edit())
        with self.db() as db:
            self.assertEqual(db.execute("SELECT status FROM evidence").fetchone()[0], "stale")

    def test_failure_keeps_unknown_and_success_does_not_restore_proofs(self):
        self.assertEqual(self.edit(), {})
        hook.handle(self.event("PostToolUse", "oxygen_edit_post", response={"isError": True, "structuredContent": {"success": False}}))
        with self.db() as db:
            self.assertEqual(db.execute("SELECT status FROM attempts").fetchone()[0], "unknown")
            self.assertEqual(db.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0], 0)

    def test_missing_result_is_closed_as_unknown_by_native_turn_boundary(self):
        self.assertEqual(self.edit(), {})
        self.ready()
        self.assertDenied(self.edit(call="unsafe-retry"))
        event = {"hook_event_name": "Stop", "cwd": str(self.workspace), "session_id": "other-session"}
        self.assertEqual(guard.finish_unobserved_attempts(event), 0)
        event["session_id"] = "session-1"
        self.assertEqual(tool_use_gate.handle(event), {})
        with self.db() as db:
            self.assertEqual(db.execute("SELECT status FROM attempts").fetchone()[0], "unknown")
        self.assertEqual(guard.finish_unobserved_attempts(event), 0)

    def test_inflight_reads_and_proofs_cannot_certify_pre_effect_state(self):
        self.assertEqual(self.edit(), {})
        result = hook.handle(self.event("PostToolUse", "oxygen_get_post_tree",
            response={"structuredContent": {"id": 1, "children": []}}))
        self.assertIn("Snapshot refusé", result.get("systemMessage", ""))
        with self.db() as db:
            self.assertIsNone(db.execute("SELECT revision FROM snapshots WHERE resource='post:42'").fetchone())
            self.assertFalse(guard.evidence_check(db, self.mission)["mechanical_pass"])
            manifest = {"mission_digest": guard.digest(self.mission), "resource": "post:42"}
            with self.assertRaisesRegex(ValueError, "Mutation en cours"):
                guard.register_evidence(self.workspace, db, self.mission, manifest)
        hook.handle(self.event("PostToolUse", "oxygen_edit_post", response={"structuredContent": {"success": True}}))
        self.ready()
        for kind in guard.REQUIRED_DELIVERY:
            self.evidence(kind, kind)
        with self.db() as db:
            self.assertTrue(guard.evidence_check(db, self.mission)["mechanical_pass"])

    def test_historical_attempt_schema_migrates_to_unknown_without_success_assertion(self):
        with self.db() as db:
            db.execute("DROP TABLE attempts")
            db.execute("CREATE TABLE attempts (call TEXT PRIMARY KEY,resource TEXT,status TEXT,argument_digest TEXT)")
            db.execute("INSERT INTO attempts VALUES ('old','post:42','pending','old-arguments')")
        with self.db() as db:
            row = db.execute("SELECT * FROM attempts WHERE call='old'").fetchone()
            self.assertEqual(row["status"], "unknown")
            self.assertIsNone(row["session"])

    def test_result_drift_invalidates_actual_object_and_never_completes_expected_action(self):
        self.mission["resources"]["post:43"] = {"owner": "coordinator", "operations": ["oxygen_edit_post"]}
        self.save_mission()
        self.ready()
        hook.handle(self.event("PostToolUse", "oxygen_get_post_tree", arguments={"post_id": 43},
            response={"structuredContent": {"id": 1, "children": []}}))
        for kind in guard.REQUIRED_DELIVERY:
            self.evidence(kind, kind, resource="post:43")
        with self.db() as db:
            self.assertTrue(guard.evidence_check(db, self.mission)["mechanical_pass"])
        self.assertEqual(self.edit(call="drift"), {})
        hook.handle(self.event("PostToolUse", "oxygen_edit_post", call="drift", arguments={"post_id": 43},
            response={"structuredContent": {"success": True}}))
        with self.db() as db:
            self.assertFalse(guard.evidence_check(db, self.mission)["mechanical_pass"])
            self.assertEqual(db.execute("SELECT status FROM attempts WHERE call='drift'").fetchone()[0], "unknown")
            self.assertTrue(all(row[0] == "stale" for row in db.execute("SELECT status FROM evidence")))
        self.ready()
        self.assertEqual(self.edit(call="identity-drift"), {})
        hook.handle(self.event("PostToolUse", "oxygen_edit_post", call="identity-drift", session="other-session",
            response={"structuredContent": {"success": True}}))
        with self.db() as db:
            self.assertEqual(db.execute("SELECT status FROM attempts WHERE call='identity-drift'").fetchone()[0], "unknown")

    def test_concurrent_same_resource_only_one_attempt_is_admitted(self):
        results = []
        threads = [threading.Thread(target=lambda i=i: results.append(self.edit(call=f"call-{i}"))) for i in range(2)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        self.assertEqual(results.count({}), 1)

    def test_global_mutation_invalidates_all_known_evidence(self):
        self.evidence()
        hook.handle(self.event("PostToolUse", "oxygen_get_global_settings", response={"structuredContent": {"settings": {"color": "blue"}}}))
        with self.db() as db:
            db.execute("INSERT OR REPLACE INTO expected SELECT resource,revision FROM snapshots")
        result = hook.handle(self.event("PreToolUse", "oxygen_set_global_settings", arguments={"settings": {"color": "red"}}))
        self.assertEqual(result, {})
        with self.db() as db:
            self.assertEqual(db.execute("SELECT status FROM evidence").fetchone()[0], "stale")

    def test_delivery_requires_all_three_invariants_and_cannot_certify_visual(self):
        self.evidence()
        with self.db() as db:
            result = guard.evidence_check(db, self.mission)
            self.assertFalse(result["mechanical_pass"])
            self.assertFalse(result["visual_certification"])
        self.evidence("octacom_credit", "credit")
        self.evidence("404", "404")
        with self.db() as db:
            self.assertTrue(guard.evidence_check(db, self.mission)["mechanical_pass"])
        (self.workspace / "qa.txt").write_text("changed", encoding="utf-8")
        with self.db() as db:
            self.assertFalse(guard.evidence_check(db, self.mission)["mechanical_pass"])

    def test_builder_reload_assertion_becomes_stale_after_edit(self):
        with self.db() as db:
            row = db.execute("SELECT revision FROM snapshots WHERE resource='post:42'").fetchone()
            db.execute("INSERT INTO builder VALUES ('post:42',0,?,'fixture')", (row[0],))
        self.edit()
        with self.db() as db:
            self.assertTrue(any("Builder périmé" in p for p in guard.evidence_check(db, self.mission)["problems"]))

    def test_two_workspaces_do_not_share_state(self):
        with tempfile.TemporaryDirectory() as other:
            other = Path(other)
            (other / ".octacom").mkdir()
            (other / ".octacom" / "mission.json").write_text(json.dumps(self.mission), encoding="utf-8")
            _, fingerprint = guard.load_mission(other)
            with guard.state(other, fingerprint) as db:
                self.assertEqual(db.execute("SELECT COUNT(*) FROM sites").fetchone()[0], 0)

    def test_stale_manifest_is_refused_even_when_tree_pixels_could_be_identical(self):
        self.evidence()
        with self.db() as db:
            manifest = json.loads(db.execute("SELECT payload FROM evidence").fetchone()[0])
            manifest["id"] = "new-proof"
            manifest["mission_digest"] = "old-mission"
            with self.assertRaisesRegex(ValueError, "Version de fiche"):
                guard.register_evidence(self.workspace, db, self.mission, manifest)

    @unittest.skipUnless(shutil.which("magick"), "ImageMagick required for real image integration")
    def test_real_comparison_provenance_is_bound_and_invalidated_after_attempt(self):
        self.mission["figma"] = {"required": True, "annotations_status": "reviewed",
            "annotations_evidence": "fixture annotation review", "references": [{"id": "home",
                "file_key": "F", "node_id": "1:1", "version": "figma-v1", "states": ["rest"]}]}
        self.mission["resources"]["post:42"]["front_url"] = "https://fixture.invalid/subsite/home"
        self.save_mission()
        self.ready()
        images = [self.workspace / "figma.png", self.workspace / "front.png"]
        for image in images:
            subprocess.run(["magick", "-size", "24x32", "xc:white", str(image)], check=True,
                capture_output=True)
        with self.db() as db:
            revision = db.execute("SELECT revision FROM snapshots WHERE resource='post:42'").fetchone()[0]
            provenance = {"mission_digest": guard.digest(self.mission), "resource": "post:42",
                "observed_revision": revision, "epoch": guard.epoch(db, "post:42"),
                "figma_reference": "home", "figma_version": "figma-v1", "state": "rest",
                "front_url": "https://fixture.invalid/subsite/home",
                "viewport": {"width": 24, "height": 32, "dpr": 1, "zoom": 100}}
        output = self.workspace / "comparison"
        comparison = compare_visuals(*images, output, provenance=provenance)
        pieces = list(images) + [Path(value["path"]) for value in comparison["outputs"].values()]
        pieces.append(output / "comparison.json")
        manifest = provenance | {"id": "visual", "kind": "visual", "reviewer": "fixture",
            "review_source": "fixture images only", "open_differences": [],
            "comparison": "comparison/comparison.json", "files": [{"path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in pieces]}
        with self.db() as db:
            wrong = copy.deepcopy(manifest)
            wrong["viewport"]["width"] = 48
            with self.assertRaisesRegex(ValueError, "provenance"):
                guard.register_evidence(self.workspace, db, self.mission, wrong)
            guard.register_evidence(self.workspace, db, self.mission, manifest)
        for kind in guard.REQUIRED_DELIVERY:
            self.evidence(kind, kind)
        with self.db() as db:
            result = guard.evidence_check(db, self.mission)
            self.assertTrue(result["mechanical_pass"])
            self.assertFalse(result["visual_certification"])
        self.assertEqual(self.edit(), {})
        with self.db() as db:
            self.assertFalse(guard.evidence_check(db, self.mission)["mechanical_pass"])
            self.assertEqual(db.execute("SELECT status FROM evidence WHERE id='visual'").fetchone()[0], "stale")


if __name__ == "__main__":
    unittest.main()
