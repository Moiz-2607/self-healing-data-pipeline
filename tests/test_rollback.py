import pandas as pd

from src.recovery.rollback import create_backup, rollback


def test_create_backup():
    data = pd.DataFrame({
        "age": [21, 24, 22]
    })

    backup = create_backup(data)

    data.loc[0, "age"] = 99

    assert backup.loc[0, "age"] == 21


def test_rollback_restores_original_data():
    original_data = pd.DataFrame({
        "age": [21, 24, 22]
    })

    backup = create_backup(original_data)

    modified_data = backup.copy()
    modified_data.loc[0, "age"] = 99

    restored_data = rollback(backup)

    assert restored_data["age"].tolist() == [21, 24, 22]
    assert modified_data["age"].tolist() == [99, 24, 22]
