MANDATORY_FIELDS = [
    "policyNumber",
    "policyholderName",
    "effectiveDates",
    "incidentDate",
    "incidentTime",
    "location",
    "description",
    "claimant",
    "thirdParties",
    "contactDetails",
    "assetType",
    "assetId",
    "estimatedDamage",
    "claimType",
    "attachments",
    "initialEstimate",
]


def validate(fields: dict):
    missing = [name for name in MANDATORY_FIELDS if fields.get(name) in (None, "", [])]

    inconsistencies = []

    damage = fields.get("estimatedDamage")
    initial = fields.get("initialEstimate")

    if damage is not None and initial is not None and damage != initial:
        inconsistencies.append(
            f"Estimated damage (₹{damage:,.0f}) and initial estimate "
            f"(₹{initial:,.0f}) are inconsistent."
        )

    return missing, inconsistencies
