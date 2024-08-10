<template>
    <input type="number" v-model.number="volume" placeholder="Enter volume" />
  </template>
  
  <script>
  export default {
    props: ['value'],
    computed: {
      volume: {
        get() { return this.value; },
        set(value) { this.$emit('update:modelValue', value); }
      }
    }
  }
  </script>
  