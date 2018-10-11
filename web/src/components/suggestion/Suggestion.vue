<template>
  <div class="suggestion">
    <div class="back-button">
      <a @click="goToSuggestions" unselectable="on">
        <!-- <svg-icon icon-name="arrow"><icon-arrow /></svg-icon> -->
        Takaisin käsite-ehdotuksiin
      </a>
    </div>

    <div v-if="suggestion" class="suggestion-container">

      <div class="suggestion-header">
        <div class="suggestion-header-headline">
          <h1 class="suggestion-title">{{ suggestion.preferred_label.fi }}</h1>
          <p class="suggestion-status">{{ suggestion.status }}</p>

          <div class="suggestion-header-details">
            <span><strong>#{{ suggestion.id }} </strong></span>
            <span>Lähetetty 3 päivää sitten</span>
            <span class="suggestion-type">{{ suggestion.suggestion_type }}</span>
            <!-- TODO: v-for suggestion's tags here -->
          </div>
        </div>
        <div class="suggestion-header-buttons">
          <!-- <svg-icon icon-name="more"><icon-more /></svg-icon> -->
        </div>
      </div>

      <suggestion-content
        :s="suggestion">
      </suggestion-content>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

import SuggestionContent from './SuggestionContent';
// import IconArrow from '../icons/IconArrow';
// import IconMore from '../icons/IconMore';
// import SvgIcon from '../icons/SvgIcon';

export default {
  components: {
    SuggestionContent,
    // IconArrow,
    // IconMore,
    // SvgIcon
  },
  data: () => ({
    suggestion: null
  }),
  created() {
    // TODO: Use getters
    axios
      .get(
        'http://localhost:8080/api/suggestions/' +
          this.$route.params.suggestionID
      )
      .then(response => {
        this.suggestion = response.data.data;
      })
      .catch(e => {
        console.log('Error in fetching Suggestion data: ');
        console.log(e);
      });
  },
  methods: {
    goToSuggestions: function() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
div.suggestion {
  width: 60vw;
  padding: 40px 20%;
  overflow: hidden;
}

div.back-button {
  color: #1ea195;
  font-weight: 800;
  font-size: 16px;
  text-align: left;
  margin-left: 6px;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

div.back-button a:hover {
  cursor: pointer;
  cursor: hand;
}

div.back-button svg {
  margin: 0 -15px -27px 0;
  width: 37px;
  height: 37px;
}

div.suggestion-container {
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  text-align: left;
}

div.suggestion-header {
  margin: 35px 40px 20px;
  position: relative;
}

div.suggestion-header-headline {
  line-height: 45px;
  display: inline-block;
  width: 80%;
  height: 100px;
}

h1.suggestion-title {
  display: inline;
  font-weight: 900;
  vertical-align: middle;
  text-transform: lowercase;
  text-transform: capitalize;
}

p.suggestion-status {
  display: inline;
  margin-left: 10px;
  padding: 3px 10px;
  border-radius: 2px;
  color: #ffffff;
  background-color: #58ba81;
  font-weight: 600;
  font-size: 16px;
  vertical-align: middle;
  text-transform: lowercase;
}

div.suggestion-header-buttons {
  position: absolute;
  top: 0px;
  right: 0px;
  bottom: 0px;
  display: inline-block;
  width: 20%;
  height: 100px;
  text-align: right;
}

@media (max-width: 700px) {
  div.suggestion {
    width: 80vw;
    padding: 10px 10% 20px;
  }

  div.suggestion-header-headline,
  div.suggestion-header-buttons {
    width: 100%;
    height: initial;
    position: initial;
    text-align: left;
  }
}

.suggestion-type {
  font-size: 14px;
  font-weight: 600;
  background-color: #f2994a;
  color: #ffffff;
  padding: 3px 10px;
  margin-left: 10px;
  border-radius: 2px;
  text-transform: lowercase;
}
</style>
