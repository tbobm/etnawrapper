INTRA_API = "https://prepintra-api.etna-alternance.net"
ETNA_API = "https://auth.etna-alternance.net"
AUTH_URL = "https://auth.etna-alternance.net/login"
MODULE_API = "https://modules-api.etna-alternance.net"
GSA_API = "https://gsa-api.etna-alternance.net"

IDENTITY_URL = ETNA_API + "/identity"
USER_INFO_URL = ETNA_API + "/api/users/{user_id}"
USER_PROMO_URL = INTRA_API + "/promo"
GRADES_URL = INTRA_API + "/terms/{promo_id}/students/{login}/marks"
NOTIF_URL = INTRA_API + "/students/{login}/informations"
ACTIVITY_URL = MODULE_API + "/students/{login}/currentactivities"
PICTURE_URL = ETNA_API + "/api/users/{login}/photo"
SEARCH_URL = MODULE_API + "/students/{login}/search"
ACTIVITIES_URL = MODULE_API + "/{module_id}/activities"
GROUPS_URL = INTRA_API + "/sessions/{module_id}/project/{project_id}/groups"
PROMOTION_URL = INTRA_API + "/trombi/{promo_id}"
GSA_EVENTS_URL = GSA_API + "/students/{login}/events"
GSA_LOGS_URL = GSA_API + "/students/{login}/logs"

EVENTS_URL = INTRA_API + "/students/{login}/events?end={end_date}&start={start_date}"
DECLARATION_URL = INTRA_API + "/students/{login}/modules/{module_id}/activities/{activity_id}/declareLogs"
