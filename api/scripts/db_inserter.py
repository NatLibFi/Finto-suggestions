from api.models import Suggestion, Tag, Meeting, SuggestionTag

class DBInserter:

  def __init__(self):
    self.suggestion_count = 0
    self.meeting_count = 0


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
    suggesiton_bo.preferred_label = model.body.preferred_label
    suggesiton_bo.groups = model.body.groups
    suggesiton_bo.neededFor = ', '.join([str(x) for x in model.body.need_for])
    return suggesiton_bo

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
        bo_models.append(suggestion_models)
    return bo_models

  def insert_models_to_db(self, db, models):
    bo_models_dict = self.__map_models_to_db_bo(models)
    for model in bo_models_dict:
      try:
        suggestion = model["suggestion"]
        if 'meeting' in model.keys():
          meeting = model["meeting"]
          print(meeting)
          if meeting != None:
            db.session.add(meeting)
            suggestion.meeting_id = meeting.id
            db.session.commit()
            self.meeting_count += 1
            print(f"New meeting added {meeting.id}")
        print(suggestion)
        db.session.add(suggestion)
        db.session.commit()
        self.suggestion_count += 1
        print(f"New suggestion added {suggestion.id}")
      except Exception as ex:
        print(str(ex))
        db.session.rollback()
    print(f"Suggestions inserted {self.suggestion_count}")
    print(f"Meetings inserted {self.meeting_count}")