import os

from pprint import pprint

from etna import EtnaClient



client = EtnaClient(
    login=os.environ.get('ETNA_USER'),
    password=os.environ.get('ETNA_PASS'),
)

pprint(client.f('get_infos'))
pprint(client.f('get_activities_for_project', login='martin_e', module_id=4176))
