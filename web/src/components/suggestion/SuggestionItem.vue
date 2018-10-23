<template>
  <li @click="goToSuggestion" class="item">
    <div class="item-summary">
      <div class="title">
        <p class="title-row">
          <span class="item-name">{{title}}</span>
          <span class="status tag" v-if="status !== 'DEFAULT'">{{ status }}</span>
          <span
            :class="[suggestionType == 'MODIFY'
              ? 'type-modify'
              : 'type-new',
            'tag']">{{ suggestionType }}
          </span>
          <span v-if="tags.length > 0">
            <span class="tags tag" v-for="tag in tags" :key="tag.label">{{tag.label}}</span>
          </span>
        </p>
      </div>
      <div class="label">
        <p>
          <strong>#{{ orderNumber }}</strong>
          Lähetetty {{ buildLabel() }}
        </p>
      </div>
    </div>
    <div class="item-comments">
      <svg-icon icon-name="comments"><icon-comments /></svg-icon>
      <span>2</span>
    </div>
  </li>
</template>

<script>
import { differenceInDays, parse } from 'date-fns';

import SvgIcon from '../icons/SvgIcon';
import IconComments from '../icons/IconComments';

export default {
  components: {
    SvgIcon,
    IconComments
  },
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
    },
    goToSuggestion: function() {
      this.$router.push({
        name: 'suggestion',
        params: { suggestionID: this.orderNumber }
      });
    }
  }
};
</script>

<style scoped>
p {
  margin: 0;
}
li.item {
  position: relative;
  width: 100%;
  height: 100%;
  margin: 0;
  cursor: pointer;
  cursor: hand;
  overflow: hidden;
}
.item-summary {
  padding: 10px 30px 10px;
  width: calc(100% - 130px);
  overflow: hidden;
}
.title {
  font-weight: 600;
  margin: 5px;
}
.title-row {
  line-height: 26px;
}
.item-name {
  font-size: 19px;
  margin-right: 8px;
  vertical-align: middle;
}
.tag {
  font-weight: 600;
  text-transform: lowercase;
  font-size: 14px;
  padding: 0 6px;
  border-radius: 3px;
  color: #ffffff;
}
.status {
  background-color: #58ba81;
  color: white;
  border: 2px solid #58ba81;
}
.type-new {
  background-color: #1137ff;
  border: 2px solid #1137ff;
}
.type-modify {
  background-color: #ff8111;
  border: 2px solid #ff8111;
}
.tags {
  color: #ac63ef;
  background-color: white;
  border: 2px solid #ac63ef;
}
.label {
  font-size: smaller;
  padding-left: 5px;
}
.item-comments {
  position: absolute;
  top: 50%;
  right: 30px;
  transform: perspective(1px) translateY(-50%);
  vertical-align: middle;
  height: 24px;
  color: #a4a4a4;
}
.item-comments span {
  font-size: 14px;
  font-weight: 600;
  vertical-align: middle;
}
.item-comments svg {
  height: 16px;
  margin-right: 8px;
  vertical-align: middle;
}

@media (max-width: 700px) {
  .item-summary {
    padding: 10px 20px 10px;
  }
  .item-name {
    display: block;
  }
}
</style>
