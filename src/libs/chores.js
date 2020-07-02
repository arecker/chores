import moment from 'moment'

import api from './api.js'

function Chore(data) {
  var self = {};

  self.data = data;

  self.name = data.name;

  self.complete = function() {
    alert('complete')
  };

  self.cssFromDueDate = function() {
    if (self.isOverdue()) {
      return 'text-danger'
    }
    return 'text-muted'
  };

  self.isOverdue = function() {
    return moment(self.data.next_due_date).diff(moment(), 'days') < 0;
  };

  self.prettyDate = function() {
    return moment(self.next_due_date).format('dddd, MMMM D Y');
  };

  self.prettyCadence = function() {
    return {
      '0': 'Weekly',
      '1': 'Monthly',
      '2': 'Every Two Weeks',
      '3': 'Every Two Months',
      '4': 'Every Three Months',
    }[self.data.cadence]
  };

  self.prettyAssignee = function() {
    return {
      '0': 'Alex',
      '1': 'Marissa',
    }[self.data.assignee]
  };

  return self;
}

export default {
  async all () {
    var response = await api.list()
    return response.data.map(Chore)
  },
}
