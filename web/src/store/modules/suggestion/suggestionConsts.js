export const namespace = 'suggestion';

export const storeStateNames = {
  ITEMS: 'items',
  OPEN_COUNT: 'openCount',
  RESOLVED_COUNT: 'resolvedCount',
  SEARCH_QUERY: 'searchQuery',
  FILTERS: 'filters'
};

export const suggestionGetters = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_OPEN_SUGGESTIONS_COUNT: 'getOpenSuggestionCount',
  GET_RESOLVED_SUGGESTIONS_COUNT: 'getResolvedSuggestionCount',
  GET_SEARCH_QUERY: 'getSearchQuery',
  GET_FILTERS: 'getFilters'
};

export const suggestionMutations = {
  SET_SUGGESTIONS: 'setSuggestions',
  SET_OPEN_SUGGESTIONS_COUNT: 'setOpenSuggestionCount',
  SET_RESOLVED_SUGGESTIONS_COUNT: 'setResolvedSuggestionCount',
  SET_SEARCH_QUERY: 'setSearchQuery',
  SET_FILTERS: 'setFilters'
};

export const suggestionActions = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_OPEN_SUGGESTIONS: 'getOpenSuggestionCount',
  GET_RESOLVED_SUGGESTIONS: 'getResolvedSuggestionCount',
  GET_SORTED_SUGGESTIONS: 'getSortedSuggestions',
  GET_SEARCHED_SUGGESTIONS: 'getSearchedSuggestions',
  GET_FILTERED_SUGGESTIONS: 'getFilteredSuggestions'
};
