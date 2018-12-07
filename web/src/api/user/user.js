import { post, get } from '../utils';

export default {
  revokeAuthentication: data => post({ resource: '/revokeAuthentication', data }),
  getUserData: userId => get({ resource: `/users/${userId}` })
};
