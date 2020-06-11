import axios from 'axios';
import { storeKeyNames } from '../store/modules/authenticatedUser/authenticatedUserConsts';

const client = axios.create({
  baseURL: '/api',
  // baseURL: 'http://localhost:8080/api',
  json: true
});
const execute = async (method, resource, data, useRefreshToken) => {
  // eslint-disable-next-line no-undef
  const access_token = $cookies.get(storeKeyNames.ACCESS_TOKEN);
  // eslint-disable-next-line no-undef
  const refreshToken = $cookies.get(storeKeyNames.REFRESH_TOKEN);
  let AuthHeaderValue;
  if (useRefreshToken) {
    AuthHeaderValue = refreshToken && refreshToken.length > 0 ? `Bearer ${refreshToken}` : '';
  } else {
    AuthHeaderValue = access_token && access_token.length > 0 ? `Bearer ${access_token}` : '';
  }
  return client({
    method,
    url: resource,
    data: data,
    headers: {
      Authorization: AuthHeaderValue
    }
  })
    .then(request => {
      return request.data;
    })
    .catch(error => {
      /* eslint-disable-next-line */
      // TODO: needs to decide where errors are going to logged but for now just printing them to console
      console.log(error);
      if (error.response) {
        return error.response.data;
      }
      return {};
    });
};
export const get = async options => execute('get', options.resource, null);
export const post = async options =>
  execute('post', options.resource, options.data, options.useRefreshToken);
export const put = async options => execute('put', options.resource, options.data);
export const patch = async options =>
  execute('patch', options.resource, options.data, options.useRefreshToken);
export const del = async options => execute('delete', options.resource, options.data);
