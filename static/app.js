var Chores = (function() {
  var api = {};

  api.list = function() {
    return axios.get('http://localhost:5000/api/chores/')
  };

  return api;
}());

var app = new Vue({
  el: '#app',

  data: {
    chores: [],
  },

  mounted: function() {
    var app = this;
    
    Chores.list().then(function(response) {
      app.chores = response.data;
    });
  },

  filters: {
    assignee: function(value) {
      return {
	'0': 'Alex',
	'1': 'Marissa',
      }[value + ''] || 'Unknown';
    }
  }
});
