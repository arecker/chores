<template>
<b-list-group flush>
  <ChoreListItem :chore="chore" v-for="chore in chores" v-bind:key="chore.id"></ChoreListItem>
</b-list-group>
</template>

<script>
import ChoreListItem from './ChoreListItem.vue'

export default {
  name: 'ChoreList',
  components: { ChoreListItem },
  data () {
    return {
      chores: [],
    }
  },
  mounted () {
    const app = this;

    app.libs.chores.all().then(results => {
      app.chores = results
    })
  }
}
</script>

<style scoped>
</style>
