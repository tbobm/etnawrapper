"""Script to interact with etnawrapper."""
import os
import typing

import arrow  # TODO: Use datetime to remove arrow dependency
import click

from etnawrapper import EtnaWrapper


CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def _clear_line():
    print(CURSOR_UP_ONE + ERASE_LINE, end='')


def display_current_projects(projects: typing.List[typing.Dict]):
    """Pretty print current projects with end date."""
    fmt_p = [f"{project['name']} ({project['date_end']})" for project in projects]
    click.secho("  projects:", bold=True)
    for project in fmt_p:
        click.secho(f"     {project}", fg='blue')


def display_current_quests(quests: typing.List[typing.Dict], show_all=False):
    """Pretty print quests and their stages."""
    _quests = [
        {
            'name': f"{quest['name']} ({quest['date_end']})",
            'stages': quest['stages'],
        } for quest in quests
    ]
    click.secho("  quests:", bold=True)
    for quest in _quests:
        click.secho(f"     {quest['name']}", fg='blue')
        for stage in quest['stages']:
            if not show_all and arrow.get(stage['end']) < arrow.utcnow():
                continue
            click.secho(f"       {stage['name']} {(stage['end'])}", fg='green')


@click.group(invoke_without_command=True)
@click.pass_context
def activities(ctx):
    """Interact with your activities."""
    if ctx.invoked_subcommand is None:
        list_current_activities(False)


@click.group()
def conversations():
    """Interact with your profile's conversations."""


@click.group()
def cli():
    """CLI utility to interact with ETNA's APIs."""


@conversations.command(name='list')
@click.option(
    '--count',
    help='Number of conversation to display',
    type=int,
    default=3,
)
def list_latest_conversations(count):
    etna = get_wrapper()
    click.secho(f"Fetching conversations for {etna.login}")
    infos = etna.get_user_info()
    response = etna.get_conversations(infos['id'], size=count)
    _clear_line()
    # TODO: Maybe cache the user_id of the author to
    #       avoid querying the same profile
    for conversation in response['hits']:
        infos = etna.get_user_info(conversation['last_message']['user'])
        identifier = conversation['metas'].get('uv_name', 'students')
        wall_name = conversation['metas']['wall-name']
        message = conversation['last_message']['content'].replace('\n\n', '\n')

        click.secho(conversation['title'], bold=True, fg='blue')
        click.secho(f"{identifier} - {wall_name}", underline=True)
        click.secho(f"{infos['login']} - {infos['firstname']} {infos['lastname']}", fg='red')
        click.secho(message)



@activities.command(name='list')
@click.option(
    '--full',
    help='Display past stages.',
    type=bool,
    is_flag=True,
)
def _wrap_list_activities(full):
    list_current_activities(full)


def list_current_activities(full):
    """List the current activities for the authenticated student."""
    etna = get_wrapper()
    click.secho(f"Fetching activities for {etna.login}")
    activities = etna.get_current_activities()
    _clear_line()
    for activity, content in activities.items():
        quests = content['quest']
        types = []
        projects = content['project']
        if projects:
            types.append('project')
        if quests:
            types.append('quest')

        click.secho(f"{activity}:", bold=True, fg='red')
        if projects:
            display_current_projects(projects)
        if quests:
            display_current_quests(quests, show_all=full)


def get_wrapper():
    login = os.environ.get('ETNA_USER')
    password = os.environ.get('ETNA_PASS')
    wrapper = EtnaWrapper(login, password)
    return wrapper


def main():
    cli.add_command(activities)
    cli.add_command(conversations)
    cli()


if __name__ == '__main__':
    main()
