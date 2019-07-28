export const namespace = 'suggestion';

export const storeStateNames = {
  ITEMS: 'items',
  ITEM: 'item',
  SEARCH_QUERY: 'searchQuery',
  FILTERS: 'filters',
  SUGGESTIONS_SELECTED_SORT: 'suggestionsSelectedSort',
  MEETING_SUGGESTIONS_SELECTED_SORT: 'meetingSuggestionsSelectedSort',
  FILTERED_ITEMS: 'filteredItems'
};

export const sessionStorageKeyNames = {
  SUGGESTIONS_SELECTED_SORT: 'suggestionsSelectedSort',
  MEETING_SUGGESTIONS_SELECTED_SORT: 'meetingSuggestionsSelectedSort',
  SELECTED_FILTERS: 'selectedFilters'
};

export const suggestionGetters = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_SUGGESTIONS_COUNT: 'getSuggestionsCount',
  GET_SUGGESTION: 'getSuggestion',
  GET_SEARCH_QUERY: 'getSearchQuery',
  GET_FILTERS: 'getFilters',
  GET_SUGGESTIONS_SELECTED_SORT: 'getSuggestionsSelectedSort',
  GET_MEETING_SUGGESTIONS_SELECTED_SORT: 'getMeetingSuggestionsSelectedSort',
  GET_FILTERED_ITEMS: 'getFilteredItems'
};

export const suggestionMutations = {
  SET_SUGGESTIONS: 'setSuggestions',
  SET_SUGGESTIONS_COUNT: 'setSuggestionsCount',
  SET_SUGGESTION: 'setSuggestion',
  SET_SEARCH_QUERY: 'setSearchQuery',
  SET_FILTERS: 'setFilters',
  SET_SUGGESTIONS_SELECTED_SORT: 'setSuggestionsSelectedSort',
  SET_SUGGESTIONS_SELECTED_STORAGE_SORT: 'setSuggestionsSelectedStorageSort',
  SET_MEETING_SUGGESTIONS_SELECTED_SORT: 'setMeetingSuggestionsSelectedSort',
  SET_MEETING_SUGGESTIONS_SELECTED_STORAGE_SORT: 'setMeetingSuggestionsSelectedStorageSort',
  SET_FILTERED_ITEMS: 'setFilteredItems',
  SET_SELECTED_STORAGE_FILTERS: 'setSelectedStorageFilters'
};

export const suggestionActions = {
  GET_SUGGESTIONS: 'getSuggestions',
  GET_SUGGESTIONS_COUNT: 'getSuggestionsCount',
  GET_SUGGESTIONS_BY_USER_ID: 'getSuggestionsByUserId',
  GET_SUGGESTION_BY_ID: 'getSuggestionById',
  ASSIGN_SUGGESTION_TO_USER: 'assignSuggestionToUser',
  UNASSIGN_SUGGESTION_FROM_USER: 'unassignSuggestionFromUser',
  ASSIGN_SUGGESTION_TO_MEETING: 'assignSuggestionToMeeting',
  GET_SUGGESTIONS_SELECTED_SORT: 'getSuggestionsSelectedSort',
  SET_SUGGESTIONS_SELECTED_SORT: 'setSuggestionsSelectedSort',
  GET_SUGGESTIONS_BY_MEETING_ID: 'getSuggestionsByMeetingId',
  GET_MEETING_SUGGESTIONS_SELECTED_SORT: 'getMeetingSuggestionsSelectedSort',
  SET_MEETING_SUGGESTIONS_SELECTED_SORT: 'setMeetingSuggestionsSelectedSort',
  SET_SUGGESTION_STATUS: 'setSuggestionStatus',
  GET_SELECTED_FILTERS: 'getSelectedFilters',
  SET_SELECTED_FILTERS: 'setSelectedFilters',
  GET_OPEN_SUGGESTIONS: 'getOpenSuggestions',
  GET_RESOLVED_SUGGESTIONS: 'getResolvedSuggestions',
  RESET_SUGGESTION_LISTING: 'resetSuggestionListing'
};
