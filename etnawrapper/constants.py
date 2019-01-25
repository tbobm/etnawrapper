"""
URL templates to unclutter main module.
"""
PREP_API = 'https://prepintra-api.etna-alternance.net'
ETNA_API = 'https://auth.etna-alternance.net'
AUTH_URL = 'https://auth.etna-alternance.net/login'
MODULE_API = 'https://modules-api.etna-alternance.net'
GSA_API = 'https://gsa-api.etna-alternance.net'

IDENTITY_URL = ETNA_API + '/identity'
USER_INFO_URL = ETNA_API + '/api/users/{user_id}'
USER_PROMO_URL = PREP_API + '/promo'
GRADES_URL = PREP_API + '/terms/{promo_id}/students/{login}/marks'
NOTIF_URL = PREP_API + '/students/{login}/informations'
ACTIVITY_URL = MODULE_API + '/students/{login}/currentactivities'
PICTURE_URL = ETNA_API + '/api/users/{login}/photo'
SEARCH_URL = MODULE_API + '/students/{login}/search'
ACTIVITIES_URL = MODULE_API + '/{project_id}/activities'
GROUPS_URL = PREP_API + '/sessions/{module_id}/project/{project_id}/groups'
PROMOTION_URL = PREP_API + '/trombi/{promotion_id}'
GSA_EVENTS_URL = GSA_API + '/students/{login}/events'

EVENTS_URL = '{}{}'.format(
    PREP_API,
    '/students/{login}/events?end={end_date}&start={start_date}',
)
