import { get } from '../utils';

export default {
  getMeetings: () => get({ resource: '/meetings' }),
  getMeeting: meetingId => get({ resource: `/meetings/${meetingId}` })
};
