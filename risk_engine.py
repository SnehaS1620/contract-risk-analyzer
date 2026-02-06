RISK_RULES = {
    "Penalty": ["penalty", "fine", "liquidated damages"],
    "Indemnity": ["indemnify", "hold harmless"],
    "Unilateral Termination": ["terminate at any time", "without notice"],
    "Auto Renewal": ["automatically renew", "auto renew"],
    "Non Compete": ["non compete", "shall not engage", "similar business"],
    "Arbitration": ["arbitration", "arbitrator"],
    "IP Transfer": ["assign all intellectual property", "ownership transfers"]
}

SEVERITY = {
    "Penalty": "High",
    "Indemnity": "High",
    "Unilateral Termination": "High",
    "IP Transfer": "High",
    "Auto Renewal": "Medium",
    "Non Compete": "Medium",
    "Arbitration": "Low"
}


def analyze_clause(text):
    found = []
    lower = text.lower()

    for risk, keywords in RISK_RULES.items():
        for word in keywords:
            if word in lower:
                found.append(risk)

    if not found:
        return "Low", []

    order = ["Low", "Medium", "High"]
    level = max([SEVERITY[r] for r in found], key=lambda x: order.index(x))

    return level, found
