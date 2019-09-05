import { post, get, patch, put } from '../utils';

export default {
  revokeAuthentication: data => post({ resource: '/revokeAuthentication', data }),
  getUser: userId => get({ resource: `/users/${userId}` }),
  patchUser: (userId, data) => patch({ resource: `/users/${userId}`, data }),
  getUsers: () => get({ resource: '/users' }),
  registerLocalUser: data => post({ resource: '/users', data }),
  authenticateLocalUser: data => post({ resource: '/login', data }),
  resetPassword: data => put({ resource: '/users/reset_password/', data: { email: data } })
};
