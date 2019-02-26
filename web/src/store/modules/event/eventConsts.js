export const namespace = 'event';

export const storeStateNames = {
  ITEMS: 'items'
};

export const eventGetters = {
  GET_EVENTS: 'getEvents'
};

export const eventMutations = {
  ADD_NEW_EVENT: 'setEvent',
  SET_EVENTS: 'setEvents'
};

export const eventActions = {
  ADD_NEW_EVENT: 'addNewEvent',
  PATCH_EVENT: 'patchEvent',
  DELETE_EVENT: 'deleteEvent',
  GET_EVENTS_BY_SUGGESTION_ID: 'getEventsBySuggestionId'
};
