export const suggestionSortingKeys = {
  NEWEST_FIRST: 'CREATED_DESC',
  OLDEST_FIRST: 'CREATED_ASC',
  MOST_COMMENTS: 'COMMENTS_DESC',
  LEAST_COMMENTS: 'COMMENTS_ASC',
  LAST_UPDATED: 'UPDATED_DESC',
  MOST_REACTIONS: 'REACTIONS_DESC'
};

export const suggestionStateStatus = {
  ACCEPTED: 'ACCEPTED',
  REJECTED: 'REJECTED',
  DEFAULT: 'DEFAULT'
};

export const suggestionType = {
  NEW: 'NEW',
  MODIFY: 'MODIFY'
};

export const filterType = {
  STATUS: 'status',
  TAG: 'tag',
  TYPE: 'type',
  MEETING: 'meeting',
  SEARCH: 'search'
};
