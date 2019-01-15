export const namespace = 'authenticatedUser';

export const storeStateNames = {
  IS_AUTHENTICATED: 'isAuthenticated',
  USER_ID: 'userId',
  NAME: 'name',
  ERROR: 'error'
};

export const storeKeyNames = {
  ACCESS_TOKEN: 'vueauth_token',
  USER_ID: 'userId',
  REFRESH_TOKEN: 'vueauth_refresh_token'
};

export const authenticatedUserGetters = {
  GET_IS_AUTHENTICATED: 'getAuthentication',
  GET_USER_ID: 'getUserId',
  GET_USER_NAME: 'getUserName',
  GET_AUTHENTICATE_ERROR: 'getAuthenticateError'
};

export const authenticatedUserMutations = {
  SET_AUTHENTICATION: 'setAuthentication',
  SET_USER_ID: 'setUserId',
  SET_STORAGE_USER_ID: 'setStorageUserId',
  SET_USER_NAME: 'setUserName',
  SET_AUTHENTICATE_ERROR: 'setAuthenticateError'
};

export const authenticatedUserActions = {
  AUTHENTICATE: 'authenticate',
  VALIDATE_AUTHENTICATION: 'validateAuthentication',
  REVOKE_AUTHENTICATION: 'revokeAuthentication',
  GET_USER_ID_FROM_STORAGE: 'getUserIdFromStorage',
  GET_USER_NAME: 'getUserName',
  AUTHENTICATE_LOCAL_USER: 'authenticateLocalUser'
};
