<template>
  <div
    v-if="isOpened"
    class="drop-down-options empty-options"
    v-on-clickaway="closeDropDown">
    <div v-if="dropDownOptions.length == 0">
      <div class="option" style="padding-left: 16px;">
        <span>{{ noOptionsMessage }}</span>
      </div>
    </div>
    <div v-if="dropDownOptions.length > 0">
      <div v-for="(option, i) in dropDownOptions" :key="option.id">
        <div
          @click="filterValueSelected(option, i)"
          :class="[i == selectedIndex ? 'selected' : '', 'option']">
          <svg-icon
            :class="[i == selectedIndex ? '' : 'hidden-checkmark']"
            icon-name="check"><icon-check />
          </svg-icon>
          <p>{{ option.label }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { findValueFromDropDownOptions } from '../../utils/dropDownHelper.js';

import SvgIcon from '../icons/SvgIcon';
import IconCheck from '../icons/IconCheck';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  components: {
    SvgIcon,
    IconCheck
  },
  directives: {
    onClickaway: onClickaway
  },
  props: {
    selectedIndex: Number,
    isOpened: Boolean,
    dropDownOptions: Array,
    noOptionsMessage: String
  },
  methods: {
    filterValueSelected(option, index) {
      this.handleDropDownSelectedIndicator(index);

      if (option && option.value !== '') {
        // do filtering by filter key
        const selectedValue = findValueFromDropDownOptions(option.value, this.dropDownOptions);
        this.applyFilter(selectedValue);
      } else {
        this.applyFilter();
      }
    },
    applyFilter(selectedFilter = null) {
      this.$emit('applyFilter', selectedFilter);
    },
    handleDropDownSelectedIndicator(index) {
      // update dropdownlist selected value indicator as selected
      this.$emit('refreshSelectedIndex', index);
    },
    closeDropDown() {
      this.$emit('closeDropDown');
    }
  }
};
</script>

<style scoped>
.drop-down-options {
  position: absolute;
  top: 44px;
  left: 0;
  background-color: #ffffff;
  min-width: 200px;
  z-index: 2;
  text-align: left;
  border: 1px solid #e1e1e1;
  border-radius: 2px;
  -webkit-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  -moz-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
}

.option {
  padding: 8px 6px 7px;
  border-bottom: 1px solid #f5f5f5;
  font-size: 14px;
  font-weight: 500;
  color: #555555;
  vertical-align: middle;
}

.option:hover {
  background-color: #f3fbfa;
  color: #111111;
  cursor: pointer;
  cursor: hand;
}

.option p {
  display: inline-block;
  margin: 0;
  text-transform: lowercase;
}

.option p::first-letter {
  text-transform: uppercase;
}

.option svg {
  height: 10px;
  margin-right: 5px;
  vertical-align: middle;
}

.selected {
  font-weight: 600;
  color: #111111;
}

.hidden-checkmark {
  opacity: 0;
}

.empty-options {
  min-width: 250px;
}

@media (max-width: 700px) {
  .option {
    padding: 12px 6px 11px;
  }
}
</style>
