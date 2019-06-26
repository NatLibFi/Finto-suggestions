export const namespace = 'user';

export const storeStateNames = {
  USER: 'user',
  AUTHENTICATED_USER: 'authenticatedUser',
  USERS: 'users'
};

export const userGetters = {
  GET_USER: 'getUser',
  GET_AUTHENTICATED_USER: 'getAuthenticatedUser',
  GET_USERS: 'getUsers'
};

export const userMutations = {
  SET_USER: 'setUser',
  SET_AUTHENTICATED_USER: 'setAuthenticatedUser',
  SET_USERS: 'setUsers'
};

export const userActions = {
  GET_USER: 'getUser',
  GET_AUTHENTICATED_USER: 'getAuthenticatedUser',
  PATCH_USER: 'patchUser',
  GET_USERS: 'getUsers',
  RESET_PASSWORD: 'resetPassword',
  CREATE_USER: 'createUser'
};
