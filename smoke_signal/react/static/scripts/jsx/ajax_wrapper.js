module.exports = {
  getRequest: (url, callback) => {
    let request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = () => {
      if (request.status >= 200 && request.status < 400) {
        const data = JSON.parse(request.responseText);
        callback(data);
      } else {
        console.error(url, request.responseText);
      }
    };
    request.onerror = () => {
      console.error(url);
    };
    request.send();
  },

  postJSONRequest: (url, data, callback) => {
    let request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.setRequestHeader('Content-Type',
                             'application/json; charset=UTF-8');
    request.onload = () => {
      if (request.status >= 200 && request.status < 400) {
        const data = JSON.parse(request.responseText);
        callback(data);
      } else {
        console.error(url, request.responseText);
      }
    };
    request.onerror = () => {
      console.error(url);
    };
    request.send(JSON.stringify(data));
  }
};
