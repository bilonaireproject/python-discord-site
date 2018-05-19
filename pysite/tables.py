from typing import List, NamedTuple


class Table(NamedTuple):
    primary_key: str
    keys: List[str]
    locked: bool = True


TABLES = {
    "bot_events": Table(  # Events to be sent to the bot via websocket
        primary_key="id",
        keys=sorted([
            "id",
            "data"
        ])
    ),

    "hiphopify": Table(  # Users in hiphop prison
        primary_key="user_id",
        keys=sorted([
            "user_id",
            "end_timestamp",
            "forced_nick"
        ])
    ),

    "hiphopify_namelist": Table(  # Names and images of hiphop artists
        primary_key="name",
        keys=sorted([
            "name",
            "image_url"
        ]),
        locked=False
    ),

    "code_jams": Table(  # Information about each code jam
        primary_key="number",
        keys=sorted([
            "date_end",  # datetime
            "date_start",  # datetime
            "end_html",  # str
            "end_rst",  # str
            "info_rst",  # str
            "info_html",  # str
            "number",  # int
            "participants",  # list[int]
            "repo",  # str
            "state",  # str
            "task_html",  # str
            "task_rst",  # str
            "teams",  # list[int]
            "theme",  # str
            "title",  # str
            "winners"  # list[int]
        ])
    ),

    "code_jam_forms": Table(  # Application forms for each jam
        primary_key="number",
        keys=sorted([
            "number",  # int
            "questions"  # list[dict[str, str]]  {title, type, input_type, options?}
        ])
    ),

    "code_jam_questions": Table(  # Application form questions
        primary_key="id",
        keys=sorted([
            "data",  # dict
            "id",  # uuid
            "optional",  # bool
            "title",  # str
            "type",  # str
        ])
    ),

    "code_jam_responses": Table(  # Application form responses
        primary_key="id",
        keys=sorted([
            "id",  # uuid
            "jam",  # int
            "answers",  # dict {question, answer, metadata}
            "approved"  # bool
        ])
    ),

    "code_jam_teams": Table(  # Teams for each jam
        primary_key="id",
        keys=sorted([
            "id",  # uuid
            "name",  # str
            "members"  # list[int]
        ])
    ),

    "code_jam_infractions": Table(  # Individual infractions for each user
        primary_key="id",
        keys=sorted([
            "id",  # uuid
            "participant",  # str
            "reason",  # str
            "number"  # int (optionally -1 for permanent)
        ])
    ),

    "code_jam_participants": Table(  # Info for each participant
        primary_key="id",
        keys=sorted([
            "snowflake",  # int
            "skill_level",  # str
            "age",  # str
            "github_username",  # str
            "timezone"  # str
        ])
    ),

    "oauth_data": Table(  # OAuth login information
        primary_key="id",
        keys=sorted([
            "id",
            "access_token",
            "expires_at",
            "refresh_token",
            "snowflake"
        ])
    ),

    "snake_facts": Table(  # Snake facts
        primary_key="fact",
        keys=sorted([
            "fact"
        ]),
        locked=False
    ),

    "snake_idioms": Table(  # Snake idioms
        primary_key="idiom",
        keys=sorted([
            "idiom"
        ]),
        locked=False
    ),

    "snake_names": Table(  # Snake names
        primary_key="name",
        keys=sorted([
            "name",
            "scientific"
        ]),
        locked=False
    ),

    "snake_quiz": Table(  # Snake questions and answers
        primary_key="id",
        keys=sorted([
            "id",
            "question",
            "options",
            "answerkey"
        ]),
        locked=False
    ),

    "special_snakes": Table(  # Special case snakes for the snake converter
        primary_key="name",
        keys=sorted([
            "name",
            "info",
            "image_list",
        ]),
        locked=False
    ),

    "tags": Table(  # Tag names and values
        primary_key="tag_name",
        keys=sorted([
            "tag_name",
            "tag_content"
        ]),
        locked=False
    ),

    "users": Table(  # Users from the Discord server
        primary_key="user_id",
        keys=sorted([
            "user_id",
            "roles",
            "username",
            "discriminator",
            "email"
        ])
    ),

    "wiki": Table(  # Wiki articles
        primary_key="slug",
        keys=sorted([
            "slug",
            "headers",
            "html",
            "rst",
            "text",
            "title"
        ])
    ),

    "wiki_revisions": Table(  # Revisions of wiki articles
        primary_key="id",
        keys=sorted([
            "id",
            "date",
            "post",
            "slug",
            "user"
        ])
    ),

    "_versions": Table(  # Table migration versions
        primary_key="table",
        keys=sorted([
            "table",
            "version"
        ])
    )
}
