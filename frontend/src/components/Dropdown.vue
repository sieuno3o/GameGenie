<template>
  <div id="dropdown-container">
    <div id="dropdown" class="full-outline dropdown-border flex-left button2" @click="handleDropdown">
      <div id="dropdown-title" class="flex-left">{{ title }}</div>
      <div id="dropdown-icon" class="flex-center">
        <b-icon icon="chevron-down" :hidden="!isHidden"></b-icon>
        <b-icon icon="chevron-up" :hidden="isHidden"></b-icon>
      </div>
    </div>
    <div id="dropdown-itembox" class="full-outline flex-col" :hidden="isHidden">
      <div class="full-outline dropwdown-items flex-left" v-for="item in items" :key="item" @click="handleClickItems">
        <div class="dropwdown-text button2">{{ item }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CustomDropdown",
  props: {
    items: Array,
  },
  data() {
    return {
      title: null,
      isHidden: true,
    };
  },
  created() {
    this.title = this.items[0];
  },
  methods: {
    handleDropdown() {
      const dropdown = document.querySelector("#dropdown");

      if (dropdown) {
        dropdown.classList.toggle("dropdown-border");
        dropdown.classList.toggle("dropdown-onclick-border");
      }

      this.isHidden = !this.isHidden;
    },
    handleClickItems(event) {
      const clickedItem = event.target;
      const selectedItem = document.querySelector(".dropwdown-selected");

      if (selectedItem) {
        selectedItem.classList.remove("dropwdown-selected");
      }

      if (clickedItem.className === "dropwdown-items") {
        clickedItem.classList.add("dropwdown-selected");
      } else if (clickedItem.className === "dropwdown-text") {
        clickedItem.parentNode.classList.add("dropwdown-selected");
      }

      this.title = clickedItem.innerText;
      this.handleDropdown();
    },
  },
};
</script>

<style lang="scss" scoped>
#dropdown-container {
  position: relative;
}

#dropdown {
  width: 152px;
  height: 40px;
  padding: 8px 12px 8px 8px;

  border-radius: 5px;
  background-color: white;
}

.dropdown-border {
  border: 1px solid $SUB-COLOR-GRAY;
}

.dropdown-onclick-border {
  border: 1px solid $MAIN-COLOR-GREEN;
}

#dropdown:hover {
  border: 1px solid $MAIN-COLOR-GREEN;
}

#dropdown-title {
  width: 96px;
  height: 24px;
  padding-right: 8px;
  border-right: 1px solid $SUB-COLOR-GRAY;
}

#dropdown-icon {
  width: 24px;
  height: 24px;
  margin-left: 12px;
}

#dropdown-itembox {
  width: 152px;
  max-height: 160px;
  border-radius: 5px;
  box-shadow: 2px 2px 2px rgba(69, 69, 69, 0.15);

  position: absolute;
  top: 100%;
  left: 0;
  z-index: 2;

  overflow-x: hidden;
}

.dropwdown-items {
  width: 152px;
  height: 40px;
  padding: 8px;
  background-color: white;
}

.dropwdown-selected {
  background-color: $MAIN-COLOR-GREEN;
}

.dropwdown-items:hover {
  background-color: $HOVER-COLOR;
}

.dropwdown-text {
  width: 88px;
  height: 24px;
  display: flex;
}

#dropdown-itembox::-webkit-scrollbar {
  width: 5px;
}

#dropdown-itembox::-webkit-scrollbar-thumb {
  background: #8e8e8e;
  border-radius: 10px;
}

#dropdown-itembox::-webkit-scrollbar-track {
  background: #fff;
}
</style>
