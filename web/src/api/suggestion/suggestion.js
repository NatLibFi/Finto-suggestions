import { get, put, post, del, patch } from '../utils';

const defaultLimit = 15;

export default {
  getSuggestions: (offset = 0, sort = '', filters = '', searchWord = '') =>
    get({
      // eslint-disable-next-line
      resource: `/suggestions?limit=${defaultLimit}&offset=${offset}&sort=${sort}&filters=${filters}&search=${searchWord}`
    }),
  getSuggestionsCount: (filters, searchWord) =>
    get({ resource: `/suggestions/count?filters=${filters}&search=${searchWord}` }),
  getSortedSuggestions: (sort, offset) =>
    get({ resource: `/suggestions?limit=${defaultLimit}&sort=${sort}&offset=${offset}` }),
  getSuggestionsByUserId: (userId, offset = 0) =>
    get({ resource: `/suggestions/user=${userId}?limit=${defaultLimit}&offset=${offset}` }),
  getSortedSuggestionByUserId: (userId, sort) =>
    get({ resource: `/suggestions/user=${userId}?sort=${sort}` }),
  getSuggestionById: suggestionId => get({ resource: `/suggestions/${suggestionId}` }),
  assignUserToSuggestion: (suggestionId, userId) =>
    put({ resource: `/suggestions/${suggestionId}/assign/${userId}` }),
  unassignUserFromSuggestion: suggestionId =>
    put({ resource: `/suggestions/${suggestionId}/unassign` }),
  assignSuggestionToMeeting: (suggestionId, meetingId) =>
    patch({ resource: `/suggestions/${suggestionId}`, data: { meeting_id: meetingId } }),
  getSuggestionByMeetingId: meetingId => get({ resource: `/suggestions/meeting/${meetingId}` }),
  updateSuggestionStatus: (suggestionId, status) =>
    put({ resource: `/suggestions/${suggestionId}/status/${status}` }),
  addTagToSuggestion: (suggestionId, tag) =>
    post({ resource: `/suggestions/${suggestionId}/tags`, data: { tags: [tag] } }),
  removeTagFromSuggestion: (suggestionId, tag) =>
    del({ resource: `/suggestions/${suggestionId}/tags`, data: { tags: [tag] } }),
  getOpenSuggestions: () => get({ resource: '/suggestions/open' }),
  getResolvedSuggestions: () => get({ resource: '/suggestions/resolved' })
};
