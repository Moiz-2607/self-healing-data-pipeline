from src.monitoring.health_summary import build_health_summary


def print_health_summary() -> None:
    summary = build_health_summary()

    print("=" * 58)
    print("SELF-HEALING PIPELINE - HEALTH SUMMARY")
    print("=" * 58)

    print(f"Total events:       {summary['total_events']}")
    print(f"Pipeline successes: {summary['pipeline_success']}")
    print(f"Successful repairs: {summary['successful_repairs']}")
    print(f"Rollbacks:          {summary['rollbacks']}")
    print(f"Human reviews:      {summary['review_required']}")

    print("=" * 58)


if __name__ == "__main__":
    print_health_summary()
