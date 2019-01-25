import os
import arrow

from pprint import pprint

from etna import EtnaClient



client = EtnaClient(
    login=os.environ.get('ETNA_USER'),
    password=os.environ.get('ETNA_PASS'),
)

# pprint(client.f('get_promos'))
# pprint(client.f('get_log_events', login='massar_t'))
pprint(client.f('get_events', login='massar_t', start_date=arrow.utcnow().shift(days=-2), end_date=arrow.utcnow().shift(days=29)))
# pprint(client.f('get_group_for_activity', project_id=5002, module_id=1800))
# pprint(client.f('get_projects', login='martin_e', module_id=4176))
