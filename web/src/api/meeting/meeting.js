import { get, post, patch, del } from '../utils';

export default {
  getMeetings: () => get({ resource: '/meetings' }),
  getMeeting: meetingId => get({ resource: `/meetings/${meetingId}` }),
  addNewMeeting: data => post({ resource: '/meetings', data: data }),
  updateMeeting: (meetingId, data) => patch({ resource: `/meetings/${meetingId}`, data: data }),
  deleteMeeting: meetingId => del({ resource: `/meetings/${meetingId}` })
};
