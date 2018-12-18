<template>
<div>
  <div class="meeting-container">
    <div class="arrow-button">
      <a @click="goToMeetings" unselectable="on">
        <svg-icon icon-name="arrow"><icon-arrow /></svg-icon>
        Takaisin kokouslistaukseen
      </a>
    </div>
    <div class="meeting-header">
      <div class="content">
        <meeting-status :meetingId="meetingId" />
        <suggestion-search-form />
        <filter-suggestions :isMeeting="true"/>
      </div>
    </div>

  </div>
  <!-- TODO: this suggestion-list must only provide suggestions from this meetingId -->
  <suggestion-list :meetingId="meetingId" />
</div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconArrow from '../icons/IconArrow';
import MeetingStatus from './MeetingStatus';
import SuggestionSearchForm from '../suggestion/SuggestionSearchForm';
import FilterSuggestions from '../suggestion/FilterSuggestions';
import SuggestionList from '../suggestion/SuggestionList';

export default {
  components: {
    SvgIcon,
    IconArrow,
    MeetingStatus,
    SuggestionSearchForm,
    FilterSuggestions,
    SuggestionList
  },
  props: {
    meetingId: {
      type: [String, Number],
      required: true
    }
  },
  // data: function() {
  //   return {
  //     meeting: {
  //       id: 1,
  //       name: 'YSA-kokous 2018/4 – Ongelmakokous',
  //       created: '2018-11-20T17:19:31.114000Z',
  //       modified: '2018-11-20T17:19:31.114000Z',
  //       meeting_date: '2018-12-24T10:00:31.114000Z'
  //     }
  //   }
  // },
  methods: {
    goToMeetings: function() {
      this.$router.push('/meetings');
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.meeting-container {
  width: 60vw;
  margin: 40px 20vw 20px;
}

.meeting-header {
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
}

.meeting-header .content {
  padding: 20px 40px 20px;
}

.arrow-button {
  color: #1ea195;
  font-weight: 800;
  font-size: 16px;
  text-align: left;
  margin-left: 6px;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

.arrow-button a:hover {
  cursor: pointer;
  cursor: hand;
}

.arrow-button svg {
  margin: 0 -15px -27px 0;
  width: 37px;
  height: 37px;
}

@media (max-width: 700px) {
  .meeting-container {
    width: 80vw;
    margin: 0 10vw 20px;
  }
}
</style>
