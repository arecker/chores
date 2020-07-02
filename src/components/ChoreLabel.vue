<template>
<span>
  <h5>{{ chore.name }}</h5>
  <p v-bind:class="computeCssClass(chore)">Due: {{ chore.nextDueDate | date  }}</p>
  <p class="text-muted crowded">{{ chore.cadence | cadence }}, Assigned: {{ chore.assignee | assignee }}</p>
</span>
</template>

<script>
import moment from 'moment'
  
export default {
  name: 'ChoreLabel',
  props: ['chore'],
  methods: {
    computeCssClass (chore) {
      if (chore.isOverdue()) {
	return 'text-danger'
      }
      return 'text-muted'
    }
  },

  filters: {
    cadence (code) {
      return {
	0: 'Weekly',
	1: 'Monthly',
	2: 'Every Two Weeks',
	3: 'Every Two Months',
	4: 'Every Three Months'
      }[code]
    },
    
    date (dateStr) {
      return moment(dateStr).format('dddd, MMMM D Y')      
    },
    
    assignee (code) {
      return {
	0: 'Alex',
	1: 'Marissa'
      }[code]
    }
  }
}
</script>

<style scoped>
  span p:first-of-type {
    margin-bottom: 0;
  }
</style>
