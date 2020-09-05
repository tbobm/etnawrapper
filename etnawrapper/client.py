"""Script to interact with etnawrapper."""
import os
import typing

import arrow  # TODO: Use datetime to remove arrow dependency
import click

from etnawrapper import EtnaWrapper


def display_current_projects(projects: typing.List[typing.Dict]):
    """Pretty print current projects with end date."""
    fmt_p = [f"{project['name']} ({project['date_end']})" for project in projects]
    print("  projects:")
    for project in fmt_p:
        print(f"     {project}")


def display_current_quests(quests: typing.List[typing.Dict], show_all=False):
    """Pretty print quests and their stages."""
    _quests = [
        {
            'name': f"{quest['name']} ({quest['date_end']})",
            'stages': quest['stages'],
        } for quest in quests
    ]
    print("  quests:")
    for quest in _quests:
        print(f"     {quest['name']}")
        for stage in quest['stages']:
            if not show_all and arrow.get(stage['end']) < arrow.utcnow():
                continue
            print(f"       {stage['name']} {(stage['end'])}")


@click.group()
def activities():
    """Click command group."""


@activities.command(name='activities')
@click.option(
    '--full',
    help='Display past stages.',
    type=bool,
    is_flag=True,
)
def list_current_activities(full):
    """List the current activities for the authenticated student."""
    etna = get_wrapper()
    activities = etna.get_current_activities()
    for activity, content in activities.items():
        quests = content['quest']
        types = []
        projects = content['project']
        if projects:
            types.append('project')
        if quests:
            types.append('quest')

        print(f"{activity}:")
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
    activities()


if __name__ == '__main__':
    main()
