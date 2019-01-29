export const userRoles = {
  NORMAL: 'NORMAL',
  ADMIN: 'ADMIN'
};

export const userNameInitials = userName => {
  if (userName && userName.length > 0) {
    return createInitials(userName);
  }
  return '';
};

const createInitials = userName => {
  if (!hasSpaceIn(userName)) {
    return userName[0].toUpperCase();
  }
  let individualNames = userName.split(' ');
  return handleSpacedUserName([individualNames[0], individualNames[1]]);
};

const hasSpaceIn = userName => {
  if (!(userName.indexOf(' ') > -1)) {
    return false;
  }
  return true;
};

const handleSpacedUserName = names => {
  let firstName = names[0],
    secondName = names[1];
  if (firstName && secondName) {
    return `${firstName[0].toUpperCase()}${secondName[0].toUpperCase()}`;
  }
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
