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
        </div>
      </div>
    </div>
    <suggestion-list :meetingId="meetingId" :page="page" />
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconArrow from '../icons/IconArrow';
import MeetingStatus from './MeetingStatus';
import SuggestionSearchForm from '../suggestion/SuggestionSearchForm';
import FilterSuggestions from '../suggestion/FilterSuggestions';
import SuggestionList from '../suggestion/SuggestionList';

import { handleMeetingQueries } from '../../utils/suggestionHelpers';

export default {
  components: {
    SvgIcon,
    IconArrow,
    MeetingStatus,
    SuggestionSearchForm,
    FilterSuggestions,
    SuggestionList
  },
  data() {
    return {
      filters: this.$route.query.filters ? this.$route.query.filters : '',
      searchWord: this.$route.query.search ? this.$route.query.search : '',
      sort: this.$route.query.sort ? this.$route.query.sort : ''
    };
  },
  props: {
    meetingId: {
      type: [String, Number],
      required: true
    },
    page: {
      type: [String, Number],
      required: true,
      default: 1
    }
  },
  created() {
    handleMeetingQueries(this.meetingId, this.filters, this.searchWord, this.sort, this.$router);
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
  margin: 40px 20vw 0;
}

.meeting-header {
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  border-bottom: 0;
}

.meeting-header .content {
  padding: 20px 40px 0;
}

.arrow-button {
  color: #1ea195;
  font-weight: 800;
  font-size: 14px;
  text-align: left;
  margin-left: 6px;
  margin-bottom: 2px;
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
  margin: 0 -15px -28px 0;
  width: 37px;
  height: 37px;
}

@media (max-width: 700px) {
  .meeting-container {
    width: 80vw;
    margin: 30px 10vw 0;
  }
}
</style>
