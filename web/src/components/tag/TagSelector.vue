<template>
  <div>
    <div v-if="showTagSelector" class="tag-selector">
      <div class="tag-selector-header">
        <h4>Hallitse käsitteen tyyppejä</h4>
      </div>
      <div class="tag-selector-search">
        <input type="text" placeholder="Etsi tyyppejä" />
      </div>
      <div class="tag-selector-tags">
        <ul>
          <li>Muutos <input type="checkbox" /></li>
          <li>Maantieteellinen <input type="checkbox" /></li>
          <li>Uusi <input type="checkbox" /></li>
        </ul>
      </div>
      <div class="tag-selector-new-tag">
        <p>
          <button>+Uusi tyyppi</button>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    showTagSelector: {
      type: Boolean,
      required: true
    }
  },
  data: () => ({
  }),
  methods: {
  }
};
</script>

<style scoped>
div.tag-selector {
  z-index: 1;
  position: absolute;
  border: 2px solid #E1E1E1;
  min-height: 250px;
  min-width: 170px;
  margin: 25px 0 0 0;
  padding: 5px;
  background-color: #ffffff;
}

div.tag-selector-header {
  border-bottom: 1px solid #F5F5F5;
}

div.tag-selector-header > h4 {
  color: #444444;
  font-size: 9pt;
  text-align: center;
  margin: 5px 0 5px 0;
}

div.tag-selector-search {
  padding-top: 10px;
  padding-left: 10px;
}

div.tag-selector-search > input {
  max-width: 90%;
  float: left;
}

div.tag-selector-tags {
  border-top: 1px solid #F5F5F5;
  margin-top: 35px;
}

div.tag-selector-tags ul {
  list-style-type: none;
  padding-left: 0;
  margin-right: 10px;
}

div.tag-selector-tags li {
  text-align: left;
  margin-left: 10px;
}

div.tag-selector-tags li > input {
  margin: 0;
  float: right;
}

div.tag-selector-tags li > input::placeholder {
  color: #BFBFBF;
}

div.tag-selector-new-tag {
  text-align: left;
  font-size: 10pt;
  color: #BFBFBF;
}

div.tag-selector-new-tag > p > button {
  background: none;
  color: inherit;
  border: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
}

div.tag-selector-new-tag > p > button:hover {
  color: #ABABAB;
  outline: none;
}

div.tag-selector-new-tag > p > button:active {
  color: #ABABAB;
  box-shadow: 0 2px #8D8D8D;
  transform: translateY(4px);
  outline: none;
}

div.tag-selector-new-tag > p > button:focus {
  outline: none;
}
</style>


