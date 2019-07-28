<template>
  <div class="select-tag-box">
    <button @click="toggleTagSelector">
      <svg-icon icon-name="select-tag"><icon-tag /></svg-icon>
    </button>
    <div v-if="showTagSelector" v-on-clickaway="toggleTagSelector" class="tag-selector">
      <div class="tag-selector-header">
        <h4 v-if="!showCreateTagInputs && !showModifyTagInputs">Hallitse käsitteen tunnisteita</h4>
        <h4 v-if="showCreateTagInputs">Luo uusi tunniste</h4>
        <h4 v-if="showModifyTagInputs">Muokkaa tunnistetta</h4>
      </div>
      <div  v-if="!showCreateTagInputs && !showModifyTagInputs" class="tag-selector-tags">
        <ul v-if="tags && tags.length > 0">
          <li class="tag-label" v-for="tag in tags" :key="tag.label">
            <span :style="{ backgroundColor: tag.color }" class="tag">
              {{ normalizeText(tag.label) }}
            </span>
            <input
              v-if="!showModifyTagButtons"
              type="checkbox"
              @click="handleTagUpdateToSuggestion(tag.label)"
              v-model="checkedTags"
              :id="tag.label"
              :value="tag.label"
            />
            <span
              v-if="showModifyTagButtons"
              @click="modifyTag(tag.label)"
              class="delete-btn"
            >
              Poista
            </span>
          </li>
        </ul>
        <ul v-else>
          <li>Ei tunnisteita</li>
        </ul>
        <div v-if="!showModifyTagButtons" class="tag-selector-new-tag">
          <p>
            <button @click="toggleNewTagInputs()" class="button">Lisää tunniste</button>
          </p>
        </div>
        <div class="tag-selector-new-tag">
          <p>
            <a @click="toggleTagModifying()">
              <span v-if="!showModifyTagButtons" class="button">Muokkaa ja poista tunnisteita</span>
              <span v-if="showModifyTagButtons" class="button">Palaa takaisin</span>
            </a>
          </p>
        </div>
      </div>
      <div class="tag-selector-new-tag-form" v-if="showCreateTagInputs">
        <div class="tag-selector-new-tag-form-input">
          <p class="input-title">Tunnisteen nimi</p>
          <input type="text" v-model="newTag" />
        </div>
        <p><a @click="addNewTag" class="button">Tallenna</a></p>
        <p><a @click="showCreateTagInputs = false" class="button back">Palaa takaisin</a></p>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconTag from '../icons/IconTag';
import IconArrow from '../icons/IconArrow';
import { mapTagActions, mapTagGetters } from '../../store/modules/tag/tagModule';
import { tagActions, tagGetters } from '../../store/modules/tag/tagConst';
import { newActionEvent } from '../../utils/tagHelpers';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  components: {
    SvgIcon,
    IconTag,
    IconArrow
  },
  directives: {
    onClickaway: onClickaway
  },
  props: {
    suggestion: {
      type: Object,
      required: true
    },
    userId: {
      type: [Number, String],
      required: true
    }
  },
  data: () => ({
    showTagSelector: false,
    checkedTags: [],
    showCreateTagInputs: false,
    showModifyTagInputs: false,
    showModifyTagButtons: false,
    newTag: null
  }),
  computed: {
    ...mapTagGetters({ tags: tagGetters.GET_TAGS })
  },
  created() {
    this.getTags();
    this.handleSuggestionTagsChecked();
  },
  methods: {
    ...mapTagActions({
      getTags: tagActions.GET_TAGS,
      deleteTag: tagActions.DELETE_TAG,
      addTagToSuggestion: tagActions.ADD_TAG_TO_SUGGESTION,
      removeTagFromSuggestion: tagActions.REMOVE_TAG_FROM_SUGGESTION
    }),
    toggleTagSelector() {
      this.showTagSelector = !this.showTagSelector;
      this.showCreateTagInputs = false;
      this.showModifyTagButtons = false;
      this.showModifyTagInputs = false;
      this.tagBeingModified = null;
      this.tagLabelBeingModified = null;
    },
    normalizeText(text) {
      const firstCharacter = text.substring(0, 1);
      const restOfTheText = text.substring(1, text.length).toLowerCase();
      return `${firstCharacter}${restOfTheText}`;
    },
    async handleTagUpdateToSuggestion(tagLabel) {
      if (this.isTagSetToSuggestion(tagLabel)) {
        const event = newActionEvent(
          'poisti ehdotuksesta tunnisteen',
          tagLabel,
          this.userId,
          this.suggestion.id
        );
        const params = { suggestionId: this.suggestion.id, tagLabel: tagLabel, event: event };
        await this.removeTagFromSuggestion(params);
      } else {
        const event = newActionEvent(
          'lisäsi ehdotukseen tunnisteen',
          tagLabel,
          this.userId,
          this.suggestion.id
        );
        const params = {
          suggestionId: this.suggestion.id,
          tagLabel: tagLabel,
          event: event
        };
        await this.addTagToSuggestion(params);
      }
    },
    isTagSetToSuggestion(tagLabel) {
      if (
        this.suggestion.tags &&
        this.suggestion.tags.length > 0 &&
        tagLabel &&
        tagLabel.length > 0
      ) {
        return this.suggestion.tags.find(tag => tag.label === tagLabel.toUpperCase())
          ? true
          : false;
      }
      return false;
    },
    handleSuggestionTagsChecked() {
      this.suggestion.tags.forEach(tag => {
        this.checkedTags.push(tag.label.toUpperCase());
      });
    },
    toggleNewTagInputs() {
      this.showCreateTagInputs = !this.showCreateTagInputs;
    },
    toggleTagModifying() {
      this.showModifyTagButtons = !this.showModifyTagButtons;
    },
    async addNewTag() {
      const event = newActionEvent(
        'lisäsi ehdotukseen tunnisteen',
        this.newTag,
        this.userId,
        this.suggestion.id
      );
      const params = { suggestionId: this.suggestion.id, tagLabel: this.newTag, event: event };
      await this.addTagToSuggestion(params);
      this.toggleNewTagInputs();
      await this.handleUpdateNewTagToPage();
    },
    async handleUpdateNewTagToPage() {
      await this.getTags();
      this.checkedTags.push(this.newTag.toUpperCase());
      this.newTag = '';
    },
    modifyTag(label) {
      const event = newActionEvent(
        'poisti ehdotuksesta tunnisteen',
        this.label,
        this.userId,
        this.suggestion.id
      );
      const params = { suggestionId: this.suggestion.id, tagLabel: label, event: event };
      this.deleteTag(params);
      this.$router.go();
    }
  }
};
</script>

