import axios from "axios";

const client = axios.create({
  baseURL: "/api",
  json: true
});

const execute = async (method, resource, data) => {
  // inject the accessToken for each request
  //   let accessToken = await Vue.prototype.$auth.getAccessToken();
  let accessToken = process.env.ACCESS_TOKEN;
  return client({
    method,
    url: resource,
    data: data,
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  }).then(req => {
    return req.data;
  });
};

export const get = async options => execute("get", options.resource, null);
