import axios from 'axios'

const apiUrl = process.env.VUE_APP_API_URL

const choresUrl = apiUrl + 'chores/'

function detailUrl(id) {
  return choresUrl + id + '/'
}

export default {
  list() {
    return axios.get(choresUrl);
  },

  complete(id) {
    var url = detailUrl(id) + 'complete/'
    return axios.post(url);
  }
}
