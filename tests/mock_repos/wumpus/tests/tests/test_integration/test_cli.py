from click.testing import CliRunner

from wumpus.cli import cli

def test_cli_name():
    runner = CliRunner()
    result = runner.invoke(cli, ["sam"])

    assert result.exit_code == 0
