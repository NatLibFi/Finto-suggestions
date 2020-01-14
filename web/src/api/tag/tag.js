import { get, del, put, post } from '../utils';

export default {
  getTags: () => get({ resource: '/tags' }),
  putTag: params =>
    put({ resource: `/tags/${params.label}`, data: { color: params.color, label: 'PLACEHOLDER' } }),
  deleteTag: tagLabel => del({ resource: `/tags/${tagLabel}` }),
  addNewTagStraightToDB: data => post({ resource: '/tags', data: data })
};
