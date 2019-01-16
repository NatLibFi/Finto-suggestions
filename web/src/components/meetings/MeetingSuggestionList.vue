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
  methods: {
    goToMeetings: function() {
      this.$router.push('/meetings');
    }
  }
};
</script>

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
