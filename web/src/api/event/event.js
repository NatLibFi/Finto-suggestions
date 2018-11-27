import { post, get } from '../utils';

export default {
  addNewComment: data => post({ resource: '/events', data: data }),
  getEventsBySuggestionId: suggestionId =>
    get({ resource: `/events?suggestion_id=${suggestionId}` })
};
