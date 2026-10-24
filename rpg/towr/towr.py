import json
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Self

from rpg.dice import dice_prob


@dataclass(frozen=True, slots=True)
class CharacterStats:
    # WS
    melee: tuple[int, int]
    defence: tuple[int, int]
    # BS
    shooting: tuple[int, int]
    throwing: tuple[int, int]
    # S
    brawn: tuple[int, int]
    toil: tuple[int, int]
    # T
    survival: tuple[int, int]
    endurance: tuple[int, int]
    # I
    awareness: tuple[int, int]
    dexterity: tuple[int, int]
    # AG
    athletics: tuple[int, int]
    stealth: tuple[int, int]
    # RE
    willpower: tuple[int, int]
    recall: tuple[int, int]
    # FEL
    leadership: tuple[int, int]
    charm: tuple[int, int]

    name: str = ""

    def report(self, successes=1, include_values=True) -> str:
        lines = [f"Character: {self.name}"] if self.name else []
        lines += [f"Successes={successes}"]
        probs = []

        body_data = []
        max_label_len = 0

        for field in fields(self):
            if field.name == "name":
                continue

            n_dice, threshold = getattr(self, field.name)
            try:
                prob = dice_prob(n_dice, threshold, successes)
            except ValueError:
                prob_str = "N/A".rjust(7)
            else:
                probs.append(prob)
                prob_str = f"{prob:>7.2%}"

            field_name = (
                f"{field.name.title()} ({n_dice}/{threshold}):" if include_values
                else f"{field.name.title()}:"
            )

            max_label_len = max(max_label_len, len(field_name))
            body_data.append((field_name, prob_str))

        # Append aligned fields to lines
        for label, val in body_data:
            lines.append(f"{label.ljust(max_label_len)} {val}")

        # Align the average line to match
        avg = sum(probs) / len(probs) if probs else 0
        avg_label = "AVG:".ljust(max_label_len)
        lines.append(f"{avg_label} {avg:>7.2%}")

        return "\n".join(lines)

    @staticmethod
    def _parse_data(data: dict) -> tuple[dict, dict, str]:
        stats, skills = data.get("stats"), data.get("skills")
        if not (isinstance(stats, dict) and isinstance(skills, dict)):
            raise ValueError("Invalid data, must contain both 'stats' and 'skills' dictionaries")
        return stats, skills, data.get("name", "")

    @classmethod
    def from_json(cls, data: dict) -> Self:
        stats, skills, name = cls._parse_data(data)

        doubled_stats = []
        for stat in stats.values():
            doubled_stats += [stat, stat]

        return cls(*zip(doubled_stats, skills.values()), name=name)

    @classmethod
    def from_file(cls, path: str | Path) -> Self:
        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        if not (
            isinstance(data, list)
            and len(data) == 1
            and isinstance(data[0], dict)
        ):
            raise ValueError(
                f"Invalid contents of TOWR character stats JSON file: {path.as_posix()}")
        return cls.from_json(data[0])

