<template>
<b-list-group flush>
  <b-list-group-item
    action
    class="d-flex justify-content-between align-items-center"
    v-for="chore in chores"
    v-bind:key="chore.id">
    <span>
      <h5>{{ chore.name }}</h5>
      <p class="crowded" v-bind:class="chore.cssFromDueDate()">Due: {{ chore.prettyDate() }}</p>
      <p class="text-muted crowded">{{ chore.prettyCadence() }}, Assigned: {{ chore.prettyAssignee() }}</p>
    </span>
    <b-button size="lg" variant="outline-primary"
	      v-bind:disabled="chore.buttonDisabled"
	      v-on:click.stop="chore.complete()">
      <b-icon v-bind:icon="chore.buttonIcon"></b-icon>
    </b-button>
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

    app.libs.chores.all().then(results => {
      app.chores = results
    })
  }
}
</script>

<style scoped>
p.crowded {
    margin-bottom: 0;
}
</style>
