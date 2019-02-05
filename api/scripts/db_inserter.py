from api.models import Suggestion, Tag, Meeting, SuggestionTag, Event, EventTypes
from datetime import datetime

class DBInserter:

  def __init__(self):
    self.suggestion_count = 0
    self.meeting_count = 0
    self.existing_tags = []
    self.suggestion_tags_count = 0
    self.events_count = 0


  def __map_meeting_bo(self, meeting):
    meeting_bo = Meeting()
    meeting_bo.name = meeting.name
    meeting_bo.created_date = meeting.created_date
    return meeting_bo

  def __map_suggestion_bo(self, model):
    suggesiton_bo = Suggestion()
    suggesiton_bo.created = model.created
    suggesiton_bo.modified = model.modified
    suggesiton_bo.suggestion_type = model.body.type
    suggesiton_bo.status = model.status
    suggesiton_bo.organization = model.body.organization
    suggesiton_bo.reason = model.body.reason
    suggesiton_bo.preferred_label = model.body.preferred_labels
    suggesiton_bo.groups = model.body.groups
    suggesiton_bo.description = model.body.description
    suggesiton_bo.scopeNote = model.body.scopeNote
    return suggesiton_bo

  def __map_tags_to_tags_bo(self, tags):
    tags_bo = []
    if tags is not None and len(tags) > 0:
      for tagModel in tags:
        tag = Tag()
        tag.label = tagModel[0]
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

  def __map_to_event_bo(self, tag_label):
    event_bo = Event()
    event_bo.created = datetime.now()
    event_bo.modified = datetime.now()
    event_bo.event_type = EventTypes.ACTION
    event_bo.text = f"tunniste tuotu vanhasta järjestelmästä {tag_label}"
    return event_bo

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
        suggestion_models["tags"] = self.__map_tags_to_tags_bo(model.tags)
        bo_models.append(suggestion_models)
    return bo_models

  def __insert_meeting_to_db(self, db, meeting):
    if meeting is not None:
      db.session.add(meeting)
      db.session.commit()
      self.meeting_count += 1
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

  def __insert_event_bo_to_db(self, db, tag_label):
    if tag_label is not None and len(tag_label) > 0:
      event_bo = self.__map_to_event_bo(tag_label)
      db.session.add(event_bo)
      db.session.commit()
      self.events_count += 1
      print(f"New event {event_bo.id} add when creating new tag {tag_label}")
      return event_bo
    return None


  def __insert_suggestion_tag_relationship(self, db, tag_label, suggestion_id, event_id):
    suggestion_tag = self.__map_tag_labels_to_suggestiontag_bo(tag_label, suggestion_id, event_id)
    if suggestion_tag is not None:
      db.session.add(suggestion_tag)
      db.session.commit()
      self.suggestion_tags_count += 1
      print(f"New suggestion {suggestion_id} <-> tag {tag_label} relation added")

  def __insert_tags_and_relation_to_suggestion(self, db, tags, suggestion_id):
    if tags is not None and len(tags) > 0:
      for tag_label in tags:
        exists = self.__get_existing_tag(tag_label.label)
        if exists is None:
          db.session.add(tag_label)
          db.session.commit()
          self.existing_tags.append(tag_label.label)
          print(f"New tag added {tag_label.label}")
        event_bo = self.__insert_event_bo_to_db(db, tag_label.label)
        if event_bo is not None:
          # lets not try to add this if event creation failed
          self.__insert_suggestion_tag_relationship(db, tag_label.label, suggestion_id, event_bo.id)

  def insert_models_to_db(self, db, models):
    bo_models_dict = self.__map_models_to_db_bo(models)
    for model in bo_models_dict:
      try:
        suggestion = model["suggestion"]
        tags = model["tags"]
        if 'meeting' in model.keys():
          meeting = model["meeting"]
          self.__insert_meeting_to_db(db, meeting)
          suggestion.meeting_id = meeting.id
        self.__insert_suggestion_to_db(db, suggestion)
        self.__insert_tags_and_relation_to_suggestion(db, tags, suggestion.id)
      except Exception as ex:
        print(str(ex))
        db.session.rollback()
      finally:
        db.session.close()
    print("RESULTS: \r\n")
    print(f"Suggestions inserted {self.suggestion_count}")
    print(f"Meetings inserted {self.meeting_count}")
    print(f"Tags inserted {len(self.existing_tags)}")