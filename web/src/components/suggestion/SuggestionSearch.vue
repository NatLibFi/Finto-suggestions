<template>
  <div class="search-container  ">
    <h3>YSE - YSAn ja YSOn käsite-ehdotukset</h3>
    <div class="welcome-text">
      <p>{{ welcomeText }}</p>
      <p class="meetings-link">
        <strong>
          Voit tarkastella tulevia YSO-kokouksia <a @click="goToMeetings()">täällä</a>.
        </strong>
      </p>
    </div>
    <div>
      <suggestion-search-form />
    </div>
    <div>
      <filter-suggestions :isMeeting="false" />
    </div>
  </div>
</template>

<script>
import SuggestionSearchForm from './SuggestionSearchForm';
import FilterSuggestions from './FilterSuggestions';

export default {
  components: {
    SuggestionSearchForm,
    FilterSuggestions
  },
  data: () => ({
    welcomeText: `Tämä palvelu on YSA/YSO -käsite-ehdotuksille ja niiden etenemisen seuraamiselle.
      Voit selata ja kommentoida ehdotuksia täällä. Ehdotusten selaaminen onnistuu ilman
      käyttäjätunnuksia,mutta kommentointi edellyttää tunnuksen luomista. Voit osoittaa
      tukesi ehdotukselle kommentoimalla sitä. Halutessasi voit nopeuttaa ehdotuksen
      käsittelyä jättämällä ehdotuksen kommenttikenttään täsmennyksiä ja lisätietoja.
      Uusien käsite-ehdotuksien tekeminen onnistuu Fintossa.`
  }),
  methods: {
    goToMeetings: function() {
      this.$router.push('/meetings');
    }
  }
};
</script>

<style scoped>
.search-container {
  width: 60vw;
  margin: 20px 20vw 0;
}
.welcome-text {
  text-align: left;
}
.meetings-link a:hover {
  cursor: pointer;
  cursor: hand;
}
</style>
