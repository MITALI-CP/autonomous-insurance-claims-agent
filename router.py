INVESTIGATION_KEYWORDS = ["fraud", "inconsistent", "staged"]


def route_claim(fields: dict, missing: list[str], inconsistencies: list[str]):
    description = (fields.get("description") or "").lower()

    # Highest priority: suspicious claim
    if any(word in description for word in INVESTIGATION_KEYWORDS):
        return (
            "Investigation Flag",
            "The claim description contains a keyword associated with potential fraud or inconsistency."
        )

    # Incomplete claims need human review
    if missing:
        return (
            "Manual review",
            "One or more mandatory fields are missing: " + ", ".join(missing) + "."
        )

    # Injury claims go to a specialist
    if (fields.get("claimType") or "").strip().lower() == "injury":
        return (
            "Specialist Queue",
            "The claim type is injury, so it is routed to the specialist queue."
        )

    # Low-value complete claims can be fast-tracked
    damage = fields.get("estimatedDamage")
    if damage is not None and damage < 25000:
        reason = (
            f"Estimated damage is ₹{damage:,.0f}, which is below ₹25,000, "
            "and all mandatory fields are present."
        )
        if inconsistencies:
            reason += " An estimate inconsistency was also detected."
        return "Fast-track", reason

    # Complete but above threshold
    reason = "All mandatory fields are present, but estimated damage is not below ₹25,000."
    if inconsistencies:
        reason += " " + " ".join(inconsistencies)
    return "Manual review", reason
