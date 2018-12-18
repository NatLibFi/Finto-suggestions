export const namespace = 'user';

export const storeStateNames = {
  IS_AUTHENTICATED: 'isAuthenticated',
  USER_ID: 'userId',
  USER: 'user',
  USERS: 'users'
};

export const storeKeyNames = {
  ACCESS_TOKEN: 'vueauth_token',
  USER_ID: 'userId',
  REFRESH_TOKEN: 'vueauth_refresh_token'
};

export const userGetters = {
  GET_AUTHENTICATE: 'getAuthenticate',
  GET_USER_ID: 'getUserId',
  GET_USER: 'getUser',
  GET_USERS: 'getUsers'
};

export const userMutations = {
  SET_AUTHENTICATE: 'setAuthenticate',
  SET_USER_ID: 'setUserId',
  SET_STORAGE_USER_ID: 'setStorageUserId',
  SET_USER: 'setUser',
  SET_USERS: 'setUsers'
};

export const userActions = {
  AUTHENTICATE: 'authenticate',
  VALIDATE_AUTHENTICATION: 'validateAuthentication',
  REVOKE_AUTHENTICATION: 'revokeAuthentication',
  GET_USER_DATA: 'getUserData',
  GET_USERS: 'getUsers',
  AUTHENTICATE_LOCAL_USER: 'authenticateLocalUser'
};
