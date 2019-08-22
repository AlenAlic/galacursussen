# Environments
DEVELOPMENT_ENV = 'development'
DEBUG_ENV = 'debug'
TESTING_ENV = 'testing'
PRODUCTION_ENV = 'production'
TESTING_ENVIRONMENTS = [DEVELOPMENT_ENV, TESTING_ENV, DEBUG_ENV]


ERRORS = "errors"


# Requests
GET = "GET"
POST = "POST"
PATCH = "PATCH"
PUT = "PUT"
DELETE = "DELETE"

# Access levels
ADMIN = 'Admin'
ORGANIZER = 'Organizer'
MEMBER = 'Member'
TREASURER = 'Treasurer'

ACCESS = {
    ADMIN: 0,
    ORGANIZER: 10,
    MEMBER: 11,
    TREASURER: 20
}
ACCESS_LEVEL = {v: k for k, v in ACCESS.items()}


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"
FIRST_MONTH = 8
FIRST_MONTH_STRING = "08"
