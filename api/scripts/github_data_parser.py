import requests
from .github_models import GithubBodyModel, GithubMeetingModel, GithubIssueModel

class GithubDataParser:

  ### ctor
  def __init__(self):
    self.prefrered_labels = dict()

  ### privates
  def __parse_preferred_labels(self, value):
    if 'Ehdotettu termi suomeksi' in value:
      splitted_values = value.split('Ehdotettu termi suomeksi')
      self.prefrered_labels['fi'] = { 'value': splitted_values[1].strip() }
    if 'Ehdotettu termi ruotsiksi' in value:
      splitted_values = value.split('Ehdotettu termi ruotsiksi')
      self.prefrered_labels['sv'] = { 'value': splitted_values[1].strip() }
    if 'Ehdotettu termi englanniksi' in value:
      splitted_values = value.split('Ehdotettu termi englanniksi')
      self.prefrered_labels['en'] = { 'value': splitted_values[1].strip() }

  def __parse_alternative_labels(self, value):
    alternative_labels = ''
    splitted_values = value.split('Vaihtoehtoiset termit ja ilmaisut')
    alternative_labels = splitted_values[1].strip()
    return alternative_labels

  def __parse_related(self, value):
    related = []
    splitted_values = value.split('Vastaava käsite muussa sanastossa')
    splitted_related = splitted_values[1].split('\n')
    for vocab in splitted_related:
      splitted_vocabulary = vocab.split(' :')
      if len(splitted_vocabulary) > 1 and len(splitted_vocabulary[0]) > 3:
        related.append({
          'vocab': splitted_vocabulary[0].strip(),
          'value': splitted_vocabulary[1].strip()}
        )
    return related

  def __parse_reason(self, value):
    reason = ''
    splitted_reason = value.split('Perustelut ehdotukselle')
    reason = splitted_reason[1].strip()
    return reason

  def __parse_need_for(self, value, body):
    if 'Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)' in value:
      splitted_need_for = value.split('Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)')
      body.need_for.append(splitted_need_for[1].strip())
    if 'Tarkoitusta täsmentävä selite' in value:
      splitted_reason_qualification = value.split('Tarkoitusta täsmentävä selite')
      body.need_for.append(splitted_reason_qualification[1].strip())
    if 'Perustelut ehdotukselle' in value:
      splitted_reason_description = value.split('Perustelut ehdotukselle')
      body.need_for.append(splitted_reason_description[1].strip())

  def __parse_groups(self, value, body):
    splitted_value = value.split('Ehdotetut temaattiset ryhmät (YSA-ryhmät)')
    if len(splitted_value) > 0:
      splitted_groups = splitted_value[1].strip().split(']')
      group_value = splitted_groups[0].replace('[', '')
      group_url = splitted_groups[1].translate({ord('('): None}).translate({ord(')'): None}).split('**')[0].strip()
      body.groups.append({'value': group_value, 'uri': group_url})

  def __parse_organization(self, value):
    organization = ''
    splitted_value = value.split('Ehdottajan organisaatio')
    organization = splitted_value[1].replace('*', '').strip()
    return organization

  def __parse_body_strings(self, body_str):
    body = GithubBodyModel()
    if 'CONCEPT' in body_str:
      body.type = 'NEW'
      splitted_body_strings = body_str.split("####")
      for section in splitted_body_strings:
        if 'Ehdotettu termi suomeksi' in section:
          self.__parse_preferred_labels(section)
        if 'Ehdotettu termi ruotsiksi' in section:
          self.__parse_preferred_labels(section)
        if 'Ehdotettu termi englanniksi' in section:
          self.__parse_preferred_labels(section)
        if 'Vaihtoehtoiset termit ja ilmaisut' in section:
          body.alternative_labels = self.__parse_alternative_labels(section)
        if 'Vastaava käsite muussa sanastossa' in section:
          body.related = self.__parse_related(section)
        if 'Perustelut ehdotukselle' in section:
          body.reason = self.__parse_reason(section)
        if 'Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)' in section:
          self.__parse_need_for(section, body)
        if 'Tarkoitusta täsmentävä selite' in section:
          self.__parse_need_for(section, body)
        if 'Ehdotetut temaattiset ryhmät (YSA-ryhmät)' in section:
          self.__parse_groups(section, body)
        if '**Ehdottajan organisaatio:**' in section:
          body.organization = self.__parse_organization(section)

      if self.prefrered_labels is not None and len(self.prefrered_labels) > 0:
        body.prefrered_labels = self.prefrered_labels
    else:
      body.type = 'MODIFY'
      splitted_body_strings = body_str.split("####")
      for section in splitted_body_strings:
        if 'preflabel' in section:
          continue
        if 'Ehdotettu muutos' in section:
          continue
        if 'Perustelut ehdotukselle' in section:
          self.__parse_need_for(section, body)
          continue
        if 'Ehdottajan organisaatio' in section:
          body.organization = self.__parse_organization(section)

    return body

  def __parse_meeting(self, meeting):
    if meeting is not None:
      title = ''
      created_date = ''
      if meeting["title"] is not None and len(meeting["title"]) > 0:
        title = meeting["title"]
      if meeting["created_at"] is not None and len(meeting["created_at"]) > 0:
        created_date = meeting["created_at"]
      return GithubMeetingModel(title, created_date)
    else:
      return None

  def __map_reponse(self, json_item):
    suggestion_model = GithubIssueModel(
      json_item["title"],
      None, # json_item["state"],
      self.__parse_meeting(json_item["milestone"]),
      json_item["created_at"],
      json_item["updated_at"],
      json_item["closed_at"],
      self.__parse_body_strings(json_item["body"])
    )

    for label in json_item["labels"]:
      suggestion_model.tags.append([label["name"]])

    return suggestion_model

  ### public methods
  def fetch_data_from_github(self):
    return requests.get('https://api.github.com/repos/Finto-ehdotus/YSE/issues?per_page=100&page=1')

  def handle_response(self, response):
    models = []
    for item in response.json():
      model = self.__map_reponse(item)
      models.append(model)
    return models