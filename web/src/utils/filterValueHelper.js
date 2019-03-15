import { findValueFromDropDownOptions } from './dropDownHelper';
import { filterType } from './suggestionHelpers';

const removeOldFilterParamFromFilterList = (filters, type) => {
  return filters.filter(f => f.type !== type);
};

const handleSearchFilter = (value, filters) => {
  filters = removeOldFilterParamFromFilterList(filters, filterType.SEARCH);
  if (value.value !== '') {
    filters.push(value);
  }
  return filters;
};

const handleTagFilters = (value, filters) => {
  if (filters && filters.length > 0) {
    const tagfilter = filters.find(f => f.type === filterType.TAG && f.value === value.value);
    if (tagfilter) {
      filters = filters.filter(f => f !== tagfilter);
    } else {
      filters.push(value);
    }
  } else {
    filters.push(value);
  }
  return filters;
};

export const handleSetFilters = (value, filters, setFilters) => {
  if (value) {
    if (value.type !== filterType.SEARCH && value.type !== filterType.TAG) {
      filters = removeOldFilterParamFromFilterList(filters, value.type);
      filters.push(value);
    }
    if (value.type === filterType.SEARCH) {
      filters = handleSearchFilter(value, filters);
    }
    if (value.type === filterType.TAG) {
      filters = handleTagFilters(value, filters);
    }
  }
  setFilters(filters);
};

export const handleDropDownSelection = (
  selectedFilter,
  filterType,
  dropDownOptions,
  filters,
  setFilters
) => {
  if (dropDownOptions && selectedFilter && selectedFilter !== '') {
    const selectedValue = findValueFromDropDownOptions(selectedFilter, dropDownOptions);
    const value = { type: filterType, value: selectedValue };
    handleSetFilters(value, filters, setFilters);
  } else {
    filters = filters.filter(f => f.type !== filterType);
    handleSetFilters(null, filters, setFilters);
  }
};
