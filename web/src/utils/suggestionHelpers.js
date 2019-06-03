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
  MODIFY: 'Muutosehdotus'
};

export const suggestionTypeToStyleClass = {
  NEW: 'type-new',
  MODIFY: 'type-modify'
};

export const filterType = {
  STATUS: 'status',
  TAGS: 'tags',
  TYPE: 'type',
  MEETING: 'meeting',
  SEARCH: 'search'
};

/* Helper method for calculating the offset for pagination */
export const offsetByPagination = page => {
  if (page > 1) {
    return (page - 1) * 15;
  }
  return 0;
};

/*
 * Helper method to calculate on place open and resolved count from suggestions
 * Return null if items count is empty
 */
export const calculateOpenAndResolvedSuggestionCounts = items => {
  if (items && items.length > 0) {
    const openCount = items.filter(
      i => i.status === suggestionStateStatus.READ || i.status === suggestionStateStatus.RECEIVED
    ).length;
    const resolvedCount = items.filter(
      i =>
        i.status === suggestionStateStatus.ACCEPTED ||
        i.status === suggestionStateStatus.REJECTED ||
        i.status === suggestionStateStatus.RETAINED ||
        i.status === suggestionStateStatus.ARCHIVED
    ).length;
    return { openCount, resolvedCount };
  }
  return null;
};
