import { get, put } from '../utils';
import { suggestionStateStatus } from '../../utils/suggestionMappings';
import { asciiUriEncoding } from '../helper';

export default {
  getSuggestions: () => get({ resource: '/suggestions' }),
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
    get({
      resource: `/suggestions?sort=${sortValue}
        &filters=meeting_id${asciiUriEncoding.VALUE_OF_PARAM}${meetingId}`
    })
};
