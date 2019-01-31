import { get, put, post, del } from '../utils';
import { suggestionStateStatus } from '../../utils/suggestionHelpers';
import { asciiUriEncoding } from '../helper';

export default {
  getSuggestions: () => get({ resource: '/suggestions' }),
  getSuggestionsByUserId: userId => get({ resource: `/suggestions/user=${userId}` }),
  getSortedSuggestionByUserId: (userId, sortValue) =>
    get({ resource: `/suggestions/user=${userId}?sort=${sortValue}` }),
  getOpenSuggestions: () =>
    get({ resource: `/suggestions?filters=type${asciiUriEncoding.VALUE_OF_PARAM}new` }),
  getResolvedSuggestions: () =>
    get({
      // eslint-disable-next-line
      resource: `/suggestions?filters=status${asciiUriEncoding.VALUE_OF_PARAM}${suggestionStateStatus.ACCEPTED}${asciiUriEncoding.NEXT_VAL}status${asciiUriEncoding.VALUE_OF_PARAM}${suggestionStateStatus.REJECTED}`
    }),
  getSortedSuggestions: sortValue => get({ resource: `/suggestions?sort=${sortValue}` }),
  getSuggestionById: suggestionId => get({ resource: `/suggestions/${suggestionId}` }),
  assignUserToSuggestion: (suggestionId, userId) =>
    put({ resource: `/suggestions/${suggestionId}/assign/${userId}` }),
  unassignUserFromSuggestion: suggestionId =>
    put({ resource: `/suggestions/${suggestionId}/unassign` }),
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
