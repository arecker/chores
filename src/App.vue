<template>
<div id="app">
  <b-container>
    <b-row>
      <b-col>
	<Header></Header>
	<hr/>
	<Toolbar></Toolbar>
	<hr/>
	<ChoreList></ChoreList>
      </b-col>
    </b-row>
  </b-container>
</div>
</template>

<script>
import Header from './components/Header.vue'
import Toolbar from './components/Toolbar.vue'
import ChoreList from './components/ChoreList.vue'

export default {
  name: 'App',
  components: {
    Header,
    Toolbar,
    ChoreList,
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
