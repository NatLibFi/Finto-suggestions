export const namespace = 'meeting';

export const storeStateNames = {
  ITEMS: 'items',
  TINY_ITEMS: 'tinyItems',
  ITEM: 'item',
  MEETINGS_SELECTED_SORT: 'meetingsSelectedSort',
  UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS: 'updateMeetingSuggestionsProgressStatus',
  MEETINGS_AS_PITHY: 'meetingsAsPithy',
  MEETING_AS_PITHY: 'meetingAsPithy',
  CURRENT_MEETING_ID: 'currentMeetingId',
};

export const sessionStorageKeyNames = {
  MEETING_LIST_SELECTED_SORT: 'meetingsSelectedSort'
};

export const meetingGetters = {
  GET_MEETINGS: 'getMeetings',
  GET_MEETINGS_BASICS: 'getMeetingsBasics',
  GET_MEETINGS_AS_PITHY: 'getMeetingsAsPithy',  
  GET_MEETING: 'getMeeting',
  GET_MEETINGS_SELECTED_SORT: 'getMeetingsSelectedSort',
  GET_UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS: 'getUpdateMeetingSuggestionsProgressStatus',
  GET_CURRENT_MEETING_ID: 'getCurrentMeetingId',
};

export const meetingMutations = {
  SET_CURRENT_MEETING_ID: 'setCurrentMeetingId',
  SET_MEETINGS: 'setMeetings',
  SET_MEETINGS_BASICS: 'setMeetingsBasics',
  SET_MEETINGS_AS_PITHY: 'setMeetingsAsPithy',
  SET_MEETING_AS_PITHY: 'setMeetingAsPithy',
  SET_MEETING: 'setMeeting',
  SET_MEETINGS_SELECTED_SORT: 'setSelectedSort',
  SET_MEETINGS_SELECTED_STORE_SORT: 'setSelectedStoreSort',
  SET_UPDATE_MEETING_SUGGESTIONS_PROGRESS_STATUS: 'setUpdateMeetingSuggestionsProgressStatus'
};

export const meetingActions = {
  GET_MEETINGS: 'getMeetings',
  GET_MEETINGS_BASICS: 'getMeetingsBasics',
  GET_MEETINGS_AS_PITHY: 'getMeetingsAsPithy',
  GET_MEETING: 'getMeeting',
  ADD_NEW_MEETING: 'addNewMeeting',
  UPDATE_MEETING: 'updateMeeting',
  DELETE_MEETING: 'deleteMeeting',
  GET_MEETINGS_SELECTED_SORT: 'getMeetingsSelectedSort',
  SET_MEETINGS_SELECTED_SORT: 'setMeetingsSelectedSort',
  SET_CURRENT_MEETING_ID: 'setCurrentMeetingId'
  
};
