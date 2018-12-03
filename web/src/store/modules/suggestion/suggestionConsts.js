export const namespace = 'suggestion';

export const storeStateNames = {
  ITEMS: 'items',
  ITEM: 'item',
  OPEN_COUNT: 'openCount',
  RESOLVED_COUNT: 'resolvedCount',
  SEARCH_QUERY: 'searchQuery',
  FILTERS: 'filters',
  PAGINATED_ITEMS: 'paginated_items'
};

export const suggestionGetters = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_SUGGESTION: 'getSuggestion',
  GET_OPEN_SUGGESTIONS_COUNT: 'getOpenSuggestionsCount',
  GET_RESOLVED_SUGGESTIONS_COUNT: 'getResolvedSuggestionsCount',
  GET_SEARCH_QUERY: 'getSearchQuery',
  GET_FILTERS: 'getFilters',
  GET_PAGINATION_SUGGESTIONS: 'getPaginationSuggestions'
};

export const suggestionMutations = {
  SET_SUGGESTIONS: 'setSuggestions',
  SET_SUGGESTION: 'setSuggestion',
  SET_OPEN_SUGGESTIONS_COUNT: 'setOpenSuggestionCount',
  SET_RESOLVED_SUGGESTIONS_COUNT: 'setResolvedSuggestionCount',
  SET_SEARCH_QUERY: 'setSearchQuery',
  SET_FILTERS: 'setFilters',
  SET_PAGINATION_SUGGESTIONS: 'setPaginationSuggestions'
};

export const suggestionActions = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_OPEN_SUGGESTIONS: 'getOpenSuggestionCount',
  GET_RESOLVED_SUGGESTIONS: 'getResolvedSuggestionCount',
  GET_SORTED_SUGGESTIONS: 'getSortedSuggestions',
  GET_SUGGESTION_BY_ID: 'getSuggestionById',
  ASSIGN_SUGGESTION_TO_USER: 'assignSuggestionToUser',
  UNASSIGN_SUGGESTION_FROM_USER: 'unassignSuggestionFromUser'
};
