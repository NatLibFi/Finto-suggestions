import { post } from '../utils';

export default {
  authenticateGitHubUser: code => post({ resource: '/auth/github', data: { code } })
};
