import { eventTypes } from './eventHelper';

export const newCommentEvent = (content, userId, suggestionId) => {
  return {
    event_type: eventTypes.COMMENT,
    text: content,
    user_id: parseInt(userId, 10),
    suggestion_id: parseInt(suggestionId, 10)
  };
};

export const newActionEvent = (content, value, userId, suggestionId) => {
  return {
    event_type: eventTypes.ACTION,
    text: content,
    value: value,
    user_id: parseInt(userId, 10),
    suggestion_id: parseInt(suggestionId, 10)
  };
};
