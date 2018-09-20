<template>
  <div class="container">
    <h3>YSE - YSAn ja YSOn käsite-ehdotukset</h3>
    <div class="welcomeText">
      <p>
        Tämä palvelu on YSA/YSO -käsite-ehdotuksille ja niiden etenemisen seuraamiselle.
        Voit selata ja kommentoida ehdotuksia täällä. Ehdotusten selaaminen onnistuu ilman käyttäjätunnuksia,
        mutta kommentointi edellyttää tunnuksen luomista. Voit osoittaa tukesi ehdotukselle kommentoimalla sitä.
        Halutessasi voit nopeuttaa ehdotuksen käsittelyä jättämällä ehdotuksen kommenttikenttään täsmennyksiä ja lisätietoja.
        Uusien käsite-ehdotuksien tekeminen onnistuu Fintossa.
      </p>
    </div>
    <div>
      <suggestion-search-form />
    </div>
    <div>
      <filter-suggestions />
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
  }
}
</script>

<style scoped>
.container {}
.welcomeText {}
</style>
