import { get, put, post, del } from '../utils';
import { asciiUriEncoding } from '../helper';

const defaultLimit = 200;

//TODO: cache limited fetch, because this is really slow
export default {
  getSuggestions: () => get({ resource: `/suggestions?limit=${defaultLimit}`}),
  getSuggestionsBySearchWord: searchWord => get({ resource: `suggestions?search=${searchWord}` }),
  getSortedSuggestions: sortValue =>
    get({ resource: `/suggestions?limit=${defaultLimit}&sort=${sortValue}` }),
  getSuggestionById: suggestionId => get({ resource: `/suggestions/${suggestionId}` }),
  assignUserToSuggestion: (suggestionId, userId) =>
    put({ resource: `/suggestions/${suggestionId}/assign/${userId}` }),
  unassignUserFromSuggestion: suggestionId =>
    put({ resource: `/suggestions/${suggestionId}/unassign` }),
  getSuggestionByMeetingId: meetingId => get({ resource: `/suggestions/meeting/${meetingId}` }),
  getSortedSuggestionByMeetingId: (meetingId, sortValue) =>
    // eslint-disable-next-line prettier/prettier
    get({ resource: `/suggestions?sort=${sortValue}&filters=meeting_id${asciiUriEncoding.VALUE_OF_PARAM}${meetingId}` }),
  updateSuggestionStatus: (suggestionId, status) =>
    put({ resource: `/suggestions/${suggestionId}/status/${status}` }),
  addTagToSuggestion: (suggestionId, tag) =>
    post({ resource: `/suggestions/${suggestionId}/tags`, data: { tags: [tag] } }),
  removeTagFromSuggestion: (suggestionId, tag) =>
    del({ resource: `/suggestions/${suggestionId}/tags`, data: { tags: [tag] } })
};
