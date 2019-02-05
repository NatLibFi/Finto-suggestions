export const suggestionStateStatus = {
  RECEIVED: 'RECEIVED',
  READ: 'READ',
  ACCEPTED: 'ACCEPTED',
  REJECTED: 'REJECTED',
  RETAINED: 'RETAINED',
  ARCHIVED: 'ARCHIVED'
};

export const suggestionStateStatusToString = {
  RECEIVED: 'Käsittelemätön',
  READ: 'Vastaanotettu',
  ACCEPTED: 'Hyväksytty',
  REJECTED: 'Hylätty',
  RETAINED: 'Jää ehdotukseksi',
  ARCHIVED: 'Arkistoitu'
};

export const suggestionType = {
  NEW: 'NEW',
  MODIFY: 'MODIFY'
};

export const suggestionTypeToString = {
  NEW: 'Käsite-ehdotus',
  MODIFY: 'Käsitemuutos'
};

export const suggestionTypeToStyleClass = {
  NEW: 'type-new',
  MODIFY: 'type-modify'
};

export const filterType = {
  STATUS: 'status',
  TAG: 'tag',
  TYPE: 'type',
  MEETING: 'meeting',
  SEARCH: 'search'
};
