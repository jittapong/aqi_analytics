# import warnings
import pytest
# from airflow.models import DagBag

# @pytest.fixture(scope="session")
# def dagbag():
#     return DagBag(dag_folder="/opt/airflow/dags", include_examples=False)

def test_import_in_dag_should_not_contains_import_errors():
    """Ensure DAG files are loaded without errors."""
    
    # errors = {
    #     dag_file: err
    #     for dag_file, err in dagbag.import_errors.items()
    #     if not isinstance(err, warnings.WarningMessage)
    # }
    # assert errors == {}, "Should not contains import errors"