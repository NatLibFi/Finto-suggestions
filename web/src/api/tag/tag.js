import { get, del } from '../utils';

export default {
  getTags: () => get({ resource: '/tags' }),
  deleteTag: tagLabel => del({ resource: `/tags/${tagLabel}` })
};
