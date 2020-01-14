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
export const handleMeetingQueries = (meetingId, filters, searchWord, sort, router) => {
  let meeting = 'meeting_id:' + meetingId;
  if (filters.includes(meeting)) {
    handleQueries(filters, searchWord, sort, router);
  } else if (filters.length === 0) {
    handleQueries(meeting, searchWord, sort, router);
  } else {
    let updatedFilters = filters + '|' + meeting;
    handleQueries(updatedFilters, searchWord, sort, router);
  }
};
export const handleUserQueries = (userId, filters, searchWord, sort, router) => {
  let user = 'user_id:' + userId;
  if (filters.includes(user)) {
    handleQueries(filters, searchWord, sort, router);
  } else if (filters.length === 0) {
    handleQueries(user, searchWord, sort, router);
  } else {
    let updatedFilters = filters + '|' + user;
    handleQueries(updatedFilters, searchWord, sort, router);
  }
};
export const handleQueries = (filters, searchWord, sort, router) => {
  if (sort.length > 0) {
    handleSortedQueries(filters, searchWord, sort, router);
  } else if (sort.length === 0) {
    handleUnSortedQueries(filters, searchWord, router);
  }
};
export const handleSortedQueries = (filters, searchWord, sort, router) => {
  if (filters.length > 0 && searchWord.length > 0) {
    router.push({
      query: {
        filters: filters,
        search: searchWord,
        sort: sort
      }
    });
  } else if (filters.length > 0 && searchWord.length === 0) {
    router.push({
      query: {
        filters: filters,
        sort: sort
      }
    });
  } else if (filters.length === 0 && searchWord.length > 0) {
    router.push({
      query: {
        search: searchWord,
        sort: sort
      }
    });
  } else {
    router.push({
      query: {
        sort: sort
      }
    });
  }
};
export const handleUnSortedQueries = (filters, searchWord, router) => {
  if (filters.length > 0 && searchWord.length > 0) {
    router.push({
      query: {
        filters: filters,
        search: searchWord
      }
    });
  } else if (filters.length > 0 && searchWord.length === 0) {
    router.push({
      query: {
        filters: filters
      }
    });
  } else if (filters.length === 0 && searchWord.length > 0) {
    router.push({
      query: {
        search: searchWord
      }
    });
  } else {
    router.push({
      query: {}
    });
  }
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
export const findSelectionIndex = (splittedFilter, array) => {
  let i = 0;
  while (i !== array.length) {
    i += 1;
    if (array[i].value.toString() === splittedFilter[1].toUpperCase()) {
      return i;
    }
  }
  return 0;
};
export const findMeetingSelectionIndex = (splittedFilter, array) => {
  let i = 0;
  while (i !== array.length) {
    if (array[i].value.toString() === splittedFilter[1].toUpperCase()) {
      return i;
    }
    i += 1;
  }
  return null;
};
export const findTagSelectionIndex = (splittedFilter, array) => {
  let indexes = [];
  let tagFilters = splittedFilter[1].split('-');
  for (let i in tagFilters) {
    for (let index in array) {
      if (array[index].value === tagFilters[i].toUpperCase()) {
        index = parseInt(index, 10);
        indexes.push(index);
        break;
      }
    }
  }
  return indexes;
};
export const findSortSelectionIndex = (sort, array) => {
  let i = 0;
  while (i !== array.length) {
    if (array[i].value.toString() === sort) {
      return i;
    }
    i += 1;
  }
  return 0;
};
