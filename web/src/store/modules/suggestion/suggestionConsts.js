export const namespace = 'suggestion';

export const storeStateNames = {
  ITEMS: 'items',
  OPEN_COUNT: 'openCount',
  RESOLVED_COUNT: 'resolvedCount',
  SEARCH_QUERY: 'searchQuery'
};

export const suggestionMutations = {
  SET_SUGGESTIONS: 'setSuggestions',
  SET_OPEN_SUGGESTIONS_COUNT: 'setOpenSuggestionCount',
  SET_RESOLVED_SUGGESTIONS_COUNT: 'setResolvedSuggestionCount',
  SET_SEARCH_QUERY: 'setSearchQuery'
};

export const suggestionActions = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_OPEN_SUGGESTIONS: 'getOpenSuggestionCount',
  GET_RESOLVED_SUGGESTIONS: 'getResolvedSuggestionCount',
  GET_SORTED_SUGGESTIONS: 'getSortedSuggestions',
  GET_SEARCHED_SUGGESTIONS: 'getSearchedSuggestions',
  SET_SEARCH_QUERY: 'setSearchQuery'
};

export const suggestionGetters = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_OPEN_SUGGESTIONS_COUNT: 'getOpenSuggestionsCount',
  GET_RESOLVED_SUGGESTIONS_COUNT: 'getResolvedSuggestionsCount',
  GET_SEARCH_QUERY: 'getSearchQuery'
};