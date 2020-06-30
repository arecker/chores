<template>
<div>
  <b-button-toolbar key-nav aria-label="Toolbar with button groups">
    <b-button-group class="mx-1">
      <b-button variant="info" v-on:click="click()">New</b-button>
    </b-button-group>
  </b-button-toolbar>
</div>
</template>

<script>
export default {
  name: 'Toolbar',
  methods: {
    click: function() {
      alert('hello!');
    }
  }
}
</script>

<style scoped>

</style>
