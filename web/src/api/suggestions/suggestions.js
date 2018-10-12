import { get } from '../utils';

export default {
  getSuggestions: () => get({ resource: '/suggestions' }),
  getOpenSuggestions: () => get({ resource: '/suggestions?filters=type%3Anew' }),
  getResolvedSuggestions: () =>
    get({
      resource: '/suggestions?filters=status%3AACCEPTED%7Cstatus%3AREJECTED'
    }),
  getSortedSuggestions: sortValue => get({ resource: `/suggestions?sort=${sortValue}` }),
  searchSuggestions: searchQuery => get({ resource: `/suggestions?search=${searchQuery}` })
};
