import axios from "axios";

const client = axios.create({
  baseURL: process.env.VUE_APP_API_ADDRESS,
  json: true
});

const execute = async (method, options) => {
  // inject the accessToken for each request
  //   let accessToken = await Vue.prototype.$auth.getAccessToken();
  const accessToken = "";
  return client({
    method,
    url: options.resource,
    data: options.data,
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  }).then(req => {
    return req.data;
  });
};

export const get = async options =>
  execute("get", options.resource, options.data);
