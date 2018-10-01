export const namespace = 'suggestion';

export const storeStateNames = {
  ITEMS: 'items',
  OPEN_COUNT: 'openCount',
  RESOLVED_COUNT: 'resolvedCount'
};

export const suggestionMutations = {
  SET_SUGGESTIONS: 'setSuggestions',
  SET_OPEN_SUGGESTIONS_COUNT: 'setOpenSuggestionCount',
  SET_RESOLVED_SUGGESTIONS_COUNT: 'setResolvedSuggestionCount'
};

export const suggestionActions = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_OPEN_SUGGESTIONS: 'getOpenSuggestionCount',
  GET_RESOLVED_SUGGESTIONS: 'getResolvedSuggestionCount',
  GET_SORTED_SUGGESTIONS: 'getSortedSuggestions'
};

export const suggestionGetters = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_OPEN_SUGGESTIONS_COUNT: 'getOpenSuggestionsCount',
  GET_RESOLVED_SUGGESTIONS_COUNT: 'getResolvedSuggestionsCount'
};
