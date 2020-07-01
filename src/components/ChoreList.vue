<template>
<b-list-group flush>
  <b-list-group-item v-for="chore in chores" v-bind:key="chore.id">
    <pre>{{ chore.name }}</pre>
  </b-list-group-item>
</b-list-group>
</template>

<script>
export default {
  name: 'ChoreList',
  data () {
    return {
      chores: [],
    }
  },
  mounted () {
    const app = this;
    
    app.$api.list().then(response => {
      app.chores = response.data
    })
  }
}
</script>

<style scoped>

</style>
