<template>
  <div id="dashboard">
    <TheNavbar />
    <div id="contents">
      <router-view></router-view>
    </div>
    <TheFooter />
  </div>
</template>

<script>
import TheNavbar from "./TheNavbar.vue";
import TheFooter from "./TheFooter.vue";

export default {
  name: "TheLayout",
  components: {
    TheNavbar,
    TheFooter,
  },
};
</script>

<style lang="scss" scoped>
</style>
