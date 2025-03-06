<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navigacija from '@/components/Navigacija.vue';
</script>

<template>
  <Navigacija class="container"/>
  <RouterView class="container"/>
</template>

<style>
  body {
    zoom: 100%;
  }
  *{
    font-family: "Roboto Condensed", serif;
    font-optical-sizing: auto;
    font-weight:<weight>;
    font-style: normal;
  }
</style>
