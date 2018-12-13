export const namespace = 'meeting';

export const storeStateNames = {
  ITEMS: 'items',
  FUTURE_MEETINGS_COUNT: 'futureMeetings',
  PAST_MEETINGS_COUNT: 'pastMeetings'
};

export const meetingGetters = {
  GET_MEETINGS: 'getMeetings',
  GET_FUTURE_MEETINGS_COUNT: 'getFutureMeetings',
  GET_PAST_MEETINGS_COUNT: 'getPastMeetings'
};

export const meetingMutations = {
  SET_MEETINGS: 'setMeetings',
  SET_FUTURE_MEETINGS_COUNT: 'setFutureMeetings',
  SET_PAST_MEETINGS_COUNT: 'setPastMeetings'
};

export const meetingActions = {
  GET_MEETINGS: 'getMeetings',
  GET_FUTURE_AND_PAST_MEETINGS_COUNT: 'getFutureAndPastMeetingsCount'
};
