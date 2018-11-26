import { get } from '../utils';

export default {
  getTags: () => get({ resource: '/tags' })
};
