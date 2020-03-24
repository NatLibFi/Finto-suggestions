import { post, get, del, patch } from '../utils';

export default {
  addNewComment: data => post({ resource: '/events', data: data }),
  patchEvent: (eventId, data, suggestionId) =>
    patch({ resource: `/events/${eventId}`, data: data, suggestionId: suggestionId }),
  deleteEvent: eventId => del({ resource: `/events/${eventId}` }),
  getEventsBySuggestion: suggestionId => get({ resource: `/events?suggestion_id=${suggestionId}` })
};
