export const namespace = 'suggestion';

export const storeStateNames = {
  ITEMS: 'items',
  ITEM: 'item',
  SEARCH_QUERY: 'searchQuery',
  FILTERS: 'filters',
  SUGGESTIONS_SELECTED_SORT: 'suggestionsSelectedSort',
  MEETING_SUGGESTIONS_SELECTED_SORT: 'meetingSuggestionsSelectedSort'
};

export const sessionStorageKeyNames = {
  SUGGESTIONS_SELECTED_SORT: 'suggestionsSelectedSort',
  MEETING_SUGGESTIONS_SELECTED_SORT: 'meetingSuggestionsSelectedSort'
};

export const suggestionGetters = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_SUGGESTION: 'getSuggestion',
  GET_SEARCH_QUERY: 'getSearchQuery',
  GET_FILTERS: 'getFilters',
  GET_SUGGESTIONS_SELECTED_SORT: 'getSuggestionsSelectedSort',
  GET_MEETING_SUGGESTIONS_SELECTED_SORT: 'getMeetingSuggestionsSelectedSort'
};

export const suggestionMutations = {
  SET_SUGGESTIONS: 'setSuggestions',
  SET_SUGGESTION: 'setSuggestion',
  SET_SEARCH_QUERY: 'setSearchQuery',
  SET_FILTERS: 'setFilters',
  SET_SUGGESTIONS_SELECTED_SORT: 'setSuggestionsSelectedSort',
  SET_SUGGESTIONS_SELECTED_STORAGE_SORT: 'setSuggestionsSelectedStorageSort',
  SET_MEETING_SUGGESTIONS_SELECTED_SORT: 'setMeetingSuggestionsSelectedSort',
  SET_MEETING_SUGGESTIONS_SELECTED_STORAGE_SORT: 'setMeetingSuggestionsSelectedStorageSort'
};

export const suggestionActions = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_SUGGESTIONS_BY_USER_ID: 'getSuggestionsByUserId',
  GET_SORTED_SUGGESTIONS_BY_USER_ID: 'getSortedSuggestionsByUserId',
  GET_SORTED_SUGGESTIONS: 'getSortedSuggestions',
  GET_SUGGESTION_BY_ID: 'getSuggestionById',
  ASSIGN_SUGGESTION_TO_USER: 'assignSuggestionToUser',
  UNASSIGN_SUGGESTION_FROM_USER: 'unassignSuggestionFromUser',
  GET_SUGGESTIONS_SELECTED_SORT: 'getSuggestionsSelectedSort',
  SET_SUGGESTIONS_SELECTED_SORT: 'setSuggestionsSelectedSort',
  GET_SUGGESTIONS_BY_MEETING_ID: 'getSuggestionsByMeetingId',
  GET_SORTED_SUGGESTIONS_BY_MEETING_ID: 'getSortedSuggestionsByMeetingId',
  GET_MEETING_SUGGESTIONS_SELECTED_SORT: 'getMeetingSuggestionsSelectedSort',
  SET_MEETING_SUGGESTIONS_SELECTED_SORT: 'setMeetingSuggestionsSelectedSort',
  SET_SUGGESTION_ACCEPTED: 'setSuggestionAccpeted',
  SET_SUGGESTION_REJECTED: 'setSuggestionRejected',
  SET_SUGGESTION_RETAINED: 'setSuggestionRetained'
};
