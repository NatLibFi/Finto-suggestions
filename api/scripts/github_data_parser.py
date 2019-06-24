import requests, math, os
from .github_models import GithubBodyModel, GithubMeetingModel, GithubIssueModel

class GithubDataParser:

  ### ctor
  def __init__(self):
    self.prefrered_labels = dict()
    self.last_request_completed = False

  ### privates
  def __parse_preferred_labels(self, value, body):
    if 'Ehdotettu termi suomeksi' in value:
      splitted_values = value.split('Ehdotettu termi suomeksi')
      body.preferred_labels['fi'] = { 'value': splitted_values[1].strip() }
    if 'Ehdotettu termi ruotsiksi' in value:
      splitted_values = value.split('Ehdotettu termi ruotsiksi')
      body.preferred_labels['sv'] = { 'value': splitted_values[1].strip() }
    if 'Ehdotettu termi englanniksi' in value:
      splitted_values = value.split('Ehdotettu termi englanniksi')
      body.preferred_labels['en'] = splitted_values[1].strip()
    if 'preflabel' in value:
      splitted_values = value.split('preflabel')
      splitted_parsed_value = splitted_values[1].replace('[', '').replace(']', '').split('(')
      body.preferred_labels['fi'] = {
        'value': splitted_parsed_value[0].strip(),
        'uri': splitted_parsed_value[1].replace(')', '').strip()
      }

  def __parse_alternative_labels(self, value, body):
    splitted_value = value.replace('\n\n', '').split('Vaihtoehtoiset termit ja ilmaisut')
    if len(splitted_value) > 0:
      group_values = splitted_value[1].strip().split(',')
      for value in group_values:
        body.alternative_labels.append({'value': value})

  def __parse_broader(self, value, body):
    splitted_value = value.split('Ehdotettu yläkäsite YSOssa (LT)')
    if len(splitted_value) > 0:
      splitted_broader = splitted_value[1].replace('(', '').replace(')', '').split('[')[1:]
      for broader in splitted_broader:
        splitted_values = broader.strip().split(']')
        group_value = splitted_values[0]
        group_url = splitted_values[1]
        body.broader_labels.append({'value': group_value, 'uri': group_url})

  def __parse_narrower(self, value, body):
    splitted_value = value.split('Alakäsitteet (ST)')
    if len(splitted_value) > 0:
      splitted_narrower = splitted_value[1].replace('(', '').replace(')', '').split('[')[1:]
      for narrower in splitted_narrower:
        splitted_values = narrower.strip().split(']')
        group_value = splitted_values[0]
        group_url = splitted_values[1]
        body.narrower_labels.append({'value': group_value, 'uri': group_url})

  def __parse_related(self, value, body):
    splitted_value = value.split('Assosiatiiviset (RT)')
    if len(splitted_value) > 0:
      splitted_related = splitted_value[1].replace('(', '').replace(')', '').split('[')[1:]
      for related in splitted_related:
        splitted_values = related.strip().split(']')
        group_value = splitted_values[0]
        group_url = splitted_values[1]
        body.related_labels.append({'value': group_value, 'uri': group_url})

  def __parse_matches(self, value, body):
    splitted_value = value.split('Vastaava käsite muussa sanastossa')
    splitted_matches = splitted_value[1].replace('\n\n', '').split('\n')
    for value in splitted_matches:
      if len(value) > 0:
        value = value.replace('<', '').replace('>', '')
        if 'http' in value:
          splitted_match = value.strip().split('http')
          match_vocab = splitted_match[0].replace(':', '').rstrip()
          match_value = 'http' + splitted_match[1]
        else:
          match_vocab = value.strip()
          match_value = ''
        body.exact_matches.append({'vocab': match_vocab, 'value': match_value})

  def __parse_description(self, value):
    description = ''
    if 'Perustelut ehdotukselle' in value:
      splitted_description = value.split('Perustelut ehdotukselle')
      description = splitted_description[1].strip()
    if 'Ehdotettu muutos' in value:
      splitted_description = value.split('Ehdotettu muutos')
      description = splitted_description[1].strip()
    return description

  def __parse_remove_name_and_email_from_body(self, body_str):
    if 'Ehdottajan nimi' in body_str:
      split_remove_sender_name = body_str.split('Ehdottajan nimi')
      body_str = split_remove_sender_name[0].replace('*', '').strip()
    if 'Ehdottajan sähköpostiosoite' in body_str:
      split_remove_sender_email = body_str.split('Ehdottajan sähköpostiosoite')
      body_str = split_remove_sender_email[0].replace('*', '').strip()
    if 'Ehdottaja' in body_str:
      split_remove_sender_email = body_str.split('Ehdottaja')
      body_str = split_remove_sender_email[0].replace('*', '').strip()
    if 'fromname' in body_str:
      split_remove_sender_email = body_str.split('fromname')
      body_str = split_remove_sender_email[0].replace('*', '').strip()
    if 'fromemail' in body_str:
      split_remove_sender_email = body_str.split('fromemail')
      body_str = split_remove_sender_email[0].replace('*', '').strip()
    return body_str

  def __parse_remove_org_and_term_suggestion_from_reason(self, value):
    if 'Ehdottajan organisaatio' in value:
      splitted_remove_org = value.split('Ehdottajan organisaatio')
      parsed_value = splitted_remove_org[0].replace('*','').replace(':','').strip()
      return parsed_value
    if 'Termiehdotus Fintossa' in value:
      splitted_remove_term_on_finto = value.split('Termiehdotus Fintossa')
      parsed_value = splitted_remove_term_on_finto[0].replace('*', '').strip()
      return parsed_value

  def __parse_reason(self, value, body):
    if 'Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)' in value:
      splitted_reasons = value.split('Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)')
      parsed_value = self.__parse_remove_org_and_term_suggestion_from_reason(splitted_reasons[1].strip())
      if parsed_value is None:
        body.reason = splitted_reasons[1].strip()
      else:
        body.reason = parsed_value
    if 'Perustelut ehdotukselle' in value:
      splitted_reason_description = value.split('Perustelut ehdotukselle')
      parsed_value = self.__parse_remove_org_and_term_suggestion_from_reason(splitted_reason_description[1].strip())
      if parsed_value is None:
        body.reason = splitted_reason_description[1].strip()
      else:
        body.reason = parsed_value

  def __parse_scope(self, value, body):
    if 'Tarkoitusta täsmentävä selite' in value:
      splitted_scope_note = value.split('Tarkoitusta täsmentävä selite')
      body.scope_note = splitted_scope_note[1].strip()

  def __parse_groups(self, value, body):
    splitted_value = value.split('Ehdotetut temaattiset ryhmät (YSA-ryhmät)')[1].split('**')[0]
    if len(splitted_value) > 0:
      splitted_groups = splitted_value.replace('(', '').replace(')','').split('[')[1:]
      for group in splitted_groups:
        splitted_values = group.strip().split(']')
        group_value = splitted_values[0]
        group_url = splitted_values[1]
        body.groups.append({'value': group_value, 'uri': group_url})

  def __parse_organization(self, value, body):
    organization = ''
    if 'Ehdottajan sähköpostiosoite' in value:
      value = value.split('Ehdottajan sähköpostiosoite')[0]
    if 'Ehdottajan organisaatio' in value:
      splitted_value = value.split('Ehdottajan organisaatio')
      organization = splitted_value[1].replace('*', '').replace(':', '').strip().split('####')[0]
    if 'fromorg' in value:
      splitted_value = value.split('fromorg')
      organization = splitted_value[1].replace('*', '').replace(':', '').strip().split('####')[0]
    if 'Termiehdotus Fintossa' in organization:
      splitted_organization = organization.split('Termiehdotus Fintossa')
      organization = splitted_organization[0].replace('*', '').replace(':', '').strip().split('####')[0]
    body.organization = organization

  def __parse_yse_term(self, value, body):
    splitted_value = value.split('Termiehdotus Fintossa')
    splitted_yse_term_value = splitted_value[1].split('\n')[0].split(']')
    yse_term = {
      'value': splitted_yse_term_value[0].replace('[','').replace(']','').replace('*','').replace(':','') .strip(),
      'uri': splitted_yse_term_value[1].replace('(','').replace(')','').strip()
    }
    body.yse_term = yse_term

  def __parse_voyager_body_strings(self, body_str):
    body = GithubBodyModel()

    if 'Ehdottajan nimi' or 'Ehdottajan sähköpostiosoite' or 'fromname' or 'fromemail' in body_str:
      body_str = self.__parse_remove_name_and_email_from_body(body_str)

    if 'Termiehdotus Fintossa' in body_str:
      self.__parse_yse_term(body_str, body)

    body.type = 'NEW'
    body.scope_note = 'Tuotu Voaygerista'
    splitted_body_strings = body_str.split("####")
    for section in splitted_body_strings:
      if 'Ehdotettu termi suomeksi' in section:
        self.__parse_preferred_labels(section, body)
      if 'Ehdotetut temaattiset ryhmät (YSA-ryhmät)' in section:
        self.__parse_groups(section, body)

    return body

  def __parse_to_json_labels(self, value):
    values = []
    splitted_value = value.split('\n')

    for value in splitted_value:
      if '[' in value:
        splitted_labels = value.split('[')[1].split(']')
        if len(splitted_labels) > 1:
          values.append({
            'value': splitted_labels[0].strip(),
            'uri': splitted_labels[1].replace('(', '').replace(')', '').strip()
          })
        elif len(splitted_labels) == 1:
          values.append({
            'value': splitted_labels[0].strip()
          })
    return values

  def __parse_created_datetime(self, value, body):
    if 'Luontipäivämäärä' in value:
      splitted_value = value.split('Luontipäivämäärä')
      date_value = splitted_value[1].replace(':','').replace('*','')
      splitted_date_value = date_value.split('\n')
      body.created_date = splitted_date_value[0].strip()

  def __parse_modified_datetime(self, value, body):
    if 'Muokkauspäivämäärä' in value:
      splitted_value = value.split('Muokkauspäivämäärä')
      date_value = splitted_value[1].replace(':','').replace('*','')
      splitted_date_value = date_value.split('\n')

      if ',' in splitted_date_value[0]:
        splitted_modified_date = splitted_date_value[0].split(',')
        body.modified_date = splitted_modified_date.pop().strip()
      else:
        body.modified_date = splitted_date_value[0].strip()

  def __parse_voyager_id(self, value, body):
    if 'Voyager-id' in value:
      splitted_values = value.split('Voyager-id')
      raw_value = splitted_values[1].split('\n')[0]
      voyager_id_value = raw_value.replace(':','').replace('*','').strip()
      body.voyager_id = voyager_id_value

  def __parse_body_strings(self, body_str):
    body = GithubBodyModel()

    if 'Ehdottajan organisaatio' or 'fromorg' in body_str:
      self.__parse_organization(body_str, body)

    if 'Ehdottajan nimi' or 'Ehdottajan sähköpostiosoite' or 'fromname' or 'fromemail' in body_str:
      body_str = self.__parse_remove_name_and_email_from_body(body_str)

    if 'Termiehdotus Fintossa' in body_str:
      self.__parse_yse_term(body_str, body)

    splitted_body_strings = body_str.split("####")

    if 'CONCEPT' in body_str or 'GEO' in body_str:
      body.type = 'NEW'
      for section in splitted_body_strings:
        if 'Ehdotettu termi suomeksi' in section:
          self.__parse_preferred_labels(section, body)
        if 'Ehdotettu termi ruotsiksi' in section:
          self.__parse_preferred_labels(section, body)
        if 'Ehdotettu termi englanniksi' in section:
          self.__parse_preferred_labels(section, body)
        if 'Vaihtoehtoiset termit ja ilmaisut' in section:
          self.__parse_alternative_labels(section, body)
        if 'Ehdotettu yläkäsite YSOssa (LT)' in section:
          self.__parse_broader(section, body)
        if 'Alakäsitteet (ST)' in section:
          self.__parse_narrower(section, body)
        if 'Assosiatiiviset (RT)' in section:
          self.__parse_related(section, body)
        if 'Vastaava käsite muussa sanastossa' in section:
          self.__parse_matches(section, body)
        if 'Perustelut ehdotukselle' in section:
          body.description = self.__parse_description(section)
        if 'Aineisto jonka kuvailussa käsitettä tarvitaan (esim. nimeke tai URL)' in section:
          self.__parse_reason(section, body)
        if 'Tarkoitusta täsmentävä selite' in section:
          self.__parse_scope(section, body)
        if 'Ehdotetut temaattiset ryhmät (YSA-ryhmät)' in section:
          self.__parse_groups(section, body)

    else:
      body.type = 'MODIFY'
      for section in splitted_body_strings:
        if 'preflabel' in section:
          self.__parse_preferred_labels(section, body)
        if 'Ehdotettu muutos' in section:
          body.description = self.__parse_description(section)
        if 'Perustelut ehdotukselle' in section:
          self.__parse_reason(section, body)

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

  def __parse_status(self, status, tags):
    mapped_status = 'RECEIVED'
    if status is 'closed':
      mapped_status = 'ARCHIVED'
    else:
      for tag in tags:
        if 'vastaanotettu' in tag["name"]:
          mapped_status = 'READ'
        if 'jää termiehdotukseksi' in tag["name"]:
          mapped_status = 'RETAINED'
        if 'hyväksytty' in tag["name"]:
          mapped_status = 'ACCEPTED'
        if 'hylätty' in tag["name"]:
          mapped_status = 'REJECTED'
    return mapped_status


  def __fetch_data_from_github(self, page = 1):
    user = os.environ.get('GITHUB_USERNAME')
    personal_token = os.environ.get('GITHUB_PERSONAL_TOKEN')
    return requests.get(f'https://api.github.com/repos/Finto-ehdotus/YSE/issues?per_page=100&state=all&page={page}', auth=(user, personal_token))

  def __map_response(self, json_item):
    if 'Voyager-id' in json_item["body"]:
      suggestion_model = GithubIssueModel(
        json_item["title"],
        self.__parse_status(json_item["state"], json_item["labels"]),
        self.__parse_meeting(json_item["milestone"]),
        json_item["created_at"],
        json_item["updated_at"],
        json_item["closed_at"],
        self.__parse_voyager_body_strings(json_item["body"])
      )
    else:
      suggestion_model = GithubIssueModel(
        json_item["title"],
        self.__parse_status(json_item["state"], json_item["labels"]),
        self.__parse_meeting(json_item["milestone"]),
        json_item["created_at"],
        json_item["updated_at"],
        json_item["closed_at"],
        self.__parse_body_strings(json_item["body"])
      )

    for label in json_item["labels"]:
      # don't add unnecessary tags
      if 'uusi' in label["name"]:
        break
      elif 'muutos' in label["name"]:
        break
      elif 'hyväksytty' in label["name"]:
        break
      elif 'jää termiehdotukseksi' in label["name"]:
        break
      # yet append the correct ones
      suggestion_model.tags.append(label["name"])

    if 'GEO' in json_item["body"] and 'maantieteellinen' not in suggestion_model.tags:
      suggestion_model.tags.append('maantieteellinen')

    return suggestion_model

  def __parse_count_from_response_headers(self, headers):
    if headers is not None and len(headers) > 0:
      return int(headers["Link"].split(",")[1].split("&page=")[1].split(">")[0])
    return 0

  ### public methods
  def handle_response(self, arg_loop_count, id = None):
    models = []

    loop_count = 0
    if arg_loop_count is not None and arg_loop_count > 0:
      loop_count = arg_loop_count
    else:
      response = self.__fetch_data_from_github()
      loop_count = self.__parse_count_from_response_headers(response.headers)

    i = 1
    while i <= loop_count:
      if self.last_request_completed == False:
        response = self.__fetch_data_from_github(i)
        if len(response.json()) > 0:
          print(f"Issue batch fetch {i}/{loop_count}")
          i+= 1
          for json_item in response.json():
            model = self.__map_response(json_item)
            models.append(model)
        else:
          self.last_request_completed = True
      else:
        response = self.__fetch_data_from_github()
        loop_count = self.__parse_count_from_response_headers(response.headers)

      i = 1
      while i <= loop_count:
        if self.last_request_completed == False:
          response = self.__fetch_data_from_github(i)
          if len(response.json()) > 0:
            print(f"Issue batch fetch {i}/{loop_count}")
            i+= 1
            for json_item in response.json():
              model = self.__map_reponse(json_item)
              models.append(model)
          else:
            self.last_request_completed = True
        else:
          break
    else:
      response = self.__fetch_data_from_github_by_id(id)
      model = self.__map_reponse(response.json())
      models.append(model)

    return models