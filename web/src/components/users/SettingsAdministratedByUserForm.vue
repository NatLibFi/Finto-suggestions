<template>
  <div>
    <div>
      <span>Syötä uuden tunnisteen tiedot ja klikkaa "Lisää tunniste"</span>
     </div>
    <div>
      <span>Poistaessasi tunnistetta, tuplaklikkaa Poista-linkkiä</span>
    </div>
    <div>
      <div >
        <ul v-if="tags && tags.length > 0">
          <ol v-for="tag in tags" :key="tag.label">
            <span class="tag" style="position: absolute; left: 35px; "> Label: {{ tag.label }} </span>
            <span style="position: absolute; left: 265px; ">
              <a @click="removeTagStraightFromDB(tag.label); refreshTagPage()" class="delete-btn">Poista</a>
            </span>
            <span class="tag" :style="{ backgroundColor: tag.color }" style="position: relative; left: 240px; "> Väri:</span>
            <span class="tag" style="position: relative; left: 240px; "> {{ tag.color }} </span>
          </ol>
        </ul>
      </div>
    </div>
    <div>   
    <div class="tag-selector-new-tag-form-input">
      <p class="input-title">Anna uudelle tunnisteelle nimi</p>
        <input type="text" v-model="transitLabel" />
      <span> {{ transitLabel }} </span>
    </div>
    <div class="tag-selector-new-tag-form-input">
      <p class="input-title">Anna uudelle tunnisteelle väri (#heksakoodi)</p>
        <input type="text" v-model="transitColor" />
      <span> {{ transitColor }} </span>
    </div>
    <p>
      <strong>
        <p><a @click="addNewTagStraightToDB">Lisää tunniste</a></p>
        <a @click="getItClear">Tyhjennä!</a>
      </strong>
    </p>
      <li v-for="tagNewbie in listForNewTags" :key="tagNewbie.label">
        <p><span> Label: {{ tagNewbie.label }} </span></p>
        <span> Väri: {{ tagNewbie.color }} </span>
      </li>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconTag from '../icons/IconTag';
import IconArrow from '../icons/IconArrow';
import { mapTagActions, mapTagGetters } from '../../store/modules/tag/tagModule';
import { tagActions, tagGetters } from '../../store/modules/tag/tagConst';
import { newActionEvent, newAddingEvent } from '../../utils/tagHelpers';
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
    showModifyTagButtons: false,
    newTag: null,
    // Mika
    listForNewTags: [],
    transitLabel: null,
    transitColor: null
  }),
  computed: {
    ...mapTagGetters({ tags: tagGetters.GET_TAGS })
  },
  created() {
    this.getTags();
    this.handleSuggestionTagsChecked();
    this.refreshTagPage();
  },
  methods: {
    ...mapTagActions({
      getTags: tagActions.GET_TAGS,
      deleteTag: tagActions.DELETE_TAG,
      // Mika
      newTagStraightToDB: tagActions.ADD_TAG_STRAIGHT_TO_DB,
      //Mika
      deleteTagStraighFromDB: tagActions.DELETE_TAG_STRAIGHT_FROM_DB,
      addTagToSuggestion: tagActions.ADD_TAG_TO_SUGGESTION,
      removeTagFromSuggestion: tagActions.REMOVE_TAG_FROM_SUGGESTION
    }),
    adder() {
      this.listForNewTags.push({ color: "#ffffff", label: "Testailua1"})
},
    getItClear() {
      this.listForNewTags = [] //Tarvitaanko
      this.transitLabel = null,
      this.transitColor = null
},
    toggleTagSelector() {
      this.showTagSelector = !this.showTagSelector;
      this.showCreateTagInputs = false;
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
      this.showModifyTagButtons = !this.showModifyTagButtons;newTagStraightToDB
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
    // Mika
    async addNewTagStraightToDB() {
        await this.newTagStraightToDB({
          color: this.transitColor,
          label: this.transitLabel
        });
    },
    // Mika
    async removeTagStraightFromDB(label) {
        await this.deleteTagStraighFromDB(label);
    },
    async handleUpdateNewTagToPage() {
      await this.getTags();
      this.checkedTags.push(this.newTag.toUpperCase());
      this.newTag = '';
    },
// Mika
    async refreshTagPage() {
      await this.getTags();
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
