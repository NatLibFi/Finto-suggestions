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
  const initials = [ individualNames[0], individualNames[1] ]
  return handleSpacedUserName(initials);
}

const hasSpaceIn = (userName) => {
  if (!(userName.indexOf(' ') > -1)) {
    return false;
  }
  return true;
}

const handleSpacedUserName = (initials) => {
  let firstName = initials[0], secondName = initials[1]
  if (firstName && secondName) {
    return `${firstName[0].toUpperCase()}${secondName[0].toUpperCase()}`;
  }
}