export const userRoles = {
  NORMAL: 'NORMAL',
  ADMIN: 'ADMIN'
};

export const userNameInitials = userName => {
  let initials = '';
  if (existsAndHasLength(userName)) {
    const splitArray = userName.split(' ');
    if (existsAndHasLength(splitArray)) {
      return createInitials(splitArray);
    }
  }
  return initials;
};

const createInitials = array => {
  if (hasOnlyOneValidElement(array)) {
    return createOneInitial(array);
  }
  if (hasTwoValidElements(array)) {
    return createTwoInitials(array);
  }
};

const createOneInitial = array => {
  const string = array[0];
  const initial = `${string[0].toUpperCase()}`;
  return initial;
};

const createTwoInitials = array => {
  const firstString = array[0];
  const secondString = array[1];
  const initials = `${firstString[0].toUpperCase()}${secondString[0].toUpperCase()}`;
  return initials;
};

const hasOnlyOneValidElement = array => {
  return !!(array[0] && !array[1] && array[0].length > 0);
};

const hasTwoValidElements = array => {
  return !!(array[0] && array[1] && (array[0].length > 0 && array[1].length > 0));
};

const existsAndHasLength = variable => {
  if (variable && variable.length > 0) {
    return true;
  }
  return false;
};

export const emailValidator = email => {
  let validEmail = false;
  if (email && email.length > 0) {
    // eslint-disable-next-line no-useless-escape
    const emailRegExp = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/;
    validEmail = emailRegExp.test(email);
  }
  return validEmail;
};
