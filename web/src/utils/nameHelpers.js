export const userNameInitials = userName => {
  if (userName && userName.length > 0) {
    return createInitials(userName);
  }
  return '';
};

function createInitials(userName) {
  if (!hasSpaceIn(userName)) {
    return userName[0].toUpperCase();
  }
  let individualNames = userName.split(' ');
  const initials = [ individualNames[0], individualNames[1] ]
  return handleSpacedUserName(initials);
}

function hasSpaceIn(userName) {
  if (!(userName.indexOf(' ') > -1)) {
    return false;
  }
  return true;
}

function handleSpacedUserName(initials) {
  if (initials[0] && initials[1]) {
    return `${initials[0][0].toUpperCase()}${initials[1][0].toUpperCase()}`;
  }
}