from click.testing import CliRunner
from weather.cli import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, auto_envvar_prefix="WEATHER")
    assert result.exit_code == 0