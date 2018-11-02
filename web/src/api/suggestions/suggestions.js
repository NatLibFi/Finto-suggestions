import { get } from '../utils';
import * as R from 'ramda';
import { suggestionStateStatus, filteringFields } from '../../utils/suggestionMappings';
import { asciiUriEncoding } from '../helper';

const parseFilterArrayToValidUri = filters => {
  let params = '';
  let sortedFilters = [];
  if (filters.length > 1) {
    const labelComparator = R.comparator((a, b) => R.gt(R.prop('label', a), R.prop('label', b)));
    sortedFilters = R.sortBy(labelComparator, filters);
  } else {
    sortedFilters = filters;
  }

  sortedFilters.forEach(filter => {
    params += `${filteringFields[filter.type]}${asciiUriEncoding.VALUE_OF_PARAM}${filter.value}${
      asciiUriEncoding.NEXT_VAL
    }`;
  });

  return params.slice(0, -3);
};

export default {
  getSuggestions: () => get({ resource: '/suggestions' }),
  getOpenSuggestions: () =>
    get({ resource: `/suggestions?filters=type${asciiUriEncoding.VALUE_OF_PARAM}new` }),
  getResolvedSuggestions: () =>
    get({
      resource: `/suggestions?filters=
      status${asciiUriEncoding.VALUE_OF_PARAM}${suggestionStateStatus.ACCEPTED}
      ${asciiUriEncoding.NEXT_VAL}status${asciiUriEncoding.VALUE_OF_PARAM}${suggestionStateStatus}`
    }),
  getSortedSuggestions: sortValue => get({ resource: `/suggestions?sort=${sortValue}` }),
  filterSuggestions: filters =>
    get({ resource: `/suggestions?filters=${parseFilterArrayToValidUri(filters)}` }),
  getSuggestionById: suggestionId => get({ resource: `/suggestions/${suggestionId}` })
};
