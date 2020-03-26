import { get, put, post, del, patch } from '../utils';

// For adjusting the list length on the front page.
// Remember to set this also at the SuggestionsList.vue
const defaultLimit = 25;

export default {
  getSuggestions: (offset = 0, sort = '', filters = '', searchWord = '', areaTerm = '') =>
    get({
      // eslint-disable-next-line max-len
      resource: `/suggestions?limit=${defaultLimit}&offset=${offset}&sort=${sort}&filters=${filters}&search=${searchWord}&area=${areaTerm}`
    }),
  getSuggestionsCount: (filters, searchWord) =>
    get({ resource: `/suggestions/count?filters=${filters}&search=${searchWord}` }),
  getArchivedSuggestionsCount: (filters, searchWord) =>
    get({ resource: `/suggestions/archivedCount?filters=${filters}&search=${searchWord}` }),
  getSuggestionsByUserId: (userId, offset = 0) =>
    get({ resource: `/suggestions/user=${userId}?limit=${defaultLimit}&offset=${offset}` }),
  getSuggestionById: suggestionId => get({ resource: `/suggestions/${suggestionId}` }),
  assignUserToSuggestion: (suggestionId, userId) =>
    put({ resource: `/suggestions/${suggestionId}/assign/${userId}` }),
  unassignUserFromSuggestion: suggestionId =>
    put({ resource: `/suggestions/${suggestionId}/unassign` }),
  assignSuggestionToMeeting: (suggestionId, meetingId) =>
    patch({ resource: `/suggestions/${suggestionId}`, data: { meeting_id: meetingId } }),
  getSuggestionsByMeetingId: meetingId => get({ resource: `/suggestions/meeting/${meetingId}` }),
  updateSuggestionStatus: (suggestionId, status) =>
    put({ resource: `/suggestions/${suggestionId}/status/${status}` }),
  addTagToSuggestion: (suggestionId, tag) =>
    post({ resource: `/suggestions/${suggestionId}/tags`, data: { tags: [tag] } }),
  removeTagFromSuggestion: (suggestionId, tag) =>
    del({ resource: `/suggestions/${suggestionId}/tags`, data: { tags: [tag] } }),
  getOpenSuggestions: () => get({ resource: '/suggestions/open' }),
  getResolvedSuggestions: () => get({ resource: '/suggestions/resolved' })
};
