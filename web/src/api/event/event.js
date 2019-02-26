import { post, get, del } from '../utils';

export default {
  addNewComment: data => post({ resource: '/events', data: data }),
  deleteEvent: eventId => del({ resource: `/events/${eventId}` }),
  getEventsBySuggestionId: suggestionId =>
    get({ resource: `/events?suggestion_id=${suggestionId}` })
};
