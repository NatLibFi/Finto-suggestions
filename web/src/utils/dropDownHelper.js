/*
* Used to find selected value from CommonDropDown options array
* selectedValue = string
* options = Array[{}] (example: [{label: 'ASD', value: 'DSA'}])
*/
export const findValueFromDropDownOptions = (selectedValue, options) => {
  if (selectedValue && options && selectedValue !== '') {
    const selection = options.find(e => e.label == selectedValue);
    return selection.value;
  }
  return null;
};
