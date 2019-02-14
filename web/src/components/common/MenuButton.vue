<template>
  <div class="button-container">
    <div @click="showDropdown = true" class="menu-button">
      <svg-icon icon-name="more"><icon-more/></svg-icon>
    </div>
    <div v-if="showDropdown" v-on-clickaway="closeDropdown" class="dropdown">
      <div v-for="option in options" :key="option.id">
        <div @click="option.method">{{ option.title }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconMore from '../icons/IconMore';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  components: {
    SvgIcon,
    IconMore
  },
  directives: {
    onClickaway: onClickaway
  },
  props: {
    options: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      showDropdown: false
    }
  },
  methods: {
    closeDropdown() {
      this.showDropdown = false;
    }
  }
}
</script>

<style scoped>
.button-container,
.menu-button {
  display: inline-block;
}

.dropdown {
  position: absolute;
  top: 20px;
  right: 0;
  width: 180px;
  font-size: 13px;
  font-weight: 600;
  color: #555555;
  text-align: center;
  background-color: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 2px;
  -webkit-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  -moz-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
}

.dropdown div {
  padding: 7px 10px;
}

.dropdown div:hover {
  background-color: #f3fbfa;
  cursor: pointer;
  cursor: hand;
}

@media (max-width: 700px) {
.dropdown {
  width: 210px;
  font-size: 14px;
}

.dropdown div {
  padding: 10px 16px;
}
}
</style>
