<template>
<div class="list-container">
  <meeting-list-header
    :futureMeetingCount="2"
    :pastMeetingCount="2"
    class="header" />
  <ul :class="['list', pageCount > 1 ? 'with-pagionation' : '']">
    <meeting-list-item
      class="item"
      v-for="item in paginated_items"
      :key="item.id"
      :meeting="item"
      />
  </ul>
  <meeting-list-pagination
    v-if="pageCount > 1"
    :pageCount="pageCount"
    @paginationPageChanged="console.log('pagination changed')"
  />
</div>
</template>

<script>
import MeetingListHeader from './MeetingListHeader';
import MeetingListItem from './MeetingListItem';
import MeetingListPagination from './MeetingListPagination';

export default {
  components: {
    MeetingListHeader,
    MeetingListItem,
    MeetingListPagination
  },
  data: function() {
    return {
      pageCount: 1,
      // TODO: use store to get real meetings
      paginated_items: [
        {
          id: 1,
          name: 'YSA-kokous 2018/4 – Ongelmakokous',
          created: '2018-11-20T17:19:31.114000Z',
          modified: '2018-11-20T17:19:31.114000Z',
          meeting_date: '2018-12-24T10:00:31.114000Z'
        },
        {
          id: 2,
          name: 'YSA-kokous 2019/1',
          created: '2018-11-20T17:19:31.114000Z',
          modified: '2018-11-20T17:19:31.114000Z',
          meeting_date: '2019-02-13T10:00:31.114000Z'
        }
      ]
    };
  },
  methods: {
    calculatePageCountForPagination: function() {
      return 10;
    },
    sortMeetingList(sort) {
      let meetings = this.meetings;
      if(sort === sortingKeys.NEWEST_FIRST) {
        meetings.sort(comparerDesc('meeting_date'));
      }

      if(sort === sortingKeys.OLDEST_FIRST) {
        meetings.sort(comparerAsc('meeting_date'));
      }
      this.paginated_items = meetings;
    },
  },
  watch: {
    meetings() {
      this.paginated_items = this.meetings;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.list-container {
  margin-bottom: 40px;
}

ul {
  list-style: none;
}

.list {
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  border-top: none;
  width: 60vw;
  margin: 0 20vw;
  padding-left: 0; /* reset inital padding for ul tags */
}

.with-pagionation {
  border-bottom: none;
}

.item {
  margin: 10px 0 10px 0;
  border-bottom: 2px solid #f5f5f5;
}

@media (max-width: 700px) {
  .list {
    width: 80vw;
    margin: 0 10vw 20px;
  }
}
</style>
