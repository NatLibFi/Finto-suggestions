import { post, get, del } from '../utils';

export default {
  getTags: () => get({ resource: '/tags' }),
  deleteTag: tagLabel => del({ resource: `/tags/${tagLabel}` }),
  // Mika
  addNewTagStraightToDB: data => post({ resource: '/tags', data: data } )
  // deleteTagStraighFromDB: data => del({ resource: '/tags', data: data } )
};


