import 'isomorphic-fetch'

const _getRequest = url =>
      fetch(url, {
        credentials: 'same-origin',
      }).then((response) => {
        if (response.ok) {
          if (response.status === 200) {
            return response.json()
          } return []
        } throw Error(response.statusText)
      })

const _postJSONRequest = (url, data) => {
  const csrfToken = document.head.querySelector('[name=csrf-token]').content
  fetch(url, {
    method: 'post',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(data),
    credentials: 'same-origin',
  })
    .then((response) => {
      if (response.ok) {
        if (response.status === 200) {
          return response.json()
        } return []
      } throw Error(response.statusText)
    })
}

const addFeed = url => _postJSONRequest('/feeds/', { url })

const getFeedList = options =>
  _getRequest('/feeds/', options)
  .then(response => response._embedded.feeds)

const refreshFeed = feedId =>
      _postJSONRequest(`/feeds/${feedId}`)

const fetchFeedEntries = feedId =>
      _getRequest(`/feeds/${feedId}/all`)

const changeEntryStatus = (feedId, entryId, newStatus) =>
      _postJSONRequest(`/feeds/${feedId}/${entryId}`,
                       newStatus)

const fetchEntries = predicate =>
      _getRequest(`/feeds/${predicate}`)
      .then(response => response._embedded.entries)

module.exports = {
  addFeed,
  getFeedList,
  refreshFeed,
  fetchFeedEntries,
  changeEntryStatus,
  fetchEntries,
}
