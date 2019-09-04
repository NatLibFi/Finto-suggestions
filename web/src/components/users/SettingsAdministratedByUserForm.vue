<template>
  <div>
    <hr v-bind:style="hrSmooth">
    <h5>Muokkaa nykyisiä tunnisteita</h5>
    <div>
      <div >
        <ul v-if="tags && tags.length > 0">
          <ol v-for="tag in tags" :key="tag.label">
            <span class="tag" v-bind:style="tab1"> {{ tag.label}}</span>

<!-- <p v-bind:style="{ fontSize: fontSize + 'px' }"> -->


            <span v-bind:style="tab2">
              <a class="button" v-on:click="removeTagStraightFromDB(tag.label)" onClick="return confirm('Oletko varma?');">Poista</a>
            </span>
            <span v-bind:style="tab3">
              <span class="tag" :style="{backgroundColor: tag.color}"> RGB </span>
            </span>
            <span class="tag" v-bind:style="tab4"> {{ tag.color }} </span>
            <span v-bind:style="tab5">
              <button class="button" @click="tagLabelForSwappingThePicker = tag.label">
                Muokkaa väriä
              </button>
            </span>
              <!-- <span> {{ tagLabelForSwappingThePicker }} </span> -->
              <div v-if="tagLabelForSwappingThePicker == tag.label"  class="tag-selector">
                <p>
                  <span> Olet muokkaamassa tunnistetta: {{ tagLabelForSwappingThePicker }} </span>
                </p>
                <color-picker 
                  v-if="tags"
                  v-model="modifyingColor"
                  class="color-picker"
                />
                <input hidden type="text" v-model="modifyingColor.hex"/>
                <p>
                  <strong>
                    <a class="button" @click="modifyTag(tag.label)">Tallenna</a>
                  </strong>
                </p>
                <p><a @click="tagLabelForSwappingThePicker = null">[ Sulje ]</a></p>
              </div>
          </ol>
        </ul>
      </div>
    </div>
    <div>   
    <hr v-bind:style="hrSmooth">
    <h5>Luo uusi tunniste</h5>
    <div class="tag-selector-new-tag-form-input">
      <p class="input-title">Anna uudelle tunnisteelle nimi</p>
        <input type="text" v-model="transitLabel" />
      <!-- <span> {{ transitLabel }} </span> -->
    </div>
    <div class="tag-selector-new-tag-form-input">
      <p class="input-title">Liu'uta ylempää palkkia ja valitse alimmaisesta väri </p>
        <!-- 4 -->

        <color-picker 
          v-if="tags"
          v-model="transitColor"
          class="color-picker"
        />
        <p>
          <input hidden type="text" v-model="transitColor.hex" />
          <strong>
            <a class="button" @click="addNewTagStraightToDB"> Lisää tunniste</a>
          </strong>
            <a class="button" @click="getItClear"> [ Tyhjennä valinnat ]</a>
        </p>
      <!-- <span> {{ transitColor.hex }} </span> -->
    </div>
    <p>
      <!-- <strong>
        <p><a class="save" @click="addNewTagStraightToDB">Lisää tunniste</a></p>
        <a @click="getItClear">Tyhjennä!</a>
      </strong>> -->


      <!-- <span class="save">
        Tallenna muutokset
      </span> -->

         <!-- <div @click.stop="submitForm" :class="[$v.$invalid ? 'disabled' : '', 'button']">
      <span class="save">
        Tallenna muutokset
      </span> -->


        <!-- <span> {{ modifyingOrigLabel }} </span>
        <span> {{ modifyingColor }} </span>
        <span> {{ modifyingColor.hex }} </span>
        <span> {{ modifyingGoalLabel }} </span>
        <span> {{ showColorPickerInTheList }} </span> -->
        <!-- <p><a @click="modifyTag">Testaa muokkausta</a></p> -->

      <!-- </strong> -->
    </p>
       <p>
    </p>
    </div>
  </div>
</template>

