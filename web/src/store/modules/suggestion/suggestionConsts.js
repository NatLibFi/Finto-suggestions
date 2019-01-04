export const namespace = 'suggestion';

export const storeStateNames = {
  ITEMS: 'items',
  ITEM: 'item',
  SEARCH_QUERY: 'searchQuery',
  FILTERS: 'filters',
  PAGINATED_ITEMS: 'paginated_items',
  SELECTED_SORT: 'selectedSort'
};

export const sessionStorageKeyNames = {
  SELECTED_SORT: 'selectedSort'
};

export const suggestionGetters = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_SUGGESTION: 'getSuggestion',
  GET_SEARCH_QUERY: 'getSearchQuery',
  GET_FILTERS: 'getFilters',
  GET_PAGINATION_SUGGESTIONS: 'getPaginationSuggestions',
  GET_SELECTED_SORT: 'getSelectedSort'
};

export const suggestionMutations = {
  SET_SUGGESTIONS: 'setSuggestions',
  SET_SUGGESTION: 'setSuggestion',
  SET_SEARCH_QUERY: 'setSearchQuery',
  SET_FILTERS: 'setFilters',
  SET_PAGINATION_SUGGESTIONS: 'setPaginationSuggestions',
  SET_SELECTED_SORT: 'setSelectedSort',
  SET_SELECTED_SORT_TO_STORAGE: 'setSelectedSortToStorage'
};

export const suggestionActions = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_SORTED_SUGGESTIONS: 'getSortedSuggestions',
  GET_SUGGESTION_BY_ID: 'getSuggestionById',
  ASSIGN_SUGGESTION_TO_USER: 'assignSuggestionToUser',
  UNASSIGN_SUGGESTION_FROM_USER: 'unassignSuggestionFromUser',
  GET_SELECTED_SORT_KEY: 'getSelectedSortKey',
  SET_SELECTED_SORT_KEY: 'setSelectedSortKey',
  GET_SUGGESTIONS_BY_MEETING_ID: 'getSuggestionsByMeetingId',
  GET_SORTED_SUGGESTIONS_BY_MEETING_ID: 'getSortedSuggestionsByMeetingId'
};
