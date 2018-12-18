import axios from 'axios';
import { storeKeyNames } from '../store/modules/user/userConsts';

const client = axios.create({
  baseURL: '/api',
  json: true
});

const execute = async (method, resource, data) => {
  // eslint-disable-next-line no-undef
  const access_token = $cookies.get(storeKeyNames.ACCESS_TOKEN);
  return client({
    method,
    url: resource,
    data: data,
    headers: {
      Authorization: `Bearer ${access_token}`
    }
  })
    .then(req => {
      return req.data;
    })
    .catch(error => {
      /* eslint-disable-next-line */
      // TODO: needs to decide where errors are going to logged but for now just printing them to console
      console.log(error);
    });
};

export const get = async options => execute('get', options.resource, null);
export const post = async options => execute('post', options.resource, options.data);
export const put = async options => execute('put', options.resource, options.data);
