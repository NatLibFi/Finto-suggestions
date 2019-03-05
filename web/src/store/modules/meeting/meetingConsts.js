export const namespace = 'meeting';

export const storeStateNames = {
  ITEMS: 'items',
  ITEM: 'item',
  MEETINGS_SELECTED_SORT: 'meetingsSelectedSort'
};

export const sessionStorageKeyNames = {
  MEETING_LIST_SELECTED_SORT: 'meetingsSelectedSort'
};

export const meetingGetters = {
  GET_MEETINGS: 'getMeetings',
  GET_MEETING: 'getMeeting',
  GET_MEETINGS_SELECTED_SORT: 'getMeetingsSelectedSort'
};

export const meetingMutations = {
  SET_MEETINGS: 'setMeetings',
  SET_MEETING: 'setMeeting',
  SET_MEETINGS_SELECTED_SORT: 'setSelectedSort',
  SET_MEETINGS_SELECTED_STORE_SORT: 'setSelectedStoreSort'
};

export const meetingActions = {
  GET_MEETINGS: 'getMeetings',
  GET_MEETING: 'getMeeting',
  ADD_NEW_MEETING: 'addNewMeeting',
  UPDATE_MEETING: 'updateMeeting',
  DELETE_MEETING: 'deleteMeeting',
  GET_MEETINGS_SELECTED_SORT: 'getMeetingsSelectedSort',
  SET_MEETINGS_SELECTED_SORT: 'setMeetingsSelectedSort'
};
