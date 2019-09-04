import { get, del, put, post } from '../utils';

export default {
  getTags: () => get({ resource: '/tags' }),
  // putTag: (tagLabel, params) =>
  putTag: (params) =>
    // put({ resource: `/tags/${tagLabel}`, data: { color: params.color, label: params.label } }),
    // put({ resource: `/tags/${tagLabel}`, data: { color: '#111113', label: 'HWEEE' } }),
    // put({ resource: `/tags/${tagLabel}`, data: { color: params.tag.color, label: params.label } }),
    // Toimivin put({ resource: `/tags/${tagLabel}`, data: { color: '#000000', label: 'HUIHAI'} }),
    put({ resource: `/tags/${params.label}`, data: { color: params.color, label: 'PLACEHOLDER'} }),
  deleteTag: tagLabel => del({ resource: `/tags/${tagLabel}` }),
  // Mika
  addNewTagStraightToDB: data => post({ resource: '/tags', data: data }),
  // Mika
  // modifyTagWithoutSuggestion: data => put({ resource: '/tags', data: data})
};

