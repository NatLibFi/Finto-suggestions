/*
 * Used to find selected value from CommonDropDown options array
 * selectedValue = string
 * options = Array[{}] (example: [{label: 'ASD', value: 'DSA'}])
 */
export const findValueFromDropDownOptions = (selectedValue, options) => {
  if (selectedValue && options && selectedValue !== '') {
    const selection = options.find(e => e.value === selectedValue);
    return selection.value;
  }
  return null;
};

/*
 * Used to find dropdownoption index by value
 * selectedValue = string
 * options = Array[{}] (example: [{label: 'ASD', value: 'DSA'}])
 */
export const findIndexFromDropDownOptionsByValue = (selectedValue, options) => {
  if (selectedValue && options && selectedValue !== '') {
    const selection = options.find(e => e.value === selectedValue);
    return options.indexOf(selection);
  }
  return -1;
};
