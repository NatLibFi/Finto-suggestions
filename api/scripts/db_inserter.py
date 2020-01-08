from datetime import datetime
from api.models import Suggestion, Tag, Meeting, SuggestionTag, Event, EventTypes, EventActionSubTypes


class DBInserter:

    def __init__(self, db):
        self.suggestion_count = 0
        self.new_meetings = []
        self.existing_tags = []
        self.new_tags = []
        self.suggestion_tags_count = 0
        self.events_count = 0

        self.__fetch_tags_from_db(db)

    def __fetch_tags_from_db(self, db):
        result = Tag.query.all()
        if result is not None and len(result) > 0:
            for tag in result:
                self.existing_tags.append(tag.label)

    def __map_meeting_bo(self, meeting):
        meeting_bo = Meeting()
        meeting_bo.name = meeting.name
        meeting_bo.created_date = meeting.created_date
        meeting_bo.meeting_date = meeting.meeting_date
        return meeting_bo

    def __map_suggestion_bo(self, model):
        suggestion_bo = Suggestion()
        suggestion_bo.created = model.created
        suggestion_bo.modified = model.modified
        suggestion_bo.suggestion_type = model.body.type
        suggestion_bo.status = model.status
        suggestion_bo.organization = model.body.organization
        suggestion_bo.description = model.body.description
        suggestion_bo.reason = model.body.reason
        suggestion_bo.preferred_label = model.body.preferred_labels
        suggestion_bo.alternative_labels = model.body.alternative_labels
        suggestion_bo.broader_labels = model.body.broader_labels
        suggestion_bo.narrower_labels = model.body.narrower_labels
        suggestion_bo.related_labels = model.body.related_labels
        suggestion_bo.groups = model.body.groups
        suggestion_bo.scopeNote = model.body.scope_note
        suggestion_bo.exactMatches = model.body.exact_matches
        suggestion_bo.yse_term = model.body.yse_term
        return suggestion_bo

    def __map_tags_to_tags_bo(self, tags):
        tags_bo = []
        if tags is not None and len(tags) > 0:
            for tagModel in tags:
                tag = Tag()
                tag.label = tagModel
                tags_bo.append(tag)
        return tags_bo

    def __map_tag_labels_to_suggestiontag_bo(self, tag_label, suggestion_id, event_id):
        if tag_label is not None and len(tag_label) > 0 and suggestion_id > 0 and event_id > 0:
            suggestion_tag = SuggestionTag()
            suggestion_tag.tag_label = tag_label
            suggestion_tag.suggestion_id = suggestion_id
            suggestion_tag.event_id = event_id
            return suggestion_tag
        return None

    def __map_to_event_bo(self, suggestion_id):
        event_bo = Event()
        event_bo.created = datetime.now()
        event_bo.modified = datetime.now()
        event_bo.event_type = EventTypes.ACTION
        event_bo.sub_type = EventActionSubTypes.SYSTEM
        event_bo.text = f"Lisätty tunnisteet:  "
        event_bo.suggestion_id = suggestion_id
        return event_bo

    def __map_comments_to_comments_bo(self, comments, suggestion_id):
        comments_bo = []
        if comments is not None and len(comments) > 0:
            for comment in comments:
                comment_bo = Event()
                comment_bo.created = comment.created
                comment_bo.modified = comment.modified
                comment_bo.event_type = EventTypes.COMMENT
                comment_bo.text = comment.text
                comment_bo.suggestion_id = suggestion_id
                # Mika 111019
                if comment_bo.user_id is None:
                    comment_bo.user_id = 1
                comments_bo.append(comment_bo)
        return comments_bo

    def __map_models_to_db_bo(self, models):
        bo_models = []
        if models is not None and len(models) > 0:
            for model in models:
                suggestion_models = dict()
                if model.meeting != None:
                    meeting_bo = self.__map_meeting_bo(model.meeting)
                    suggestion_models["meeting"] = meeting_bo
                suggestion_bo = self.__map_suggestion_bo(model)
                suggestion_models["suggestion"] = suggestion_bo
                suggestion_models["tags"] = self.__map_tags_to_tags_bo(
                    model.tags)
                suggestion_models["comments"] = self.__map_comments_to_comments_bo(
                    model.comments, None)
                bo_models.append(suggestion_models)
        return bo_models

    def __get_existing_meeting(self, meeting_name):
        for existing_meeting in self.new_meetings:
            if existing_meeting["name"] == meeting_name:
                return existing_meeting
        return None

    def __insert_meeting_to_db(self, db, meeting):
        if meeting is not None:
            db.session.add(meeting)
            db.session.commit()
            self.new_meetings.append({"name": meeting.name, "id": meeting.id})
            print(f"New meeting added {meeting.id}")

    def __insert_suggestion_to_db(self, db, suggestion):
        if suggestion is not None:
            db.session.add(suggestion)
            db.session.commit()
            self.suggestion_count += 1
            print(f"New suggestion added {suggestion.id}")

    def __get_existing_tag(self, tag_label):
        for existing_tag in self.existing_tags:
            if existing_tag == tag_label.upper():
                return existing_tag
        return None

    def __insert_event_bo_to_db(self, db, tags, suggestion_id):
        if tags is not None and len(tags) > 0:
            event_bo = self.__map_to_event_bo(suggestion_id)
            db.session.add(event_bo)
            db.session.commit()
            self.events_count += 1
            print(
                f"New event {event_bo.id} for adding tags {', '.join(tags)} to suggestion {suggestion_id}")
            return event_bo
        return None

    def __insert_comments_to_db(self, db, comments, suggestion_id):
        comment_id_list = []
        if comments is not None and len(comments) > 0:
            comments_bo = self.__map_comments_to_comments_bo(
                comments, suggestion_id)
            for comment_bo in comments_bo:
                db.session.add(comment_bo)
                db.session.commit()
                self.events_count += 1
                comment_id_list.append(comment_bo.id)
                print(
                    f"New comment {comment_bo.id} added to suggestion {suggestion_id}")
        return comment_id_list

    def __insert_suggestion_tag_relationship(self, db, tag_label, suggestion_id, event_id):
        suggestion_tag = self.__map_tag_labels_to_suggestiontag_bo(
            tag_label, suggestion_id, event_id)
        if suggestion_tag is not None:
            db.session.add(suggestion_tag)
            db.session.commit()
            self.suggestion_tags_count += 1
            print(
                f"New suggestion {suggestion_id} <-> tag {tag_label} relation added")

    def __insert_tags_and_relation_to_suggestion(self, db, tags, suggestion_id):
        if tags is not None and len(tags) > 0:
            suggestion_tags = []
            for tag_label in tags:
                existing_tag = self.__get_existing_tag(tag_label.label)
                if existing_tag is None:
                    db.session.add(tag_label)
                    db.session.commit()
                    self.new_tags.append(tag_label.label)
                    suggestion_tags.append(tag_label.label)
                    self.existing_tags.append(tag_label.label)
                    print(f"New tag added {tag_label.label}")
                else:
                    suggestion_tags.append(existing_tag)
            event_bo = self.__insert_event_bo_to_db(
                db, suggestion_tags, suggestion_id)
            for tag_label in tags:
                if event_bo is not None:
                    # lets not try to add this if event creation failed
                    self.__insert_suggestion_tag_relationship(
                        db, tag_label.label, suggestion_id, event_bo.id)

    def insert_models_to_db(self, db, models):
        bo_models_dict = self.__map_models_to_db_bo(models)
        for model in bo_models_dict:
            try:
                suggestion = model["suggestion"]
                tags = model["tags"]
                if 'meeting' in model.keys():
                    meeting = model["meeting"]
                    exists = self.__get_existing_meeting(meeting.name)
                    if exists is None:
                        self.__insert_meeting_to_db(db, meeting)
                        suggestion.meeting_id = meeting.id
                    else:
                        suggestion.meeting_id = exists["id"]
                self.__insert_suggestion_to_db(db, suggestion)
                self.__insert_tags_and_relation_to_suggestion(
                    db, tags, suggestion.id)
                if 'comments' in model.keys():
                    comments = model["comments"]
                    comment_id_list = self.__insert_comments_to_db(
                        db, comments, suggestion.id)
                    for id in comment_id_list:
                        suggestion.events.append(Event.query.get(id))
            except Exception as ex:
                print(str(ex))
                db.session.rollback()
            finally:
                db.session.close()
        print("\r\n")
        print("RESULTS: ")
        print(f"Suggestions inserted {self.suggestion_count}")
        print(f"Meetings inserted {len(self.new_meetings)}")
        print(f"Events inserted {self.events_count}")
        print(f"Tags inserted {len(self.new_tags)}")
        print(
            f"Tag <-> Suggestion relationships inserted {self.suggestion_tags_count}")
