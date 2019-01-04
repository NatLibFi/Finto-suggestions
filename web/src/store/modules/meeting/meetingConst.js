export const namespace = 'meeting';

export const storeStateNames = {
  ITEMS: 'items',
  ITEM: 'item',
  SELECTED_SORT: 'selectedSort'
};

export const sessionStorageKeyNames = {
  MEETING_LIST_SELECTED_SORT: 'meetingListSelectedSort'
};

export const meetingGetters = {
  GET_MEETINGS: 'getMeetings',
  GET_MEETING: 'getMeeting',
  GET_SELECTED_SORT: 'getSelectedSort'
};

export const meetingMutations = {
  SET_MEETINGS: 'setMeetings',
  SET_MEETING: 'setMeeting',
  SET_SELECTED_SORT: 'setSelectedSort',
  SET_SELECTED_STORE_SORT: 'setSelectedStoreSort'
};

export const meetingActions = {
  GET_MEETINGS: 'getMeetings',
  GET_MEETING: 'getMeeting',
  GET_SELECTED_SORT: 'getSelectedSort',
  SET_SELECTED_SORT: 'setSelectedSort'
};
