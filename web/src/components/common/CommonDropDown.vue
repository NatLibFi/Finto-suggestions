<template>
  <div class="sorting-options">
    <select v-model="selectedOption" @change="changeCallBack">
      <option value="">{{ header }}</option>
      <option v-for="selection in options" :key="selection.value" :value="selection.label"
        >{{ formatLabel(selection.label) }}
      </option>
    </select>
    <i class="arrow down"></i>
  </div>
</template>

<script>
export default {
  props: {
    /*
     * Dropdown header as string
     */
    header: String,
    /*
     * Options as Array needs to be as follows:
     * [{ label: 'A', value: '1' },{ label: 2, value: 'C' }]
     */
    options: Array,
    /*
     * changeCallBack as Func, functio to callback after change event is launched
     */
    changeCallBack: Function
  },
  data: () => ({
    selectedOption: ''
  }),
  methods: {
    formatLabel(label) {
      if (label) {
        const tolowercased = label.toLowerCase();
        return tolowercased.charAt(0).toUpperCase() + tolowercased.slice(1);
      } else {
        return '';
      }
    }
  }
};
</script>

<style>
.sorting-options {
  flex-grow: 1;
  right: 0;
  position: relative;
}

.sorting-options select {
  border: 0 !important; /*Removes border*/
  -webkit-appearance: none; /*Removes default chrome and safari style*/
  -moz-appearance: none; /*Removes default style Firefox*/
  font-size: 12pt;
  width: 80%;
  background-color: transparent;
}

.sorting-options select:focus {
  outline: none;
  border: 2px solid red;
}

/* CAUTION: IE hackery ahead */
.sorting-options select::-ms-expand {
  display: none; /* remove default arrow on ie10 and ie11 */
}

/* target Internet Explorer 9 to undo the custom arrow */
@media screen and (min-width: 0\0) {
  .sorting-options select {
    background: none\9;
    padding: 5px\9;
  }
}

i {
  border: solid black;
  border-width: 0 3px 3px 0;
  display: inline-block;
  padding: 3px;
  margin-left: 5px;
}
.down {
  transform: rotate(45deg);
  -webkit-transform: rotate(45deg);
}
.right {
  transform: rotate(-45deg);
  -webkit-transform: rotate(-45deg);
}
</style>
