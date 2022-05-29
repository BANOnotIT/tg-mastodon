from schema import Schema, Or, Optional

config_schema = Schema({
    Optional('default_props'): {
        Optional('instance_url'): str,
        Optional('client_secret'): str,
        Optional('client_id'): str,
        Optional('format'): Or('plain', 'referenced', 'markdown'),
        Optional('visibility'): Or('direct', 'private', 'unlisted', 'public'),
    },
    'channel': {
        str: {
            'tg_content_link': str,
            Optional('instance_url'): str,
            Optional('client_secret'): str,
            Optional('client_id'): str,
            Optional('format'): Or('plain', 'referenced', 'markdown'),
            Optional('visibility'): Or('direct', 'private', 'unlisted', 'public'),
        }
    },
    'persist_path': str,
})
