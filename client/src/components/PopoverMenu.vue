<template>
  <v-layout>
    <v-navigation-drawer :modelValue="modelValue" @update:modelValue="newValue => modelValue=newValue">
      <v-list density="compact" nav>
        <v-list-item prepend-icon="mdi-home-city" title="Home" value="home"></v-list-item>
        <v-list-item prepend-icon="mdi-account" title="My Account" value="account"></v-list-item>
        <v-list-item prepend-icon="mdi-account-group-outline" title="Users" value="users"></v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-layout>
</template>
<script setup>
defineProps(['modelValue'])
defineEmits(['update:modelValue'])
</script>
