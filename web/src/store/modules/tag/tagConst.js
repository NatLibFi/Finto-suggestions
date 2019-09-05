export const namespace = 'tag';

export const storeStateNames = {
  ITEMS: 'items'
};

export const tagGetters = {
  GET_TAGS: 'getTags'
};

export const tagMutations = {
  SET_TAGS: 'setTags'
};

export const tagActions = {
  GET_TAGS: 'getTags',
  PUT_TAG: 'putTag',
  DELETE_TAG: 'deleteTag',
  ADD_TAG_TO_SUGGESTION: 'addTagToSuggestion',
  REMOVE_TAG_FROM_SUGGESTION: 'removeTagFromSuggestion',
  // Mika
  ADD_TAG_STRAIGHT_TO_DB: 'addTagStraightToDB',
  DELETE_TAG_STRAIGHT_FROM_DB: 'deleteTagStraightFromDB',
  // MODIFY_TAG_WITHOUT_SUGGESTION: 'modifyTagWithoutSuggestion'
};
