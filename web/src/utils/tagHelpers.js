import { eventTypes } from './eventMappings';

export const newCommentEvent = (content, userId, suggestionId) => {
  return {
    event_type: eventTypes.COMMENT,
    text: content,
    user_id: parseInt(userId),
    suggestion_id: parseInt(suggestionId)
  };
};

export const newActionEvent = (content, userId, suggestionId) => {
  return {
    event_type: eventTypes.ACTION,
    text: content,
    user_id: parseInt(userId),
    suggestion_id: parseInt(suggestionId)
  };
};