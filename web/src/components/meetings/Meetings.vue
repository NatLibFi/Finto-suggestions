<template>
<div class="meetings">
  <div class="arrow-button">
    <a @click="goToHome" unselectable="on">
      <svg-icon icon-name="arrow"><icon-arrow /></svg-icon>
      Takaisin etusivulle
    </a>
  </div>
  <div class="meetings-header">
    <div class="header-content">
      <h3>Ehdotuksia käsittelevät kokoukset</h3>
      <p>
        YSA- ja YSO-käsite-ehdotuksia käsitellään neljä kertaa vuodessa YSA-kokouksissa.
        <br><br>
        Alla näet tulevien ja menneiden YSA-kokouksien asialistat.
      </p>
    </div>
  </div>
</div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconArrow from '../icons/IconArrow';

export default {
  components: {
    SvgIcon,
    IconArrow
  },
  methods: {
    goToHome: function() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.meetings {
  width: 60vw;
  margin: 40px 20vw 20px;
}

.arrow-button {
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

.arrow-button a:hover {
  cursor: pointer;
  cursor: hand;
}

.arrow-button svg {
  margin: 0 -15px -27px 0;
  width: 37px;
  height: 37px;
}

.meetings-header {
  text-align: left;
  background-color: #ffffff;
  border: 2px solid #f5f5f5;
  padding-left: 0; /* reset inital padding for ul tags */
}

.header-content {
  padding: 15px 40px;
}

.header-content p {
  font-weight: 500;
}

@media (max-width: 700px) {
  .meetings {
    width: 80%;
    margin: 40px 10vw 20px;
  }
}
</style>
