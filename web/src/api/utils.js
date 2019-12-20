import axios from 'axios';
import { storeKeyNames } from '../store/modules/authenticatedUser/authenticatedUserConsts';

const client = axios.create({
  baseURL: '/api',
  json: true
});



const execute = async (method, resource, data, useRefreshToken) => {
  console.log("API resource is: " + resource);
  console.log("Data: " + data);
  console.log("Is RefreshToken used: "+ useRefreshToken);
  // eslint-disable-next-line no-undef
  const access_token = $cookies.get(storeKeyNames.ACCESS_TOKEN);
  // const access_token = $cookies.get(storeKeyNames.ACCESS_TOKEN.concat(Math.random().toString(36).substring(7)));
  // alert(storeKeyNames.ACCESS_TOKEN.concat(Math.random().toString(36).substring(7)));
  // alert(Math.random().toString(36).substring(7));
  // eslint-disable-next-line no-undef
  const refreshToken = $cookies.get(storeKeyNames.REFRESH_TOKEN);

  let AuthHeaderValue;

  if (useRefreshToken) {
    AuthHeaderValue = refreshToken && refreshToken.length > 0 ? `Bearer ${refreshToken}` : '';
    console.log("RefreshToken is: " + AuthHeaderValue);
  } else {
    AuthHeaderValue = access_token && access_token.length > 0 ? `Bearer ${access_token}` : '';
    console.log("AccessToken is: " + AuthHeaderValue);
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
      return error.response.data;
    });
};

export const get = async options => execute('get', options.resource, null);
export const post = async options =>
  execute('post', options.resource, options.data, options.useRefreshToken);
export const put = async options => execute('put', options.resource, options.data);
export const patch = async options =>
  execute('patch', options.resource, options.data, options.useRefreshToken);
export const del = async options => execute('delete', options.resource, options.data);
