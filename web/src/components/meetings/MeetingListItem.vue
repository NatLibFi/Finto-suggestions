<template>
  <li @click="goToMeetingList()" class="item">
    <div class="item-summary">
      <div class="title">
        <p class="title-row">
          <span class="item-name">{{ meeting.name }}</span>
        </p>
      </div>
      <div class="label">
        <p>
          <strong>#{{ meeting.id }}</strong>
          <span v-if="meeting.meeting_date.length > 0">
            Järjestetään {{ meeting.meeting_date.split('T')[0] }}
          </span>
          <span v-if="meeting.meeting_date.length == 0">
            Ei asetettua päivämäärää
          </span>
        </p>
      </div>
    </div>
    <div class="item-status">
      <div class="status-bar">
        <div :style="progressWidth" class="progress-bar"></div>
        <div :style="backgroundWidth" class="progress-background"></div>
      </div>
      <div class="status-summary">
        0/28 ehdotusta käsitelty (0%)
      </div>
    </div>
  </li>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconComments from '../icons/IconComments';

export default {
  components: {
    SvgIcon,
    IconComments
  },
  props: {
    meeting: {
      type: Object,
      required: true
    }
  },
  data: function() {
    return {
      progressWidth: {
        width: this.calculateStatusBarWidth() + '%'
      },
      backgroundWidth: {
        width: 100 - this.calculateStatusBarWidth() + '%'
      }
    }
  },
  methods: {
    goToMeetingList() {
      this.$router.push({
        name: 'meeting-suggestion-list',
        params: {
          meetingId: this.meeting.id,
          meeting: this.meeting
        }
      });
    },
    calculateStatusBarWidth() {
      // return integer percentage value for suggestions (processed / all %)
      return 30
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
  transition: background-color, 0.1s;
}
li.item:hover {
  background-color: #f3fbfa;
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
  font-size: 17px;
  margin-right: 8px;
  vertical-align: middle;
}
.label {
  font-size: smaller;
  padding-left: 5px;
}
.item-status {
  position: absolute;
  top: 42%;
  right: 30px;
  transform: perspective(1px) translateY(-50%);
  vertical-align: middle;
  height: 24px;
  color: #6a6a6a;
}
.item-status > div {
  font-size: 13px;
  font-weight: 500;
  vertical-align: middle;
}
.item-status .status-bar {
  width: 100%;
  margin-bottom: 4px;
}
.item-status .status-bar .progress-bar,
.item-status .status-bar .progress-background
 {
  display: inline-block;
  height: 6px;
  background-color: #eeeeee;
}
.item-status .status-bar .progress-bar {
  background-color: #66bea9;
}

@media (max-width: 700px) {
  .item-summary {
    padding: 10px 20px 10px;
  }
  .item-name {
    display: block;
  }
  .item-status {
    display: none;
  }
}
</style>
