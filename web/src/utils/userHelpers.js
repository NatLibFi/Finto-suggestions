export const userRoles = {
  NORMAL: 'NORMAL',
  ADMIN: 'ADMIN'
};

export const userNameInitials = userName => {
  let initials = '';
  if (userName && userName.length > 0) {
    const splitArray = userName.split(' ');
    if (splitArray && splitArray.length > 0) {
      const firstElement = splitArray[0];
      const lastElement = splitArray[1];
      if (firstElement && lastElement && (firstElement.length > 0 && lastElement.length > 0)) {
        initials = `${firstElement[0].toUpperCase()}${lastElement[0].toUpperCase()}`;
        return initials;
      }
    }
  }
  return initials;
};
