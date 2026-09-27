from src.simulation.scenario_runner import run_all_scenarios


def print_report(results: list[dict]) -> None:
    print("=" * 58)
    print("SELF-HEALING PIPELINE - FAILURE SIMULATION")
    print("=" * 58)

    for index, result in enumerate(results):
        print()
        print(f"Scenario:   {result['scenario'].upper()}")
        print(f"Risk:       {result['risk']['risk_level']}")
        print(f"Decision:   {result['decision']['action']}")
        print(f"Status:     {result['status']}")
        print(
            "Validation: "
            + ("PASSED" if result["validation"]["valid"] else "FAILED")
        )

        if index < len(results) - 1:
            print("-" * 58)

    print()
    print("=" * 58)
    print("Simulation completed")
    print("=" * 58)


if __name__ == "__main__":
    results = run_all_scenarios()
    print_report(results)
