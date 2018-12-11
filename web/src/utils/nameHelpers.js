export const userNameInitials = () => {
  if (this.userName && this.userName.length > 0) {
    let initials = '';
    const splitArray = this.userName.split(' ');
    if (splitArray && splitArray.length > 0) {
      const firstElement = splitArray[0];
      const lastElement = splitArray.slice(-1)[0];
      initials = `${firstElement[0].toUpperCase()}${lastElement[0].toUpperCase()}`;
      this.userInitials = initials;
    }
  }
};
