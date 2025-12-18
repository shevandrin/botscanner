from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import json
import csv
import shutil
from typing import Optional


class OutcomeWriter:
    """
    It organizes botstanner outcomes.
    """

    def __init__(self, url: str, base_dir: Optional[Path] = None):
        self.base_dir = Path(base_dir or "results")
        self.url = url
        self.timestamp = datetime.now()
        self.domain = urlparse(url).netloc.replace("www.", "")

        self.scan_dir = (
            self.base_dir
            / f"{self.domain}__{self.timestamp.strftime('%Y-%m-%dT%H-%M-%S')}"
        )

        # Fixed folders (by contract)
        self.dom_dir = self.scan_dir / "dom"
        self.screenshots_dir = self.scan_dir / "screenshots"
        self.result_dir = self.scan_dir / "result"
        self.stats_path = self.scan_dir / "stats.csv"

        # Internal registry for artefacts.json
        self._artefacts = {
            "dom": {},
            "screenshots": {}
        }

        self._create_structure()


    def _create_structure(self):
        for d in [
            self.scan_dir,
            self.dom_dir,
            self.screenshots_dir,
            self.result_dir,
        ]:
            d.mkdir(parents=True, exist_ok=True)

    
    def save_dom(self, name: str, html: str):
        path = self.dom_dir / f"{name}.txt"
        path.write_text(html, encoding="utf-8")

        self._artefacts["dom"][name] = str(
            path.relative_to(self.scan_dir)
        )

    def save_screenshot(self, name: str, src: Path):
        dst = self.screenshots_dir / f"{name}.png"
        shutil.copy(src, dst)

        self._artefacts["screenshots"][name] = str(
            dst.relative_to(self.scan_dir)
        )

    def save_json(self, name: str, records: list[dict]):
        """
        Save structured JSON data into result/ folder.
        Optionally enrich it with paths to DOM artefacts.

        Args:
            name: file name without .json (e.g. 's1_chatbot_anchors')
            data: JSON-serializable dictionary
            dom_refs: mapping logical_key -> dom artefact name
                    e.g. { "best_candidate": "s1_candidate_0" }
        """

        if not isinstance(records, list):
            raise TypeError("save_json expects a list of dictionaries")
    

        path = self.result_dir / f"{name}.json"
        path.write_text(
            json.dumps(records, indent=2),
            encoding="utf-8"
        )


    def finalize(self, outcome: dict):
        self._write_outcome(outcome)
        self._write_artefacts()
        self._write_stats(outcome)



    def _write_outcome(self, outcome: dict):
        path = self.result_dir / "outcome.json"
        path.write_text(
            json.dumps(outcome, indent=2),
            encoding="utf-8"
        )


    def _write_artefacts(self):
        path = self.result_dir / "artefacts.json"
        path.write_text(
            json.dumps(self._artefacts, indent=2),
            encoding="utf-8"
        )


    def _write_stats(self, outcome: dict):
        row = {
            "domain": self.domain,
            "timestamp": self.timestamp.isoformat(),
            "detected": outcome.get("chatbot_detected"),
            "position": outcome.get("position"),
            "confidence": outcome.get("confidence"),
            "widget_type": outcome.get("widget_type"),
        }

        write_header = not self.stats_path.exists()

        with self.stats_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(row)