from api.models import EventTypes

# temp models


class GithubBodyModel(object):
    def __init__(self):
        self.type = ''
        self.preferred_labels = {}
        self.alternative_labels = []
        self.broader_labels = []
        self.narrower_labels = []
        self.related_labels = []
        self.exact_matches = []
        self.needed_for = None
        self.description = None
        self.reason = None
        self.scope_note = None
        self.groups = []
        self.organization = None
        self.yse_term = None


class GithubMeetingModel(object):
    def __init__(self, name, created_date, meeting_date):
        self.name = name
        self.created_date = created_date
        self.meeting_date = meeting_date


class GithubIssueModel(object):
    def __init__(self, name, status, meeting, created, modified, closed, body):
        self.name = name
        self.status = status
        self.meeting = meeting
        self.created = created
        self.modified = modified
        self.closed = closed
        self.body = body
        self.tags = []
        self.events = []
        self.comments = []


class GithubCommentModel(object):
    def __init__(self, created, modified, text):
        self.created = created
        self.modified = modified
        self.user_id = None
        self.event_type = EventTypes.COMMENT
        self.suggestion_id = None
        self.text = text
