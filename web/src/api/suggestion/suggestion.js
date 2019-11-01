import { get, put, post, del, patch } from '../utils';

const defaultLimit = 15;

// function toUnicode(value){
//   value = value.toLowerCase();
//   value = value.replace(/ä/g, '\u00e4');
//   value = value.replace(/%C3%A4/g, '\u00e4');
//   value = value.replace(/Ä/g, '\u00C4');
//   value = value.replace(/ö/g, '\u00f6');
//   value = value.replace(/Ö/g, '\u00d6');
//   value = value.replace(/å/g, '\u00e5');
//   value = value.replace(/Å/g, '\u00c5');
//   return value;
// }

export default {
  getSuggestions: (offset = 0, sort = '', filters = '', searchWord = '') =>
    get({
      // eslint-disable-next-line
      resource: `/suggestions?limit=${defaultLimit}&offset=${offset}&sort=${sort}&filters=${filters}&search=${searchWord}`
      // resource: `/suggestions?search=${toUnicode(searchWord)}`
    }),
  getSuggestionsCount: (filters, searchWord) =>
    get({ resource: `/suggestions/count?filters=${filters}&search=${searchWord}` }),
  getSuggestionsByUserId: (userId, offset = 0) =>
    get({ resource: `/suggestions/user=${userId}?limit=${defaultLimit}&offset=${offset}` }),
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
