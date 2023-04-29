<template>
  <div class="lds-ellipsis">
    <div class="lds-ball">
    </div>
    <div class="lds-ball"></div>
    <div class="lds-ball"></div>
    <div class="lds-ball"></div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
const props = defineProps({
  size: {
    type: Number,
    default: 80,
  },
  color: {
    type: String,
    default: "green",
  },
});

//Increase
//Original size 80, ball size 13
// 13/80 = 0.1625
const ballShrinkMultiplier = 0.1625;
// Original ball css top: value 33
// 33/80 = 0.4125
const ballTopMultiplier = 0.4125;
//Original low left value 8 (for div:nth-child(1 & 2))
// 8 / 80 = 0.1
const ballLeftMultiplier = 0.1;
//Original higher left value 32 (for div:nth-child(3))
// 32 / 80 = 0.4
const ballLeftMultiplier2 = 0.4;
//Original highest left value 56 (for div:nth-child(4))
// 56 / 80 = 0.7
const ballLeftMultiplier3 = 0.7;
//Original ball travel distance 24
// 24 / 80 = 0.3
const ballTravelMultiplier = 0.3;

const size = computed(()=>props.size.toString() + "px")
const ballTop = computed(()=>(props.size * ballTopMultiplier).toString() + "px")
const ballSize = computed(()=>(props.size * ballShrinkMultiplier).toString() + "px");
const ballLeftSize = computed(()=>(props.size * ballLeftMultiplier).toString() + "px");
const ballLeftSize2 = computed(()=>(props.size * ballLeftMultiplier2).toString() + "px");
const ballLeftSize3 = computed(()=>(props.size * ballLeftMultiplier3).toString() + "px");
const ballTravelDistance = computed(()=>(props.size * ballTravelMultiplier).toString() + "px");
</script>

<style scoped lang="scss">
@use "@/styles/settings.scss" as *;

.lds-ellipsis {
  display: inline-block;
  position: relative;
  height: v-bind("size");
  width: v-bind("size");
}
.lds-ellipsis div {
  position: absolute;
  top: v-bind("ballTop");
  width: v-bind("ballSize");
  height: v-bind("ballSize");
  border-radius: 50%;
  background: v-bind("props.color");
  animation-timing-function: cubic-bezier(0, 1, 1, 0);
}
.lds-ellipsis div:nth-child(1) {
  left: v-bind('ballLeftSize');
  animation: lds-ellipsis1 0.6s infinite;
}
.lds-ellipsis div:nth-child(2) {
  left: v-bind('ballLeftSize');
  animation: lds-ellipsis2 0.6s infinite;
}
.lds-ellipsis div:nth-child(3) {
  left: v-bind('ballLeftSize2');
  animation: lds-ellipsis2 0.6s infinite;
}
.lds-ellipsis div:nth-child(4) {
  left: v-bind('ballLeftSize3');
  animation: lds-ellipsis3 0.6s infinite;
}
@keyframes lds-ellipsis1 {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}
@keyframes lds-ellipsis3 {
  0% {
    transform: scale(1);
  }
  100% {
    transform: scale(0);
  }
}
@keyframes lds-ellipsis2 {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(20px, 0);
  }
}


</style>
