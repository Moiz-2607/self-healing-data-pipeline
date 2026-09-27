from src.simulation.scenario_runner import (
    run_scenario,
    run_all_scenarios,
)


def test_healthy_scenario():
    result = run_scenario("healthy")

    assert result["scenario"] == "healthy"
    assert result["status"] == "SUCCESS"
    assert result["validation"]["valid"] is True


def test_renamed_column_scenario():
    result = run_scenario("renamed_column")

    assert result["scenario"] == "renamed_column"
    assert result["status"] == "REVIEW_REQUIRED"
    assert result["decision"]["action"] == "HUMAN_REVIEW"


def test_datatype_drift_scenario():
    result = run_scenario("datatype_drift")

    assert result["scenario"] == "datatype_drift"
    assert result["status"] in {
        "REPAIRED",
        "ROLLED_BACK",
    }


def test_unknown_scenario():
    try:
        run_scenario("unknown")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Unknown scenario should raise ValueError."
        )


def test_run_all_scenarios():
    results = run_all_scenarios()

    assert len(results) == 3
    assert {
        result["scenario"]
        for result in results
    } == {
        "healthy",
        "renamed_column",
        "datatype_drift",
    }
