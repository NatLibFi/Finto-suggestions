export const namespace = 'suggestion';

export const storeStateNames = {
  ITEMS: 'items',
  OPEN_COUNT: 'openCount',
  RESOLVED_COUNT: 'resolvedCount',
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
  GET_OPEN_SUGGESTIONS_COUNT: 'getOpenSuggestionsCount',
  GET_RESOLVED_SUGGESTIONS_COUNT: 'getResolvedSuggestionsCount',
  GET_SEARCH_QUERY: 'getSearchQuery',
  GET_FILTERS: 'getFilters',
  GET_PAGINATION_SUGGESTIONS: 'getPaginationSuggestions',
  GET_SELECTED_SORT: 'getSelectedSort'
};

export const suggestionMutations = {
  SET_SUGGESTIONS: 'setSuggestions',
  SET_OPEN_SUGGESTIONS_COUNT: 'setOpenSuggestionCount',
  SET_RESOLVED_SUGGESTIONS_COUNT: 'setResolvedSuggestionCount',
  SET_SEARCH_QUERY: 'setSearchQuery',
  SET_FILTERS: 'setFilters',
  SET_PAGINATION_SUGGESTIONS: 'setPaginationSuggestions',
  SET_SELECTED_SORT: 'setSelectedSort'
};

export const suggestionActions = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_OPEN_SUGGESTIONS: 'getOpenSuggestionCount',
  GET_RESOLVED_SUGGESTIONS: 'getResolvedSuggestionCount',
  GET_SORTED_SUGGESTIONS: 'getSortedSuggestions',
  GET_SUGGESTION_BY_ID: 'getSuggestionById',
  GET_SELECTED_SORT_KEY: 'getSelectedSortKey',
  SET_SELECTED_SORT_KEY: 'setSelectedSortKey'
};
