import { get, put, post, del, patch } from '../utils';
import { asciiUriEncoding } from '../helper';

const defaultLimit = 200;

//TODO: cache limited fetch, because this is really slow
export default {
  getSuggestions: () => get({ resource: `/suggestions?limit=${defaultLimit}` }),
  getSortedSuggestions: sortValue =>
    get({ resource: `/suggestions?limit=${defaultLimit}&sort=${sortValue}` }),
  getSuggestionsByUserId: userId => get({ resource: `/suggestions/user=${userId}` }),
  getSortedSuggestionByUserId: (userId, sortValue) =>
    get({ resource: `/suggestions/user=${userId}?sort=${sortValue}` }),
  getSuggestionsBySearchWord: searchWord => get({ resource: `suggestions?search=${searchWord}` }),
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
    del({ resource: `/suggestions/${suggestionId}/tags`, data: { tags: [tag] } })
};
