<template>
<b-list-group-item
  action button
  class="d-flex justify-content-between align-items-center"
  v-bind:key="chore.id">
  <ChoreLabel :chore="chore"></ChoreLabel>
  <ChoreCompleteButton :chore="chore"></ChoreCompleteButton>
</b-list-group-item>
</template>

<script>
import ChoreCompleteButton from './ChoreCompleteButton.vue'
import ChoreLabel from './ChoreLabel.vue'

export default {
  name: 'ChoreListItem',
  props: ['chore'],
  components: { ChoreCompleteButton, ChoreLabel },
}
</script>

<style scoped>
</style>
