import { findValueFromDropDownOptions } from './dropDownHelper';
import { filterType } from './suggestionMappings';

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

export const handleSetFilters = (value, filters, setFilters) => {
  if (value && value.type !== filterType.SEARCH) {
    filters = removeOldFilterParamFromFilterList(filters, value.type);
    filters.push(value);
  }
  if (value && value.type === filterType.SEARCH) {
    filters = handleSearchFilter(value, filters);
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
  if (dropDownOptions && selectedFilter && selectedFilter.target.value !== '') {
    const selectedValue = findValueFromDropDownOptions(
      selectedFilter.target.value,
      dropDownOptions
    );
    const value = { type: filterType, value: selectedValue };
    handleSetFilters(value, filters, setFilters);
  } else {
    filters = filters.filter(f => f.type !== filterType);
    handleSetFilters(null, filters, setFilters);
  }
};
