<template>
  <svg xmlns="http://www.w3.org/2000/svg" :width="props.size" :height="props.size" :color="props.color" viewBox="0 0 24 18" fill="none">
    <path d="M18 16.2C18 16.8627 17.4627 17.4 16.8 17.4L1.2 17.4C0.537281 17.4 -4.69706e-08 16.8627 -1.04907e-07 16.2C-1.62844e-07 15.5373 0.537281 15 1.2 15L16.8 15C17.4627 15 18 15.5373 18 16.2ZM1.2 10.2L22.8 10.2C23.4627 10.2 24 9.66267 24 9C24 8.33728 23.4627 7.8 22.8 7.8L1.2 7.8C0.53728 7.8 -7.92288e-07 8.33728 -7.34351e-07 9C-6.76419e-07 9.66267 0.53728 10.2 1.2 10.2ZM1.2 3L12 3C12.6627 3 13.2 2.46272 13.2 1.8C13.2 1.13733 12.6627 0.599999 12 0.6L1.2 0.6C0.53728 0.600001 -1.42173e-06 1.13733 -1.3638e-06 1.8C-1.30586e-06 2.46272 0.53728 3 1.2 3Z" fill="black"/>
  </svg>
</template>
<script setup>
const props = defineProps({
  size: {
    type: String,
    default: "20"
  },
  color: {
    type: String,
    default: "black"
  }
})
</script>
