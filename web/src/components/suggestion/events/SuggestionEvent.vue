<template>
<div class="event">
  <div class="event-divider"></div>

  <div class="event-container">
    <div class="event-header">
      <div class="event-user-initials"></div>
      <div class="event-info">
        <p class="event-user">
          <span class="user-name">{{ userName }} </span>
          <span v-if="type == 'ACTION'">{{ action }}</span>
        </p>
        <p class="date-sent">Lähetetty 5 päivää sitten</p>
      </div>
    </div>

    <div v-if="type == 'COMMENT'" class="event-comment">
      <p>{{ event.text }}</p>
    </div>
  </div>
</div>

</template>

<script>
export default {
  props: {
    event: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      required: true
    }
  },
  data: () => ({
    userInitials: 'MP',
    userName: 'Miki Pernu',
    action: 'vaihtoi tyypiksi '
  })
};
</script>

<style scoped>
div.event-divider {
  display: inline-block;
  text-align: center;
  width: 2px;
  height: 40px;
  margin-top: 20px;
  background-color: #dddddd;
}

div.event-container {
  width: 100%;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
  margin-top: 10px;
}

div.event-header {
  padding: 20px 40px;
}

div.event-header .event-user-initials {
  display: inline-block;
  height: 50px;
  width: 50px;
  background-color: #eeeeee;
  vertical-align: middle;
}

div.event-header .event-info {
  display: inline-block;
  vertical-align: middle;
  margin-left: 20px;
}

div.event-header .event-info p {
  vertical-align: middle;
  margin: 0;
}

div.event-header .event-info .user-name {
  font-weight: 600;
  font-size: 16px;
}

div.event-header .event-info .date-sent {
  font-size: 14px;
}

div.event-comment {
  width: 100%;
  border-top: 1px solid #f5f5f5;
  padding: 10px 40px;
  margin: 0;
}

@media (max-width: 700px) {
  div.event-header {
    padding: 20px;
  }

  div.event-comment {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>
