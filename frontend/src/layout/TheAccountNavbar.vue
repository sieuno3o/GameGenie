<template>
  <div id="navbar" class="flex-center">
    <router-link to="/">
      <img src="../assets/image/logo.png" class="navLogoImg">
    </router-link>
  </div>
</template>

<script>
export default {
  name: "TheAccountNavbar",
};
</script>

<style lang="scss" scoped>
#navbar {
  width: auto;
  height: 55px;
  justify-content: space-between;
}

.navLogoImg {
  width: 140px;
  margin-top: -4px;
  padding-left: 25px;
}

</style>
