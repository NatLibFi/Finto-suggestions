export const suggestionStateStatus = {
  ACCEPTED: 'ACCEPTED',
  REJECTED: 'REJECTED',
  RETAINED: 'RETAINED'
};

export const suggestionStateStatusToString = {
  ACCEPTED: 'Hyväksytty',
  REJECTED: 'Hylätty',
  RETAINED: 'Jää ehdotukseksi'
};

export const suggestionType = {
  NEW: 'NEW',
  MODIFY: 'MODIFY'
};

export const suggestionTypeToString = {
  NEW: 'Käsite-ehdotus',
  MODIFY: 'Muutosehdotus'
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
