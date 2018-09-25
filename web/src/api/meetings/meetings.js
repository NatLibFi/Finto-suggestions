import { get } from '../utils';

export default {
  getMeetings: () => get({ resource: '/meetings' })
};
