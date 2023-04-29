<template>
  <PopoverMenu v-model="popoverMenu"></PopoverMenu>
  <div class="appbar-btn" @click.stop="popoverMenu = !popoverMenu">
    <Hamburger size="25"></Hamburger>
  </div>
  <div class="appbar">
    <div class="appbar-title">Friday</div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import Hamburger from "@/components/icons/Hamburger.vue";
import PopoverMenu from "@/components/PopoverMenu.vue";

const popoverMenu = ref(false);
</script>

<style lang="scss">
@use "@/styles/settings.scss" as *;
.appbar{
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  display: flex;
  align-items: center;
  background-color: $white;
  padding-inline: 10px;
}
.appbar-btn{
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 8px;
  position: fixed;
  z-index: 1;
  top: 10px;
  left: 10px;
}
.appbar-btn:hover{
  background-color: $gray;
}
.appbar-title{
  font-size: 18px;
  font-weight: 600;
  margin-inline-start: 10px;
  margin:auto;
}
</style>
