<template>
<div class="comment">
  <div class="comment-container">
    <div class="comment-header">
      <div class="comment-info">
        <p>Kommentoi ehdotusta</p>
      </div>
    </div>
    <div class="comment-box">
      <markdown-editor v-model="content" ref="markdownEditor"></markdown-editor>
    </div>
    <div class="comment-submit">
      <span @click="saveNewComment" class="submit-button">
        Lähetä kommentti
      </span>
    </div>
  </div>
</div>

</template>

<script>
import markdownEditor from 'vue-simplemde/src/markdown-editor';

import { mapEventActions } from '../../store/modules/event/eventModule.js';
import { eventActions } from '../../store/modules/event/eventConsts.js';
import { eventTypes } from '../../utils/eventMappings.js';
// import {
//   suggestionMutations,
//   suggestionActions
// } from '../../store/modules/suggestion/suggestionConsts.js';
// import { mapSuggestionMutations } from '../../store/modules/suggestion/suggestionModule.js';

export default {
  props: {
    userId: {
      type: [String, Number],
      required: true
    },
    suggestionId: {
      type: [String, Number],
      required: true
    }
  },
  components: {
    markdownEditor
  },
  data: () => ({
    content: ''
  }),
  methods: {
    ...mapEventActions({
      addNewEvent: eventActions.ADD_NEW_EVENT
    }),
    constructEventJsonObject() {
      if (this.userId > 0 && this.suggestionId > 0) {
        return {
          event_type: eventTypes.COMMENT,
          text: this.content,
          user_id: parseInt(this.userId),
          suggestion_id: parseInt(this.suggestionId)
        };
      }
      return null;
    },
    saveNewComment() {
      this.addNewEvent({
        event: this.constructEventJsonObject(),
        suggestionId: parseInt(this.suggestionId)
      });
      this.content = '';
    }
  }
};
</script>

<style scoped>
@import '~simplemde/dist/simplemde.min.css';

div.comment-container {
  width: 100%;
  text-align: left;
  overflow: hidden;
}

div.comment-header {
  padding: 20px 40px 0;
}

div.comment-header .comment-info {
  display: inline-block;
  vertical-align: middle;
}

div.comment-header .comment-info p {
  vertical-align: middle;
  margin: 0;
  font-weight: bold;
}

div.comment-box {
  width: calc(100% - 80px);
  padding: 20px 40px 10px;
  margin: 0;
}

div.comment-submit {
  width: calc(100% - 80px);
  padding: 0 40px 15px;
  margin: 4px 0 10px;
  text-align: right;
}

.submit-button {
  background-color: #06a798;
  border: none;
  border-radius: 1px;
  color: white;
  padding: 10px 18px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  cursor: hand;
  transition: background-color 0.1s;
}

.submit-button:hover {
  background-color: #44bdb2;
}

@media (max-width: 750px) {
  div.comment-header {
    padding: 20px;
  }

  div.comment-box {
    width: calc(100% - 40px);
    padding-left: 20px;
    padding-right: 20px;
  }

  div.comment-submit {
    width: calc(100% - 40px);
    padding: 10px 20px;
  }
}
</style>

<style>
.markdown-editor .CodeMirror, .markdown-editor .CodeMirror-scroll {
  min-height: 100px;
}
</style>