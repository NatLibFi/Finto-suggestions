export const namespace = 'authenticatedUser';

export const storeStateNames = {
  IS_AUTHENTICATED: 'isAuthenticated',
  USER_ID: 'userId',
  NAME: 'name',
  ERROR: 'error',
  ROLE: 'role'
};

export const storeKeyNames = {
  ACCESS_TOKEN: 'access_token',
  USER_ID: 'userId',
  REFRESH_TOKEN: 'refresh_token'
};

export const authenticatedUserGetters = {
  GET_IS_AUTHENTICATED: 'getAuthentication',
  GET_USER_ID: 'getUserId',
  GET_USER_NAME: 'getUserName',
  GET_AUTHENTICATE_ERROR: 'getAuthenticateError',
  GET_USER_ROLE: 'getUserRole'
};

export const authenticatedUserMutations = {
  SET_AUTHENTICATION: 'setAuthentication',
  SET_USER_ID: 'setUserId',
  SET_STORAGE_USER_ID: 'setStorageUserId',
  SET_USER_NAME: 'setUserName',
  SET_AUTHENTICATE_ERROR: 'setAuthenticateError',
  SET_USER_ROLE: 'setUserRole'
};

export const authenticatedUserActions = {
  AUTHENTICATE: 'authenticate',
  VALIDATE_AUTHENTICATION: 'validateAuthentication',
  REVOKE_AUTHENTICATION: 'revokeAuthentication',
  GET_USER_ID_FROM_STORAGE: 'getUserIdFromStorage',
  GET_USER_NAME: 'getUserName',
  AUTHENTICATE_LOCAL_USER: 'authenticateLocalUser',
  REFRESH_AUTHORIZATION_TOKEN: 'refreshAuthorizationToken',
  RESET_PASSWORD: 'resetPassword'
};
