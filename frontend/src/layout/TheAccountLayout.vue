<template>
  <div id="dashboard">
    <TheAccountNavbar />
    <div id="contents">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import TheAccountNavbar from "./TheAccountNavbar.vue";

export default {
  name: "TheAccountLayout",
  components: {
    TheAccountNavbar,
  },
};
</script>

<style lang="scss" scoped></style>
