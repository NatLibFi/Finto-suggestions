import { get, del, put, post } from '../utils';

export default {
  getTags: () => get({ resource: '/tags' }),
  putTag: (tagLabel, params) =>
    put({ resource: `/tags/${tagLabel}`, data: { color: params.color, label: params.label } }),
  deleteTag: tagLabel => del({ resource: `/tags/${tagLabel}` })
  addNewTagStraightToDB: data => post({ resource: '/tags', data: data } )
};

