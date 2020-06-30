<template>
<div id="app">
  <b-container>
    <b-row>
      <b-col>
	<Header></Header>
	<hr/>
	<Toolbar></Toolbar>
      </b-col>
    </b-row>
  </b-container>
</div>
</template>

<script>
import Header from './components/Header.vue'
import Toolbar from './components/Toolbar.vue'

export default {
  name: 'App',
  components: {
    Header,
    Toolbar,
  }
}
</script>

<style>
#app {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}

#app div.container {
    max-width: 46rem;
}
</style>
