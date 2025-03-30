from sales_pipeline.utils.envs import get_bool_env


def test_get_bool_env_true(monkeypatch):
    monkeypatch.setenv("FEATURE_ENABLED", "true")
    assert get_bool_env("FEATURE_ENABLED") is True


def test_get_bool_env_false(monkeypatch):
    monkeypatch.setenv("FEATURE_ENABLED", "false")
    assert get_bool_env("FEATURE_ENABLED") is False


def test_get_bool_env_default():
    assert get_bool_env("DOES_NOT_EXIST", "true") is True
    assert get_bool_env("DOES_NOT_EXIST", "false") is False
