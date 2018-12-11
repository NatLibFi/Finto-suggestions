import json
import os

from api.models import Suggestion, Tag, Meeting, SuggestionTag, db
from app import create_app

meetings_cache = []
tags_cache = []


def import_meeting(meeting):
    for existing_meeting in meetings_cache:
        if existing_meeting.name == meeting:
            return existing_meeting
    new_meeting = Meeting()
    new_meeting.name = meeting
    meetings_cache.append(new_meeting)
    insert(new_meeting)
    return new_meeting


def get_existing_tag(tag_label):
    for existing_tag in tags_cache:
        if existing_tag.label == tag_label.upper():
            return existing_tag
    return None


def import_tags(tags):
    result_tags = []
    for tag in tags:
        existing_tag = get_existing_tag(tag)
        if existing_tag is None:
            new_tag = Tag()
            new_tag.label = tag
            insert(new_tag)
            result_tags.append(new_tag)
            tags_cache.append(new_tag)
        else:
            result_tags.append(existing_tag)

    return result_tags


def import_suggestion_tags_association(suggestion, tags):
    for tag in tags:
        suggestion_tag = SuggestionTag()
        suggestion_tag.suggestion_id = suggestion.id
        suggestion_tag.tag_label = tag.label
        insert(suggestion_tag)


def import_suggestion(suggestion):
    tags = import_tags(suggestion["tags"])
    new_suggestion = Suggestion()
    new_suggestion.suggestion_type = "NEW" # hard coded...fix before late
    new_suggestion.preferred_label = suggestion["preferred_label"]
    new_suggestion.alternative_label = suggestion["alternative_label"]
    new_suggestion.organization = suggestion["organization"]
    new_suggestion.broader = suggestion["broader"]
    new_suggestion.related = suggestion["related"]
    new_suggestion.reason = suggestion["reason"]
    new_suggestion.groups = suggestion["groups"]
    # new_suggestion.tags = import_tags(suggestion["tags"])
    new_suggestion.meeting_id = import_meeting(suggestion["meeting"]["name"]).id
    insert(new_suggestion)
    import_suggestion_tags_association(new_suggestion, tags)
    # not implemented yet new_suggestion.needed_for = suggestion["needed_for"]


def insert(model):
    try:
        db.session.add(model)
        db.session.commit()
    except Exception as exception:
        db.session.rollback()
        raise exception


if __name__ == '__main__':
    app = create_app()
    db.app = app.app
    with open(os.path.join(os.path.dirname(__file__), "suggestions.json")) as suggestions_file:
        raw_suggestions = json.load(suggestions_file)
        for suggestion in raw_suggestions:
            import_suggestion(suggestion)

