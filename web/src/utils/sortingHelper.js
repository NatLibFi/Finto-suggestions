import { parse } from 'date-fns';

export const sortingKeys = {
  NEWEST_FIRST: 'CREATED_DESC',
  OLDEST_FIRST: 'CREATED_ASC',
  MOST_COMMENTS: 'COMMENTS_DESC',
  LEAST_COMMENTS: 'COMMENTS_ASC',
  LAST_UPDATED: 'UPDATED_DESC',
  MOST_REACTIONS: 'REACTIONS_DESC'
};

/*
* Desc (newest first) comparer for array.sort()
* field is the name of the property inside array's object
*/
export const comparerDesc = field => {
  return (obj1, obj2) => parse(obj2[field]) - parse(obj1[field]);
};

/*
* Asc (oldest first) comparer for array.sort()
* field is the name of the property inside array's object
*/
export const comparerAsc = field => {
  return (obj1, obj2) => parse(obj1[field]) - parse(obj2[field]);
};
