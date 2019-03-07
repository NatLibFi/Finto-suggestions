export const eventTypes = {
  ACTION: 'ACTION',
  COMMENT: 'COMMENT'
};

export const combineEventTextContent = (text, value) => {
  if (text && text.length > 0 && value && value.length > 0) {
    return `${text} ${value}`;
  }
};
