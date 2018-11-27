import { get } from '../utils';
import { suggestionStateStatus } from '../../utils/suggestionMappings';
import { asciiUriEncoding } from '../helper';

export default {
  getSuggestions: () => get({ resource: '/suggestions' }),
  getOpenSuggestions: () =>
    get({ resource: `/suggestions?filters=type${asciiUriEncoding.VALUE_OF_PARAM}new` }),
  getResolvedSuggestions: () =>
    get({
      // eslint-disable-next-line
      resource: `/suggestions?filters=status${asciiUriEncoding.VALUE_OF_PARAM}${suggestionStateStatus.ACCEPTED}${asciiUriEncoding.NEXT_VAL}status${asciiUriEncoding.VALUE_OF_PARAM}${suggestionStateStatus.REJECTED}`
    }),
  getSortedSuggestions: sortValue => get({ resource: `/suggestions?sort=${sortValue}` }),
  filterSuggestions: filters =>
    // eslint-disable-next-line no-undef
    get({ resource: `/suggestions?filters=${parseFilterArrayToValidUri(filters)}` }),
  getSuggestionById: suggestionId => get({ resource: `/suggestions/${suggestionId}` })
};
