<template>
  <div class="select-tag-box">
    <button @click="toggleTagSelector">
        <svg-icon icon-name='select-tag'><icon-tag /></svg-icon>
    </button>
    <div v-if="showTagSelector" v-on-clickaway="toggleTagSelector" class="tag-selector">
      <div class="tag-selector-header">
        <h4>Hallitse käsitteen tunnisteita</h4>
      </div>
      <!-- TODO: build later search ability for tags in tag selection -->
      <!-- <div class="tag-selector-search">
        <input type="text" placeholder="Etsi tunnisteita" />
      </div> -->
      <div class="tag-selector-tags">
        <ul v-if="tags && tags.length > 0">
          <li class="tag-label" v-for="tag in tags" :key="tag.label">
            {{ normalizeText(tag.label) }}
            <input 
              type="checkbox"
              @click="handleTagUpdateToSuggestion(tag.label)"
              v-model="checkedTags"
              :id="tag.label"
              :value="tag.label" />
          </li>
        </ul>
        <ul v-else>
          <li>Ei tunnisteita</li>
        </ul>
      </div>
      <div class="tag-selector-new-tag">
        <p>
          <button @click="toggleNewTagInputs()">Lisää tunniste</button>
        </p>
      </div>
      <div class="tag-selector-new-tag-form" v-if="showCreateTagInputs">
        <div class="tag-selector-new-tag-form-input">
          <input type="text" v-model="newTag" />
        </div>
        <div class="tag-selector-new-tag-form-submit">
          <button @click="addNewTag">Tallenna</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconTag from '../icons/IconTag';
import { mapTagActions, mapTagGetters } from '../../store/modules/tag/tagModule';
import { tagActions, tagGetters } from '../../store/modules/tag/tagConst';
import { newActionEvent } from '../../utils/tagHelpers';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  components: {
    SvgIcon,
    IconTag
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
      addTagToSuggestion: tagActions.ADD_TAG_TO_SUGGESTION,
      removeTagFromSuggestion: tagActions.REMOVE_TAG_FROM_SUGGESTION
    }),
    toggleTagSelector() {
      this.showTagSelector = !this.showTagSelector;
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
    }
  }
};
</script>

<style scoped>
div.select-tag-box {
  position: relative;
  display: inline-block;
}

div.select-tag-box button {
  background-color: rgba(0, 0, 0, 0);
  border-width: 0;
}

div.tag-selector {
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

div.tag-selector-header {
  border-bottom: 1px solid #f5f5f5;
}

div.tag-selector-header > h4 {
  color: #444444;
  font-size: 9pt;
  text-align: center;
  margin: 5px 0 5px 0;
}

div.tag-selector-search {
  padding-top: 10px;
  padding-left: 10px;
}

div.tag-selector-search > input {
  max-width: 90%;
  width: 90%;
  height: 20px;
  float: left;
}

div.tag-selector-tags ul {
  list-style-type: none;
  padding-left: 0;
  margin-right: 10px;
}

div.tag-selector-tags li {
  text-align: left;
  margin-left: 10px;
  font-size: 10pt;
}

div.tag-selector-tags li > input {
  margin: 0;
  float: right;
}

div.tag-selector-tags li > input::placeholder {
  color: #bfbfbf;
}

div.tag-selector-new-tag {
  text-align: left;
  font-size: 10pt;
  color: #06a798;
  padding-left: 10px;
}

div.tag-selector-new-tag > p > button {
  background: none;
  color: inherit;
  border: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
}

div.tag-selector-new-tag > p > button:hover {
  color: #21baac;
  outline: none;
}

div.tag-selector-new-tag > p > button:active {
  color: #ababab;
  transform: translateY(4px);
  outline: none;
}

div.tag-selector-new-tag > p > button:focus {
  outline: none;
}

div.tag-selector-new-tag-form {
  text-align: left;
  padding-top: 10px;
  padding-left: 10px;
}

div.tag-selector-new-tag-form > .tag-selector-new-tag-form-input {
  padding-top: 10px;
  padding-bottom: 10px;
}

div.tag-selector-new-tag-form-submit {
  text-align: left;
  font-size: 10pt;
  color: #bfbfbf;
}

div.tag-selector-new-tag-form-submit > button {
  background: none;
  color: inherit;
  border: none;
  padding: 0;
  font: inherit;
  cursor: pointer;
}

div.tag-selector-new-tag-form-submit > button:hover {
  color: #ababab;
  outline: none;
}

div.tag-selector-new-tag-form-submit > button:active {
  color: #ababab;
  transform: translateY(4px);
  outline: none;
}

div.tag-selector-new-tag-form-submit > button:focus {
  outline: none;
}

@media (max-width: 700px) {
  div.tag-selector {
    right: initial;
  }
}
</style>
