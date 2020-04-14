import click

from main import Wumpus

@click.command('--greeting', '-g',
               default=None,
               help="What to say to the wumpus")
@click.argument("name")
def cli(greeting, name):

    wumpus = Wumpus(name)

    click.echo(f"A wild wumpus named {wumpus.name} appears.")

    if greeting is None:
        click.echo("You do not disturb the wumpus")
    else:
        click.echo(f"You say to the wumpus: {greeting}")

        response = wumpus.talk_to(greeting)
        click.echo(f"It responds to you: {response}")

if __name__ == "__main__":

    cli()
