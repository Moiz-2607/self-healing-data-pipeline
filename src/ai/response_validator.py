from typing import Any


ALLOWED_ACTIONS = {
    "NO_ACTION",
    "REPAIR_DATATYPE",
    "HUMAN_REVIEW",
}

ALLOWED_OPERATIONS = {
    "CONVERT_DTYPE",
}


def validate_ai_diagnosis(
    diagnosis: dict[str, Any],
) -> dict[str, Any]:
    """
    Validate and sanitize an AI-generated diagnosis
    before it can reach the recovery system.
    """

    required_fields = {
        "issue",
        "description",
        "suggested_action",
        "confidence",
        "repair_plan",
    }

    missing_fields = required_fields - diagnosis.keys()

    if missing_fields:
        raise ValueError(
            f"AI diagnosis is missing fields: {sorted(missing_fields)}"
        )

    confidence = diagnosis["confidence"]

    if not isinstance(confidence, (int, float)):
        raise ValueError("AI confidence must be numeric.")

    if not 0.0 <= confidence <= 1.0:
        raise ValueError("AI confidence must be between 0.0 and 1.0.")

    action = diagnosis["suggested_action"]

    if action not in ALLOWED_ACTIONS:
        raise ValueError(
            f"Unsupported AI action: {action}"
        )

    repair_plan = diagnosis["repair_plan"]

    if not isinstance(repair_plan, list):
        raise ValueError("AI repair_plan must be a list.")

    validated_plan = []

    for operation in repair_plan:
        if not isinstance(operation, dict):
            raise ValueError(
                "Each repair operation must be an object."
            )

        operation_type = operation.get("operation")

        if operation_type not in ALLOWED_OPERATIONS:
            raise ValueError(
                f"Unsupported repair operation: {operation_type}"
            )

        if operation_type == "CONVERT_DTYPE":
            required_operation_fields = {
                "operation",
                "column",
                "from_dtype",
                "to_dtype",
            }

            missing_operation_fields = (
                required_operation_fields - operation.keys()
            )

            if missing_operation_fields:
                raise ValueError(
                    "Repair operation is missing fields: "
                    f"{sorted(missing_operation_fields)}"
                )

        validated_plan.append(operation)

    validated_diagnosis = diagnosis.copy()
    validated_diagnosis["confidence"] = float(confidence)
    validated_diagnosis["repair_plan"] = validated_plan

    return validated_diagnosis
