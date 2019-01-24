export const userNameInitials = userName => {
  if (userName && userName.length > 0) {
    return createInitials(userName);
  }
  return '';
};

const createInitials = (userName) => {
  if (!hasSpaceIn(userName)) {
    return userName[0].toUpperCase();
  }
  let individualNames = userName.split(' ');
  return handleSpacedUserName([individualNames[0], individualNames[1]]);
}

const hasSpaceIn = (userName) => {
  if (!(userName.indexOf(' ') > -1)) {
    return false;
  }
  return true;
}

const handleSpacedUserName = (names) => {
  let firstName = names[0], secondName = names[1]
  if (firstName && secondName) {
    return `${firstName[0].toUpperCase()}${secondName[0].toUpperCase()}`;
  }
}