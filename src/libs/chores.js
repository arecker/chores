import moment from 'moment'

import api from './api.js'

function Chore (data) {
  var self = {}

  self.complete = async function () {
    var response = await api.complete(self.id)
    self.reloadData(response.data)
  }

  self.isOverdue = function () {
    return moment(self.nextDueDate).diff(moment(), 'days') < 0
  }

  self.reloadData = function (data) {
    self.name = data.name
    self.id = data.id
    self.nextDueDate = data.next_due_date
    self.cadence = data.cadence
    self.assignee = data.assignee
  }

  self.reloadData(data)

  return self
}

export default {
  async all () {
    var response = await api.list()
    return response.data.map(Chore)
  }
}
