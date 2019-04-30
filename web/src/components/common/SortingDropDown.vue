<template>
  <div v-if="isOpened" class="drop-down-options" v-on-clickaway="closeDropDown">
    <div v-for="(option, i) in dropDownOptions" :key="option.id">
      <div
        @click="sortValueSelected(option, i)"
        :class="[i == selectedIndex ? 'selected' : '', 'option']"
      >
        <svg-icon :class="[i == selectedIndex ? '' : 'hidden-checkmark']" icon-name="check">
          <icon-check />
        </svg-icon>
        <span>{{ option.label }}</span>
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
    dropDownOptions: Array
  },
  methods: {
    sortValueSelected(option, index) {
      this.handleDropDownSelectedIndicator(index);

      let selectedSort = null;

      if (option && option.value !== '') {
        // do sorting by sorting key
        const selectedValue = findValueFromDropDownOptions(option.value, this.dropDownOptions);
        selectedSort = selectedValue;
      }
      this.setSelectedSort(selectedSort);
    },
    setSelectedSort(selectedSort = null) {
      this.$emit('setSelectedSort', selectedSort);
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
  top: 42px;
  right: 0;
  background-color: #ffffff;
  width: 200px;
  z-index: 2;
  border: 1px solid #e1e1e1;
  border-radius: 2px;
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

@media (max-width: 700px) {
  .option {
    padding: 12px 6px 11px;
  }
}
</style>
