import { get, put, post, del, patch } from '../utils';
import { asciiUriEncoding } from '../helper';
import { sortingKeys } from '../../utils/sortingHelper';

const defaultLimit = 15;

export default {
  getSuggestions: (
    offset = 0,
    sortValue = sortingKeys.NEWEST_FIRST,
    filters = '',
    searchWord = ''
  ) =>
    get({
      // eslint-disable-next-line
      resource: `/suggestions?limit=${defaultLimit}&offset=${offset}&sort=${sortValue}&filters=${filters}&search=${searchWord}`
    }),
  getSuggestionsCount: (filters, searchWord) =>
    get({ resource: `/suggestions/count?filters=${filters}&search=${searchWord}` }),
  getSortedSuggestions: (sortValue, offset) =>
    get({ resource: `/suggestions?limit=${defaultLimit}&sort=${sortValue}&offset=${offset}` }),
  getSuggestionsByUserId: (userId, offset = 0) =>
    get({ resource: `/suggestions/user=${userId}?limit=${defaultLimit}&offset=${offset}` }),
  getSortedSuggestionByUserId: (userId, sortValue) =>
    get({ resource: `/suggestions/user=${userId}?sort=${sortValue}` }),
  getSuggestionsBySearchWord: (searchWord, offset = 0) =>
    get({ resource: `suggestions?search=${searchWord}?limit=${defaultLimit}&offset=${offset}` }),
  getSuggestionById: suggestionId => get({ resource: `/suggestions/${suggestionId}` }),
  assignUserToSuggestion: (suggestionId, userId) =>
    put({ resource: `/suggestions/${suggestionId}/assign/${userId}` }),
  unassignUserFromSuggestion: suggestionId =>
    put({ resource: `/suggestions/${suggestionId}/unassign` }),
  assignSuggestionToMeeting: (suggestionId, meetingId) =>
    patch({ resource: `/suggestions/${suggestionId}`, data: { meeting_id: meetingId } }),
  getSuggestionByMeetingId: meetingId => get({ resource: `/suggestions/meeting/${meetingId}` }),
  getSortedSuggestionByMeetingId: (meetingId, sortValue) =>
    // eslint-disable-next-line
    get({ resource: `/suggestions?sort=${sortValue}&filters=meeting_id${asciiUriEncoding.VALUE_OF_PARAM}${meetingId}` }),
  updateSuggestionStatus: (suggestionId, status) =>
    put({ resource: `/suggestions/${suggestionId}/status/${status}` }),
  addTagToSuggestion: (suggestionId, tag) =>
    post({ resource: `/suggestions/${suggestionId}/tags`, data: { tags: [tag] } }),
  removeTagFromSuggestion: (suggestionId, tag) =>
    del({ resource: `/suggestions/${suggestionId}/tags`, data: { tags: [tag] } }),
  getOpenSuggestions: () => get({ resource: '/suggestions/open' }),
  getResolvedSuggestions: () => get({ resource: '/suggestions/resolved' })
};
