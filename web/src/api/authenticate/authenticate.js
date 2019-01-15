import { post } from '../utils';

export default {
  authenticateGitHubUser: code => post({ resource: '/auth/github', data: { code } }),
  refreshAuthenticationToken: data =>
    post({ resource: `/refresh`, data: { token_key: data.refresh_token }, useRefreshToken: true })
};
