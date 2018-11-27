import { post } from '../utils';

export default {
  revokeAuthentication: data => post({ resource: '/revokeAuthentication', data })
};
