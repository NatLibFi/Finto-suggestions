<template>
  <div class="comment">
    <div v-if="isAuthenticated" class="comment-container">
      <div class="comment-header">
        <div class="comment-info">
          <p><strong>Kommentoi ehdotusta</strong></p>
        </div>
      </div>
      <div class="comment-box">
        <markdown-editor
          v-model="content"
          ref="markdownEditor"
          :configs="mdeConfigs"
          :class="[!isAuthenticated ? 'disabled' : '']"
        >
        </markdown-editor>
      </div>
      <div class="comment-submit">
        <span @click="saveNewComment" class="submit-button">
          Lähetä kommentti
        </span>
      </div>
    </div>
    <div v-if="!isAuthenticated" class="comment-container">
      <div class="comment-header">
        <div class="comment-info">
          <p>Kirjaudu sisään kommentoidaksesi ehdotusta</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import markdownEditor from 'vue-simplemde/src/markdown-editor';

import { mapEventActions } from '../../store/modules/event/eventModule.js';
import { eventActions } from '../../store/modules/event/eventConsts.js';

// eslint-disable-next-line
import { mapAuthenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserModule.js';
// eslint-disable-next-line
import { authenticatedUserGetters } from '../../store/modules/authenticatedUser/authenticatedUserConsts.js';

import { newCommentEvent } from '../../utils/tagHelpers';

export default {
  props: {
    suggestionId: {
      type: [String, Number],
      required: true
    }
  },
  components: {
    markdownEditor
  },
  data() {
    return {
      content: '',
      mdeConfigs: {
        autofocus: false,
        hideIcons: ['preview', 'fullscreen', 'side-by-side', 'guide', 'image'],
        indentWithTabs: false,
        spellChecker: false,
        status: false,
        toolbarTips: true
      }
    };
  },
  computed: {
    ...mapAuthenticatedUserGetters({
      userId: authenticatedUserGetters.GET_USER_ID,
      isAuthenticated: authenticatedUserGetters.GET_IS_AUTHENTICATED
    })
  },
  methods: {
    ...mapEventActions({
      addNewEvent: eventActions.ADD_NEW_EVENT
    }),
    saveNewComment() {
      if (this.isAuthenticated && this.userId > 0 && this.suggestionId > 0) {
        this.addNewEvent({
          event: newCommentEvent(this.$sanitize(this.content), this.userId, this.suggestionId),
          suggestionId: parseInt(this.suggestionId, 10)
        });
        this.content = '';
      }
    }
  }
};
</script>

<style scoped>
@import '~simplemde/dist/simplemde.min.css';

.comment-container {
  text-align: left;
  overflow: hidden;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  margin-top: 10px;
}

.comment-header {
  padding: 25px 40px;
}

.comment-header .comment-info {
  display: inline-block;
  vertical-align: middle;
}

.comment-header .comment-info p {
  vertical-align: middle;
  margin: 0;
}

.comment-box {
  width: calc(100% - 80px);
  padding: 0 40px 10px;
  margin: 0;
}

.comment-submit {
  width: calc(100% - 80px);
  padding: 0 40px 15px;
  margin: 4px 0 10px;
  text-align: right;
}

.submit-button {
  background-color: #06a798;
  border: none;
  border-radius: 2px;
  color: white;
  padding: 8px 16px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  cursor: hand;
  transition: background-color 0.1s;
  margin: 0;
}

.submit-button:hover {
  background-color: #44bdb2;
}

.disabled {
  pointer-events: none;
  /* for "disabled" effect */
  opacity: 0.5;
  background: #cccccc;
}

@media (max-width: 750px) {
  .comment-header {
    padding: 20px;
  }

  .comment-box {
    width: calc(100% - 40px);
    padding-left: 20px;
    padding-right: 20px;
  }

  .comment-submit {
    width: calc(100% - 40px);
    padding: 10px 20px;
  }
}
</style>

<style>
.markdown-editor .CodeMirror,
.markdown-editor .CodeMirror-scroll {
  min-height: 100px;
}
</style>
