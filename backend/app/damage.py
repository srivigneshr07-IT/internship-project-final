from typing import Any

DAMAGE_KEYWORDS = {
    "bumper": 12000,
    "scratch": 8000,
    "dent": 10000,
    "windshield": 15000,
    "door": 9000,
    "paint": 7000,
    "headlight": 8500,
    "tail light": 8500,
    "wheel": 9000,
    "engine": 25000,
    "radiator": 18000,
}

SEVERITY_MULTIPLIER = {
    "minor": 0.75,
    "light": 0.75,
    "moderate": 1.0,
    "major": 1.5,
    "severe": 2.0,
}


def normalize_text(text: str) -> str:
    return text.lower().strip()


def extract_damage_signals(description: str) -> list[dict[str, Any]]:
    normalized = normalize_text(description)
    items: list[dict[str, Any]] = []

    if not normalized:
        return items

    for keyword, base_cost in DAMAGE_KEYWORDS.items():
        if keyword in normalized:
            severity = "moderate"
            for level in SEVERITY_MULTIPLIER:
                if f"{level} {keyword}" in normalized or f"{keyword} is {level}" in normalized:
                    severity = level
                    break
            items.append({
                "component": keyword,
                "severity": severity,
                "base_cost": base_cost,
                "multiplier": SEVERITY_MULTIPLIER.get(severity, 1.0),
            })

    if not items and normalized:
        items.append({
            "component": "unspecified damage",
            "severity": "moderate",
            "base_cost": 10000,
            "multiplier": 1.0,
        })

    return items


def estimate_damage_cost(description: str) -> dict[str, Any]:
    items = extract_damage_signals(description)
    total_cost = sum(item["base_cost"] * item["multiplier"] for item in items)

    return {
        "damage_description": description.strip(),
        "damage_items": items,
        "damage_cost": round(total_cost, 2),
    }
