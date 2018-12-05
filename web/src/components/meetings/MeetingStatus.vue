<template>
  <div class="status-container">
    <!-- TODO: get meeting from store and show meeting.name only-->
    <h2 v-if="meeting">{{ meeting.name }}</h2>
    <h2 v-if="!meeting">YSA-kokous 2018-3</h2>
    <div class="meeting-status">
      <div class="status-bar">
        <div :style="progressWidth" class="progress-bar"></div>
        <div :style="backgroundWidth" class="progress-background"></div>
      </div>
      <div class="status-summary">
        <p>0/28 ehdotusta käsitelty (0%)</p>
        <p 
          v-if="['meeting-suggestion-list'].includes($route.name)" 
          class="next-suggestion-link">
          <!-- @click="goToNextSuggestion()" -->
          Jatka käsittelyä
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    meetingId: [String, Number],
    meeting: Object
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
    goToNextSuggestion() {
      this.$router.push({
        name: 'meeting-suggestion',
        params: {
          meetingId: this.meetingId,
          // TODO: create a method to calculate the next unprocessed suggestion in the meeting
          suggestionId: 1
        }
      })
    },
    calculateStatusBarWidth() {
      // return integer percentage value for suggestions (processed / all %)
      return 30
    }
  }
}
</script>

<style scoped>
.status-container {
  position: relative;
  width: 100%;
  text-align: left;
}
.meeting-status > div {
  font-size: 14px;
  font-weight: 600;
  vertical-align: middle;
  color: #6a6a6a;
}
.meeting-status .status-bar {
  width: 100%;
  margin-bottom: 4px;
}
.meeting-status .status-bar .progress-bar,
.meeting-status .status-bar .progress-background
 {
  display: inline-block;
  height: 6px;
  background-color: #eeeeee;
}
.meeting-status .status-bar .progress-bar {
  background-color: #66bea9;
}
.status-summary {
  position: relative;
  height: 40px;
}
.status-summary p {
  display: inline-block;
  position: absolute;
  left: 0;
  margin: 0;
}
.status-summary p.next-suggestion-link {
  left: initial;
  right: 0;
}
.next-suggestion-link {
  color: #06a798;
  cursor: pointer;
  cursor: hand;
}

@media (max-width: 700px) {
  .status-summary {
    position: initial;
    height: initial;
    padding-bottom: 10px;
  }
  .status-summary p {
    display: block;
    position: initial;
    right: initial;
    margin-bottom: 6px;
  }
}
</style>
