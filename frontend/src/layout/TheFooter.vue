<template>
  <div v-if="shouldShowFooter" :class="{ 'main-background': isMainPage }" id="footer">
    <span>GameGenie</span>
  </div>
</template>

<script>
export default {
  name: "TheFooter",
  computed: {
    isMainPage() {
      return this.$route.name === 'main' || this.$route.name === 'profile';
    },
    shouldShowFooter() {
      return this.$route.name !== 'recommends';
    }
  }
};
</script>

<style lang="scss" scoped>
.main-background {
  background-color: $MAIN-COLOR-SKYBLUE;
}

span {
  color: $MAIN-COLOR-GRAY;
}

#footer {
  padding: 170px 30px 50px 30px;
}
</style>
