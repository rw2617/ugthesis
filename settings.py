from os import environ

SESSION_CONFIGS = [

    #competition
    dict(
        name='competition_risk',
        app_sequence=['comp'],
        num_demo_participants=3,
        known_probability=True,
    ),
    
    dict(
        name='competition_uncertain',
        app_sequence=['comp'],
        num_demo_participants=3,
    ),

    #no competition
    dict(
        name='no_competition_risk',
        app_sequence=['no_comp'],
        num_demo_participants=2,
        known_probability=True,
    ),

    dict(
        name='no_competition_uncertain',
        app_sequence=['no_comp'],
        num_demo_participants=2,
    )
]

ROOMS = [
    dict(
        name='cess',
        display_name='CESS lab',
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.10, participation_fee=15.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2087189829501'
