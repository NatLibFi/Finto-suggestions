import { post, get } from '../utils';

export default {
  revokeAuthentication: data => post({ resource: '/revokeAuthentication', data }),
  getUser: userId => get({ resource: `/users/${userId}` }),
  getUsers: () => get({ resource: '/users' }),
  registerLocalUser: data => post({ resource: '/users', data }),
  authenticateLocalUser: data => post({ resource: '/login', data })
};