<style scoped>
.select-tag-box {
  position: relative;
  display: inline-block;
}

.select-tag-box:focus,
.select-tag-box button:focus {
  outline: none;
}

.select-tag-box button {
  background-color: rgba(0, 0, 0, 0);
  border-width: 0;
}

.tag-selector {
  z-index: 1;
  position: absolute;
  right: 0;
  border: 2px solid #e1e1e1;
  min-height: 250px;
  min-width: 280px;
  margin: 0 0 0 0;
  padding: 5px;
  background-color: #ffffff;
}

.tag-selector-header {
  border-bottom: 1px solid #f5f5f5;
}

.tag-selector-header > h4 {
  color: #444444;
  font-size: 9pt;
  text-align: center;
  margin: 5px 0 5px 0;
}

.tag-selector-search {
  padding-top: 10px;
  padding-left: 10px;
}

.tag-selector-search > input {
  max-width: 90%;
  width: 90%;
  height: 20px;
  float: left;
}

.tag-selector-tags ul {
  list-style-type: none;
  padding-left: 0;
  margin-right: 10px;
  max-height: 300px;
  overflow: scroll;
}

.tag-selector-tags li {
  text-align: left;
  margin-left: 10px;
  font-size: 14px;
  height: 24px;
  position: relative;
  vertical-align: middle;
  padding: 1px;
}

.tag-selector-tags .tag-color-picker-btn {
  height: 19px;
  width: 19x;
  z-index: 12;
  border: 1px solid #eeeeee;
  background-color: #eeeeee;
}

.tag-selector-tags li .tag {
  background-color: #4794a2;
  color: #ffffff;
  padding: 2px 6px;
  border-radius: 2px;
}

.tag-selector-tags li span {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.tag-selector-tags li > input {
  position: absolute;
  top: 50%;
  transform: translateY(-72%);
  right: 0;
}

.tag-selector-tags li > input::placeholder {
  color: #bfbfbf;
}

.tag-selector-tags li > .delete-btn {
  margin: 0;
  color: #06a798;
  position: absolute;
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  transition: opacity 0.1s;
}

.tag-selector-tags li > .delete-btn:hover {
  opacity: 0.6;
  cursor: pointer;
  cursor: hand;
}

.tag-selector-new-tag {
  text-align: left;
  font-size: 10pt;
  color: #06a798;
  padding-left: 10px;
}

.tag-selector-new-tag > p > button {
  background: none;
  color: inherit;
  border: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
}

.tag-selector-new-tag > p > button:hover {
  color: #21baac;
  outline: none;
}

.tag-selector-new-tag > p > button:active {
  color: #ababab;
  outline: none;
}

.tag-selector-new-tag > p > button:focus {
  outline: none;
}

.tag-selector-new-tag-form {
  text-align: left;
  padding-top: 10px;
  padding-left: 14px;
}

.input-title {
  font-size: 11px;
  font-weight: 600;
  margin: 10px 0 3px;
}

.tag-selector-new-tag-form > .tag-selector-new-tag-form-input input {
  padding: 5px 4px;
  width: 70%;
  font-size: 12px;
}

.tag-selector-new-tag-form-submit button {
  padding: 0;
  margin: 0;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.1s;
  color: #06a798;
}

.tag-selector-new-tag-form-submit button:hover {
  opacity: 0.6;
  cursor: pointer;
  cursor: hand;
}

.button {
  font-size: 12px;
  background: none;
  color: #06a798;
  border: none;
  padding: 0;
  outline: none;
  font-size: 10pt;
  cursor: pointer;
  cursor: hand;
  transition: opacity 0.1s;
}

.button:hover {
  opacity: 0.6;
}

.back {
  position: absolute;
  left: 16px;
  bottom: 10px;
}

@media (max-width: 700px) {
  .tag-selector {
    right: initial;
    max-width: 72vw;
    min-width: 72vw;
    margin-left: -42px;
  }
}
</style>
