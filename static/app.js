var Chores = (function() {
  var api = {};

  var choresUrl = GLOBALS.api_url + 'chores/';

  var detailUrl = function(id) {
    return choresUrl + id + '/';
  };

  api.list = function() {
    return axios.get(choresUrl);
  };

  api.update = function(chore) {
    return axios.put(detailUrl(chore.id), chore);
  };

  api.delete = function(id) {
    return axios.delete(detailUrl(id));
  };

  api.complete = function(id) {
    var url = detailUrl(id) + 'complete/'
    return axios.post(url);
  };

  api.create = function(chore) {
    return axios.post(choresUrl, chore);
  };

  return api;
}());

var app = new Vue({
  el: '#app',

  data: {
    chores: [],
    choreEdit: {},
    choreEditErrors: [],
    choreEditMissing: [],
    choreEditSummary: '',
    globals: GLOBALS,
    filters: {
      days: 0,
      assignee: 'None',
      cadence: 'None',
    },
  },

  mounted: function() {
    var app = this;

    // populate chores
    Chores.list().then(function(response) {
      app.chores = response.data;
    });
  },

  filters: {
    displayAssignee: function(value) {
      return GLOBALS.assignees[value] || 'Unknown';
    },
    displayCadence: function(value) {
      return GLOBALS.cadences[value] || 'Unknown';
    },
    prettyDate: function(date) {
      return moment(date).format('dddd, MMMM D Y');
    },
  },

  computed: {
    computedChores: function() {
      var app = this;
      return app.chores.filter(function(c) {

	// days
	if (app.filters.days == '0') {
	  var now = moment(moment().format('YYYY-MM-DD'));
	  var then = moment(c.next_due_date);
	  if (!then.isSameOrBefore(now)) {
	    return false;
	  }
	}

	// assigned
	if (app.filters.assignee !== 'None') {
	  if (c.assignee != app.filters.assignee) {
	    return false;
	  }
	}

	// cadence
	if (app.filters.cadence !== 'None') {
	  if (c.cadence != app.filters.cadence) {
	    return false;
	  }
	}

	return true;
      }).sort(function(a, b){
	return moment(a.next_due_date).diff(b.next_due_date);
      });
    },
  },
  
  methods: {
    isOverdue: function(chore) {
      return moment(chore.next_due_date).diff(moment(), 'days') < 0;
    },
    choreClicked: function(chore) {
      console.log('editing ' + chore.id);
      $('#modal').modal('show');
      this.choreEdit = chore;
    },
    resetForm: function() {
      var app = this;

      app.choreEdit = {};
      app.choreEditSummary = '';
      app.choreEditMissing = [];
      app.choreEditErrors = [];
    },
    newClicked: function() {
      var app = this;
      app.resetForm();
    },
    deleteClicked: function() {
      var app = this;
      console.log('deleting ' + app.choreEdit.id);
      Chores.delete(app.choreEdit.id).then(function(response) {
	app.chores = app.chores.filter(function(chore) {
	  return chore.id != app.choreEdit.id;
	});

	$('#modal').modal('hide');
      }).catch(function(response) {
	console.log(response);
	app.choreEditSummary = 'Could not create chore!';
      });
    },
    choreCompleteClicked: function(chore) {
      var app = this;
      console.log('moving chore ' + chore.id + 'to next due date');
      Chores.complete(chore.id).then(function(response) {
	app.chores = app.chores.filter(function(thisChore) {
	  return thisChore.id != chore.id;
	});
	app.chores.push(response.data);
      }).catch(function(response) {
	console.log(response);
      });
    },
    saveClicked: function() {
      var app = this;

      if (!app.choreEdit.id) {
	console.log('saving new chore')
	Chores.create(app.choreEdit).then(function(response) {
	  var newChore = response.data;
	  app.chores.push(newChore);
	  $('#modal').modal('hide');
	}).catch(function(response) {
	  app.choreEditSummary = 'Could not create chore!';

	  var data = response.response.data;

	  if (data.missing) {
	    app.choreEditMissing = data.missing;
	  }

	  if (data.invalid) {
	    app.choreEditErrors = data.invalid;
	  }
	});
      } else {
	console.log('updating chore ' + this.choreEdit.id);
	Chores.update(app.choreEdit).then(function(response) {
	  console.log('Success: ' + response);
	  app.chores = app.chores.filter(function(thisChore) {
	    return thisChore.id != app.choreEdit.id;
	  });
	  app.chores.push(response.data);
	  $('#modal').modal('hide');
	}).catch(function(response) {
	  app.choreEditSummary = 'Could not update chore!';
	  console.log(response);
	  var data = response.response.data;

	  console.log(data);

	  if (data.missing) {
	    app.choreEditMissing = data.missing;
	  }

	  if (data.invalid) {
	    app.choreEditErrors = data.invalid;
	  }
	});
      }
    }
  }
});
