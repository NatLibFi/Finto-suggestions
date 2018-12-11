export const userNameInitials = userName => {
  if (userName && userName.length > 0) {
    let initials = '';
    const splitArray = userName.split(' ');
    if (splitArray && splitArray.length > 0) {
      const firstElement = splitArray[0];
      const lastElement = splitArray[1];
      initials = `${firstElement[0].toUpperCase()}${lastElement[0].toUpperCase()}`;
      return initials;
    }
  }
  return '';
};