<script>
import IconTag from '../icons/IconTag';
import IconArrow from '../icons/IconArrow';
import { mapTagActions, mapTagGetters } from '../../store/modules/tag/tagModule';
import { tagActions, tagGetters } from '../../store/modules/tag/tagConst';
import { newActionEvent, newAddingEvent } from '../../utils/tagHelpers';
import { directive as onClickaway } from 'vue-clickaway';
import { Slider } from 'vue-color'; // 1
import Vue from 'vue';

export default {
  components: {
    IconTag,
    IconArrow,
    'color-picker': Slider // 2
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
  data() {
    return {
      // showCreateTagInputs: false,
      showColorPickerInTheList: false,
      tagLabelForSwappingThePicker: false,
      newTag: null,
      listForNewTags: [],
      transitLabel: null,
      transitColor: '#RRGGBB',
      modifyingOrigLabel: 'PPPP',
      modifyingColor: '#RRGGBB',
      modifyingGoalLabel: 'PLACEHOLDER',
      tab1: {
        position: 'absolute', 
        left: '41px'
      },
      tab2: {
        position: 'relative', 
        left: '80px'
      },
      tab3: {
        position: 'relative', 
        left: '100px'
      },
      tab4: {
        position: 'relative', 
        left: '120px'
      },
      tab5: {
        position: 'absolute', 
        left: '400px'
      },
      hrSmooth: {
        border: '0.5px dashed',
        color: '#D3D3D3'
        // border-radius: '5px'
      }
    };
  },
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
      newTagStraightToDB: tagActions.ADD_TAG_STRAIGHT_TO_DB,
      deleteTagStraighFromDB: tagActions.DELETE_TAG_STRAIGHT_FROM_DB,
      putTag: tagActions.PUT_TAG,
      addTagToSuggestion: tagActions.ADD_TAG_TO_SUGGESTION,
      removeTagFromSuggestion: tagActions.REMOVE_TAG_FROM_SUGGESTION
    }),

    swapBetween() {
      this.showColorPickerInTheList = !this.showColorPickerInTheList;
    },

    getItClear() {
      this.listForNewTags = [] //Tarvitaanko
      this.transitLabel = "",
      this.transitColor = ""
},
    normalizeText(text) {
      const firstCharacter = text.substring(0, 1);
      const restOfTheText = text.substring(1, text.length).toLowerCase();
      return `${firstCharacter}${restOfTheText}`;
    },
    async addNewTagStraightToDB() {
      if (this.transitLabel) {
        await this.newTagStraightToDB({
          color: this.transitColor.hex,
          label: this.transitLabel
        });
        this.getTags();
      }
    },
    async removeTagStraightFromDB(label) {
        await this.deleteTagStraighFromDB(label);
        this.getTags();
    },
    async refreshTagPage() {
      await this.getTags();
    },

    async modifyTag(label) {
      this.modifyingOrigLabel = label;
      if (this.modifyingOrigLabel) {
        await this.putTag(
          {
            color: this.modifyingColor.hex,
            label: this.modifyingOrigLabel
          }
        );
        this.getTags();
      }

// Toistaiseksi toimivin
    // async modifyTag() {
    //   if (this.modifyingOrigLabel) {
    //     // document.write(5 + 6);
    //     // document.writeln(params.tagLabel);
    //     await this.putTag(this.modifyingOrigLabel, 
    //       {
    //         color: this.modifyingColor,
    //         label: this.modifyingGoalLabel
    //       });
    //     this.getTags();
    //   }
      


      // const event = newActionEvent(
      //   'poisti ehdotuksesta tunnisteen',
      //   this.label,
      //   this.userId,
      //   this.suggestion.id
      // );
      // const params = { suggestionId: this.suggestion.id, tagLabel: label, event: event };
      // this.deleteTag(params);
      // this.$router.go();
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
.color-picker {
  box-shadow: none;
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
/* .button:hover {
  opacity: 0.6;
} */

.button:hover {
  background-color: #44bdb2;
  border: 3px solid #44bdb2;
  cursor: pointer;
  cursor: hand;
}

.a .save {
  color: #ffffff;
  transition: background-color, 0.1s;
  transition: border, 0.1s;
}

.a:hover {
  background-color: #44bdb2;
  border: 3px solid #44bdb2;
  cursor: pointer;
  cursor: hand;
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
