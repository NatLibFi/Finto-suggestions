export const namespace = 'meeting';

export const storeStateNames = {
  ITEMS: 'items',
  ITEM: 'item',
  MEETINGS_SELECTED_SORT: 'meetingsSelectedSort',
  UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS: 'updateMeetingSuggestionsProgressStatus'
};

export const sessionStorageKeyNames = {
  MEETING_LIST_SELECTED_SORT: 'meetingsSelectedSort'
};

export const meetingGetters = {
  GET_MEETINGS: 'getMeetings',
  GET_MEETINGS_AS_PITHY: 'getMeetingsAsPithy',  
  GET_MEETING: 'getMeeting',
  GET_MEETINGS_SELECTED_SORT: 'getMeetingsSelectedSort',
  GET_UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS: 'getUpdateMeetingSuggestionsProgressStatus'
};

export const meetingMutations = {
  SET_MEETINGS: 'setMeetings',
  SET_MEETINGS_AS_PITHY: 'setMeetingsAsPithy',
  SET_MEETING: 'setMeeting',
  SET_MEETINGS_SELECTED_SORT: 'setSelectedSort',
  SET_MEETINGS_SELECTED_STORE_SORT: 'setSelectedStoreSort',
  SET_UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS: 'setUpdateMeetingSuggestionsProgressStatus'
};

export const meetingActions = {
  GET_MEETINGS: 'getMeetings',
  GET_MEETINGS_AS_PITHY: 'getMeetingsAsPithy',
  GET_MEETING: 'getMeeting',
  ADD_NEW_MEETING: 'addNewMeeting',
  UPDATE_MEETING: 'updateMeeting',
  DELETE_MEETING: 'deleteMeeting',
  GET_MEETINGS_SELECTED_SORT: 'getMeetingsSelectedSort',
  SET_MEETINGS_SELECTED_SORT: 'setMeetingsSelectedSort'
};
