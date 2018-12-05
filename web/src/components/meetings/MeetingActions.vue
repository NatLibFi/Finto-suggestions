<template>
  <div class="actions-container">
    <add-comment :userId="userId" :suggestionId="suggestionId" />
    <div class="action-buttons">
      <span class="button move-to-next-meeting">
        Siirrä seuraavaan<span class="hidden-in-mobile"> kokoukseen</span>
      </span>
      <span class="button dismiss">
        Jätä ehdotukseksi
      </span>
      <span class="button approve">
        Hyväksy ehdotus
      </span>
    </div>
  </div>
</template>

<script>
import AddComment from '../suggestion/AddComment';

export default {
  components: {
    AddComment
  },
  props: {
    userId: [String, Number],
    suggestionId: {
      type: [String, Number],
      required: true
    },
    meetingId: {
      type: [String, Number],
      required: false
    }
  }
}
</script>

<style scoped>
.actions-container {
  border: 2px solid #f5f5f5;
  background-color: #ffffff;
  border-top: none;
}

.action-buttons {
  padding: 20px 40px 25px;
  border-top: 1px solid #eeeeee;
  display: flex;
  justify-content: space-between;
}

.action-buttons .button {
  display: inline-block;
  padding: 8px 15px;
  margin: 0;
  font-weight: 600;
  font-size: 16px;
  border-radius: 1px;
  cursor: pointer;
  cursor: hand;
}

.action-buttons .move-to-next-meeting {
  color: #06a798;
  border: 3px solid #44bdb2;
  margin-right: 12px;
  transition: color, 0.1s;
  transition: border, 0.1s;
}

.action-buttons .move-to-next-meeting:hover {
  color: #44bdb2;
  border: 3px solid #5bcdc3;
}

.action-buttons .dismiss {
  color: #ffffff;
  background-color: #394554;
  border: 3px solid #394554;
  transition: background-color, 0.1s;
  transition: border, 0.1s;
  margin: 0 12px;
  margin-left: auto
}

.action-buttons .dismiss:hover {
  background-color: #525d6c;
  border: 3px solid #525d6c;
}

.action-buttons .approve {
  color: #ffffff;
  background-color: #237bba;
  border: 3px solid #237bba;
  transition: background-color, 0.1s;
  transition: border, 0.1s;
}

.action-buttons .approve:hover {
  background-color: #3c90cd;
  border: 3px solid #3c90cd;
}

@media (max-width: 700px) {
  .action-buttons {
    padding: 20px 20px 25px;
    display: inline-block;
  }
  .hidden-in-mobile {
    display: none;
  }

  .action-buttons .button {
    text-align: center;
    width: calc(100% - 40px);
    margin-bottom: 8px;
  }

  .action-buttons .dismiss,
  .actions-buttons .move-to-next-meeting {
    margin-left: 0;
    margin-right: 0;
  }

  .button:last-of-type {
    margin-bottom: 0;
  }
}
</style>
