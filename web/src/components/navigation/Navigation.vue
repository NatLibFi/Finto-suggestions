<template>
  <div class="navigation">

    <div class="nav-content">
      <div class="nav-title">
        <img @click="returnToHome" src="./finto-logo.svg" alt="">
        <span>Finto – Käsite-ehdotukset</span>
      </div>
      <div class="nav-menu" @click="showDropdown = true">
        <div class="user-bubble">
          <span unselectable="on">{{ userInitials }}</span>
        </div>
        <div class="nav-menu-user">
          <p>{{ userName }}</p>
        </div>
        <svg-icon icon-name="triangle"><icon-triangle /></svg-icon>
      </div>
      <!-- Mobile menu shown below screen width of 700px -->
      <div class="nav-menu-mobile" @click="showMobileDropdown = true">
        <svg-icon icon-name="more"><icon-more/></svg-icon>
      </div>
    </div>

    <div v-if="showDropdown" v-on-clickaway="closeDropdown" class="nav-menu-dropdown dropdown">
      <div>Profiili</div>
      <div>Asetukset</div>
      <div>Kirjaudu ulos</div>
    </div>

    <div
      v-if="showMobileDropdown"
      v-on-clickaway="closeMobileDropdown"
      class="nav-mobile-dropdown dropdown">
      <div class="nav-mobile-dropdown-header">
        <div class="user-bubble">
          <span unselectable="on">{{ userInitials }}</span>
        </div>
        <div class="nav-dropdown-user">
          <p>{{ userName }}</p>
        </div>
      </div>
      <div class="nav-mobile-dropdown-content">
        <div>Profiili</div>
        <div>Asetukset</div>
        <div>Kirjaudu ulos</div>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '../icons/SvgIcon';
import IconMore from '../icons/IconMore';
import IconTriangle from '../icons/IconTriangle';
import { directive as onClickaway } from 'vue-clickaway';

export default {
  components: {
    SvgIcon,
    IconMore,
    IconTriangle
  },
  directives: {
    onClickaway: onClickaway
  },
  data: () => ({
    userInitials: 'MP',
    userName: 'Miki Pernu',
    showDropdown: false,
    showMobileDropdown: false
  }),
  methods: {
    returnToHome: function() {
      this.$router.push('/');
    },
    closeDropdown: function() {
      this.showDropdown = false;
    },
    closeMobileDropdown: function() {
      this.showMobileDropdown = false;
    }
  },
  mounted: function() {
    document.addEventListener('keydown', e => {
      if (e.keyCode == 27) {
        this.closeDropdown();
        this.closeMobileDropdown();
      }
    });
  }
};
</script>

<style scoped>
div.navigation {
  width: 100%;
  overflow: hidden;
  border-bottom: 2px solid #f5f5f5;
  background-color: #ffffff;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* IE10+/Edge */
  user-select: none; /* Standard */
}

div.nav-content {
  position: relative;
  height: 60px;
}

div.nav-title {
  position: absolute;
  top: 50%;
  left: 40px;
  transform: perspective(1px) translateY(-50%);
  height: 60px;
  line-height: 60px;
  width: 45%;
}

div.nav-title img {
  position: absolute;
  top: 51%;
  left: 0;
  transform: perspective(1px) translateY(-50%);
  cursor: pointer;
  cursor: hand;
}

div.nav-title img:hover {
  opacity: 0.9;
}

div.nav-title span {
  display: inline-block;
  position: absolute;
  top: 56%;
  left: 90px;
  transform: perspective(1px) translateY(-50%);
  font-weight: 600;
}

div.nav-menu {
  position: absolute;
  right: 0;
  padding: 0 40px 0 20px;
  top: 52%;
  height: 100%;
  transform: perspective(1px) translateY(-50%);
  color: #1ea195;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  cursor: hand;
}

div.nav-menu .user-bubble {
  position: relative;
  top: 50%;
  transform: perspective(1px) translateY(-50%);
  overflow: hidden;
}

div.nav-menu .nav-menu-user {
  display: inline;
  vertical-align: middle;
}

div.nav-menu .nav-menu-user p {
  display: inline;
  margin: 0 0 0 14px;
}

div.nav-menu svg {
  margin: 0 0 -13px 10px;
}

div.nav-menu-mobile {
  display: none;
  position: absolute;
  right: 0;
  padding-right: 40px;
  top: 50%;
  transform: perspective(1px) translateY(-50%);
  height: 100%;
}

div.nav-menu-mobile svg {
  position: relative;
  top: 55%;
  transform: perspective(1px) translateY(-50%);
  display: inline-block;
  margin: 0 0 -8px 10px;
  background-size: 24px 24px;
}

div.nav-menu-dropdown {
  position: absolute;
  z-index: 2;
  top: 55px;
  right: 40px;
  width: 200px;
}

div.nav-menu-dropdown div {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
}

div.nav-menu-dropdown div:last-of-type {
  border-bottom: none;
}

div.nav-menu-dropdown div:hover {
  background-color: #f3fbfa;
  cursor: pointer;
  cursor: hand;
}

div.nav-mobile-dropdown {
  display: none;
  position: absolute;
  z-index: 2;
  top: 50px;
  right: 1px;
  width: 300px;
}

div.nav-mobile-dropdown-header {
  padding: 20px;
  padding-top: 24px;
  border-bottom: 1px solid #f5f5f5;
}

div.nav-mobile-dropdown-header .user-bubble {
  height: 50px;
  width: 50px;
  line-height: 50px;
  font-size: 16px;
}

div.nav-mobile-dropdown-header .nav-dropdown-user {
  display: inline-block;
  margin-left: 30px;
  font-size: 16px;
  line-height: 16px;
}

div.nav-mobile-dropdown-content div {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
}

div.nav-mobile-dropdown-content div:last-of-type {
  padding: 16px 20px;
  border-bottom: 1px solid #f5f5f5;
}

div.nav-mobile-dropdown-content div:hover {
  background-color: #f3fbfa;
  cursor: pointer;
  cursor: hand;
}

@media (max-width: 700px) {
  div.nav-title {
    left: 20px;
  }

  div.nav-title span {
    display: none;
  }

  div.nav-menu {
    display: none;
  }

  div.nav-menu-mobile {
    display: initial;
    padding-right: 20px;
  }

  div.nav-menu-dropdown {
    display: none;
  }

  div.nav-mobile-dropdown {
    display: initial;
  }
}

.dropdown {
  font-size: 15px;
  font-weight: 600;
  color: #555555;
  text-align: left;
  background-color: #ffffff;
  border: 1px solid #e1e1e1;
  border-radius: 2px;
  -webkit-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  -moz-box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
  box-shadow: 6px 8px 17px -6px rgba(80, 80, 80, 0.35);
}

.user-bubble {
  display: inline-block;
  height: 35px;
  width: 35px;
  border-radius: 35px;
  line-height: 35px;
  text-align: center;
  background-color: #804af2;
  color: #ffffff;
  font-size: 14px;
  font-weight: 800;
}
</style>
