"""登记规则的单元测试。示例数据都是虚构的。"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.obd.engine import (  # noqa: E402
    allocate_id,
    classify_counterexample,
    dual_report,
    is_reserved_test_id,
    load_policy,
    next_glyph_id,
    pilot_errors,
    pointer_errors,
    publication_pilot_logs,
    qualification_for,
    review_errors,
    transcription_errors,
    validate_repository,
)
from scripts.download_datasets import decision  # noqa: E402
from tools.interface import build_machine_suggestion, validate_model_output  # noqa: E402


def _now() -> datetime:
    return datetime(2026, 10, 2, tzinfo=timezone.utc)


def _entry(**overrides):
    base = {
        "record_id": "EX-T1",
        "glyph_id": "OBD-000001",
        "catalog_ref": "示例字编EX-1",
        "period_group": "unknown",
        "transcription": "丁未",
        "damage_level": "complete",
        "source_citation": "示例论著列为未识",
        "entered_by": "example-a",
        "note": "",
    }
    base.update(overrides)
    return base


class RepositoryTests(unittest.TestCase):
    def test_repository_passes(self):
        errors = validate_repository(ROOT, now=_now())
        self.assertEqual(errors, [], "\n".join(errors))

    def test_drill_is_validated_but_not_published(self):
        drill = ROOT / "pilot" / "_drill" / "OBD-900001.md"
        self.assertEqual(pilot_errors(drill), [])
        published = publication_pilot_logs(ROOT)
        self.assertTrue(all("_drill" not in path.parts for path in published))
        self.assertNotIn(drill.resolve(), [path.resolve() for path in published])

    def test_stats_exclude_drill(self):
        import scripts.stats as stats

        self.assertEqual(stats.main(), 0)


class IdTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_policy(ROOT)

    def test_skips_reserved_range(self):
        ledger = {
            "allocations": [
                {
                    "glyph_id": "OBD-900000",
                    "issued_to": "a",
                    "issued_at": "2026-10-02T00:00:00Z",
                    "state": "used",
                    "source_note": "x",
                    "description": "x",
                    "duplicate_checked_by": "b",
                }
            ]
        }
        self.assertEqual(next_glyph_id(ledger, self.policy), "OBD-900100")
        self.assertTrue(is_reserved_test_id("OBD-900001", self.policy))
        self.assertFalse(is_reserved_test_id("OBD-900100", self.policy))

    def test_pending_cap_and_no_reuse_after_abandon(self):
        ledger = {"allocations": []}
        for index in range(5):
            allocate_id(ledger, "person", f"d{index}", "来源", _now(), self.policy)
        with self.assertRaises(ValueError):
            allocate_id(ledger, "person", "more", "来源", _now(), self.policy)
        old = _now() - timedelta(days=31)
        ledger["allocations"][0]["issued_at"] = old.strftime("%Y-%m-%dT%H:%M:%SZ")
        issued = {row["glyph_id"] for row in ledger["allocations"]}
        row = allocate_id(ledger, "person", "after", "来源", _now(), self.policy)
        self.assertEqual(ledger["allocations"][0]["state"], "abandoned")
        self.assertNotIn(row["glyph_id"], issued)
        self.assertNotIn(row["glyph_id"], {f"OBD-{i:06d}" for i in range(900001, 900100)})


class PilotTests(unittest.TestCase):
    def test_empty_scope_blocks_hypothesis(self):
        text = (ROOT / "pilot" / "_TEMPLATE.md").read_text(encoding="utf-8")
        text = text.replace("证据不足暂不结论", "候选假说", 1)
        errors = pilot_errors(ROOT / "pilot" / "_TEMPLATE.md", text)
        self.assertTrue(any("线索待查" in item for item in errors))

    def test_login_required_source_caps_conclusion(self):
        text = (ROOT / "pilot" / "_TEMPLATE.md").read_text(encoding="utf-8")
        text = text.replace("conclusion_level: \"证据不足暂不结论\"", "conclusion_level: \"候选假说\"", 1)
        text = text.replace("corpus_scope: \"\"", "corpus_scope: \"示例字编；检索日期 2026-10-02；缀合库查询日期 2026-10-02\"", 1)
        text = text.replace(
            "evidence: []",
            "\n".join(
                [
                    "evidence:",
                    "  - catalog_ref: \"示例字编EX-9\"",
                    "    quotation: \"示例辞，非真实\"",
                    "    source: \"需登录的示例库\"",
                    "    page: \"1\"",
                    "    checker: \"example\"",
                    "    login_required: \"是\"",
                ]
            ),
            1,
        )
        errors = pilot_errors(ROOT / "pilot" / "_TEMPLATE.md", text)
        self.assertTrue(any("个人线索" in item for item in errors))
        text = text.replace("conclusion_level: \"候选假说\"", "conclusion_level: \"线索待查\"", 1)
        errors = pilot_errors(ROOT / "pilot" / "_TEMPLATE.md", text)
        self.assertFalse(any("个人线索" in item for item in errors))

    def test_scope_requires_rejoin_date(self):
        text = (ROOT / "pilot" / "_TEMPLATE.md").read_text(encoding="utf-8")
        text = text.replace('corpus_scope: ""', 'corpus_scope: "示例字编；检索日期 2026-10-02"', 1)
        errors = pilot_errors(ROOT / "pilot" / "_TEMPLATE.md", text)
        self.assertTrue(any("缀合库" in item for item in errors))

    def test_reserved_id_cannot_leave_drill(self):
        text = (ROOT / "pilot" / "_drill" / "OBD-900001.md").read_text(encoding="utf-8")
        errors = pilot_errors(Path("pilot/OBD-900001.md"), text)
        self.assertTrue(any("测试编号" in item for item in errors))


class TranscriptionTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_policy(ROOT)

    def test_restoration_cannot_be_complete(self):
        errors = transcription_errors(
            _entry(transcription="【丁】", damage_level="complete"),
            [],
            self.policy,
            "t",
        )
        self.assertTrue(errors)

    def test_severe_requires_marker_and_brackets_pair(self):
        self.assertEqual(
            transcription_errors(
                _entry(transcription="丁□…", damage_level="severe"),
                [],
                self.policy,
                "t",
            ),
            [],
        )
        errors = transcription_errors(
            _entry(transcription="丁【未", damage_level="minor"),
            [],
            self.policy,
            "t",
        )
        self.assertTrue(any("括号" in item for item in errors))

    def test_dual_conflict_is_not_merged(self):
        left = _entry(transcription="丁未", entered_by="a")
        right = _entry(transcription="丁□", damage_level="minor", entered_by="b")
        report = dual_report(left, right, [])
        self.assertFalse(report["consistent"])
        self.assertFalse(report["auto_merge"])
        self.assertTrue(any(item["field"] == "transcription" for item in report["conflicts"]))


class ReviewAndCandidateTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_policy(ROOT)
        self.record = {
            "glyph_id": "OBD-000001",
            "status_tier": "widely_undeciphered",
            "review_status": "待议",
            "disclaimer": "",
            "proposer": "proposer",
            "verification": {"locked": False},
            "community_reviewers": [],
            "counterevidence": {"open": False, "items": []},
            "evidence": [],
            "priority_votes": [],
        }

    def test_self_fill_cannot_raise_status(self):
        record = copy.deepcopy(self.record)
        record["review_status"] = "可接受的候选"
        record["claimed"] = {"attestation_count": 99}
        errors = review_errors(record, self.policy, _now())
        self.assertTrue(any("不生效" in item for item in errors))

    def test_expert_tier_is_vacant(self):
        record = copy.deepcopy(self.record)
        record["review_status"] = "专家认可"
        record["verification"] = {
            "locked": True,
            "reviewer": "other",
            "checked_against_catalog": True,
            "attestation_count": 9,
            "damage_level": "complete",
            "all_attestations_read": True,
        }
        errors = review_errors(record, self.policy, _now())
        self.assertTrue(any("暂空置" in item for item in errors))

    def test_candidate_cannot_be_evidence(self):
        document = json.loads(
            (ROOT / "tools" / "examples" / "obsd-placeholder.json").read_text(encoding="utf-8")
        )
        self.assertEqual(validate_model_output(document), [])
        broken = copy.deepcopy(document)
        broken["status"] = "accepted"
        broken["human_review"] = {"reviewer": "a", "note": "x", "edited_at": "2026-10-02"}
        errors = validate_model_output(broken)
        self.assertTrue(any("machine-suggestion" in item or "human_review" in item for item in errors))
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                build_machine_suggestion(
                    target_glyph_id="OBD-000001",
                    input_ref="rubbing.png",
                    model={"name": "OBSD", "version": "unknown", "weights_source": "x"},
                    training_data={"name": "x", "license": "unknown"},
                    log_path=Path(tmp) / "calls.jsonl",
                )

    def test_unformed_counterexample(self):
        self.assertEqual(
            classify_counterexample({"kind": "reading_fails_in_context", "catalog_ref": "x"}),
            "unformed",
        )

    def test_image_and_unknown_domain(self):
        allow = {"doi.org"}
        self.assertTrue(pointer_errors({"image_pointer": "plate.png"}, allow, "g"))
        self.assertTrue(pointer_errors({"image_pointer": "https://example.com/a"}, allow, "g"))
        self.assertEqual(pointer_errors({"image_pointer": "待查原书"}, allow, "g"), [])


class OtherTests(unittest.TestCase):
    def test_download_policy(self):
        self.assertEqual(decision("hust-obc"), "external-noncommercial")
        self.assertEqual(decision("obc306"), "refuse")
        self.assertEqual(decision("oracle-50k"), "refuse")

    def test_qualification_is_not_a_ranking(self):
        policy = load_policy(ROOT)
        pairs = [
            {"left_by": "a", "right_by": "b", "consistent": True},
            {"left_by": "a", "right_by": "c", "consistent": True},
            {"left_by": "a", "right_by": "d", "consistent": True},
        ]
        result = qualification_for(pairs, "a", policy)
        self.assertTrue(result["qualified_reviewer"])
        self.assertIn("不是准确率", result["note"])
        self.assertNotIn("rank", result)

    def test_roadmap_mentions_reminder_only(self):
        text = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("经验设定，待校准", text)
        self.assertIn("范围过期，需复查", text)
        self.assertIn("不自动降档", text)
        for item in ("重复提案检索", "投票资格自动判定", "串通抽查", "译文同步"):
            self.assertIn(item, text)


if __name__ == "__main__":
    unittest.main()
