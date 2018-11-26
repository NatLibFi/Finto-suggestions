import { get } from '../utils';

export default {
  getUserId: () => get({ resource: '/' })
};
