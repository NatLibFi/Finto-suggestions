export const namespace = 'authenticatedUser';

export const storeStateNames = {
  IS_AUTHENTICATED: 'isAuthenticated',
  USER_ID: 'userId',
  NAME: 'name'
};

export const storeKeyNames = {
  ACCESS_TOKEN: 'vueauth_token',
  USER_ID: 'userId',
  REFRESH_TOKEN: 'vueauth_refresh_token'
};

export const authenticatedUserGetters = {
  GET_AUTHENTICATE: 'getAuthenticate',
  GET_USER_ID: 'getUserId',
  GET_USER_NAME: 'getUserName'
};

export const authenticatedUserMutations = {
  SET_AUTHENTICATE: 'setAuthenticate',
  SET_USER_ID: 'setUserId',
  SET_STORAGE_USER_ID: 'setStorageUserId',
  SET_USER_NAME: 'setUserName'
};

export const authenticatedUserActions = {
  AUTHENTICATE: 'authenticate',
  VALIDATE_AUTHENTICATION: 'validateAuthentication',
  REVOKE_AUTHENTICATION: 'revokeAuthentication',
  GET_USER_ID_FROM_STORAGE: 'getUserIdFromStorage',
  GET_USER_NAME: 'getUserName',
  AUTHENTICATE_LOCAL_USER: 'authenticateLocalUser'
};
