import pytest

from sinatools import cli


def test_cli_help_lists_commands(capsys):
    assert cli.main([]) == 0
    output = capsys.readouterr().out
    assert "sinatools" in output
    assert "arStrip" in output
    assert "relation_extractor" in output


def test_cli_runs_subcommand(capsys):
    cli.main(["arStrip", "--text", "مُختَبَر سينا 2026!"])
    output = capsys.readouterr().out.strip()
    assert output == "مختبر سينا"


def test_cli_runs_jaccard_subcommand(capsys):
    cli.main([
        "jaccard_similarity",
        "--list1",
        "a,b",
        "--list2",
        "a,c",
        "--delimiter",
        ",",
        "--selection",
        "jaccardSimilarity",
    ])
    output = capsys.readouterr().out.strip()
    assert output == "Jaccard Result: 0.3333333333333333"


def test_cli_unknown_command_exits():
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["unknown-command"])

    assert excinfo.value.code == 2
