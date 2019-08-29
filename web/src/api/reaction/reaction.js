import { get, post, del } from '../utils';

export default {
  addReaction: data => post({ resource: '/reactions', data }),
  deleteReaction: reactionId => del({ resource: `/reactions/${reactionId}` }),
  getReactionsBySuggestion: suggestionId =>
    get({ resource: `/suggestions/${suggestionId}/reactions` }),
  getReactionsByEvent: eventId => get({ resource: `/events/${eventId}/reactions` })
};
