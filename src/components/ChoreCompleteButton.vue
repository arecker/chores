<template>
<b-button size="lg" variant="outline-primary"
	  v-bind:disabled="disabled"
	  v-on:click.stop="complete(chore)">
  <b-spinner small label="Completing..." v-if="showSpinner"></b-spinner>
  <b-icon-check v-else></b-icon-check>
</b-button>
</template>

<script>
export default {
  name: 'ChoreCompleteButton',
  props: ['chore'],
  data () {
    return {
      disabled: false,
      showSpinner: false,
    }
  },
  methods: {
    complete (chore) {
      const app = this

      if (app.disabled) return

      app.disabled = true
      app.showSpinner = true
      chore.complete()

      app.disabled = false
      app.showSpinner = false
    },
  }
}
</script>

<style scoped>
</style>
