<template>
  <li class="item">
    <div class="title">
      <p>
        <router-link :to="{name: 'suggestion', params: { suggestionID: orderNumber }}">{{title}}</router-link>
        <span class="status" v-if="status !== 'DEFAULT'">{{ status }}</span>
        <span class="type">{{ suggestionType }}</span>
        <span v-if="tags.length > 0">
          <span class="tags" v-for="tag in tags" :key="tag.label">{{tag.label}}</span>
        </span>
      </p>
    </div>
    <div class="label">
      <p>
        #{{ orderNumber }} Lähetetty {{ buildLabel() }}
      </p>
    </div>
  </li>
</template>

<script>
import { differenceInDays, parse } from 'date-fns';

export default {
  props: {
    orderNumber: Number,
    title: String,
    created: String,
    status: String,
    suggestionType: String,
    tags: Array
  },
  methods: {
    getDayDifference() {
      return differenceInDays(parse(new Date()), parse(this.created));
    },
    buildLabel() {
      const whenSended = this.getDayDifference();
      return whenSended > 0 ? `${whenSended} päivää sitten` : 'tänään';
    }
  }
};
</script>

<style scoped>
.item {
  width: 100%;
  height: 100%;
}
.item p {
  margin: 0;
}
.title {
  font-weight: bold;
  margin: 5px;
}
.status {
  margin: 5px;
  font-weight: normal;
  text-transform: lowercase;
  font-size: smaller;
  padding: 5px;
  background-color: green;
  color: white;
  border: 2px solid green;
}
.type {
  margin: 5px;
  font-weight: normal;
  text-transform: lowercase;
  font-size: smaller;
  padding: 5px;
  background-color: orange;
  color: white;
  border: 2px solid orange;
  border-radius: 3px;
}
.tags {
  margin: 5px;
  font-weight: normal;
  text-transform: lowercase;
  font-size: smaller;
  padding: 5px;
  background-color: white;
  color: purple;
  border: 2px solid purple;
}
.label {
  font-size: smaller;
  padding-left: 5px;
}
</style>
