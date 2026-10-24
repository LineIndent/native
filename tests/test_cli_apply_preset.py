import pytest

from cli import main as cli_main


def test_documented_example_preset_decodes():
    cfg = cli_main.decode_seed(
        "b1000",
        cli_main.BASE_THEMES,
        cli_main.COLOR_THEMES,
        cli_main.STYLE_REGISTRY,
        cli_main.RADII_OPTIONS,
        cli_main.FONT_REGISTRY,
    )
    assert cfg


def test_invalid_preset_errors_to_stderr(tmp_path, monkeypatch, capsys):
    (tmp_path / "rxconfig.py").write_text("")
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as exc:
        cli_main.cmd_apply("zzz-invalid")
    assert exc.value.code == 1
    out = capsys.readouterr()
    assert "Invalid preset ID" in out.err
    assert "buridan.reflex.run/create" in out.err
    assert "buridan-ui.com" not in out.err
    assert out.out == ""
