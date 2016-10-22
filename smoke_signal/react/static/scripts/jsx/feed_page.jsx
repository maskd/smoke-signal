import React from 'react';
import ReactDOM from 'react-dom';
import AddFeedForm from './add_feed_form.jsx';
import FeedList from './feed_list.jsx';
import EntryList from './entry_list.jsx';
import { IndexRedirect, Route, Router, hashHistory } from 'react-router';

var FeedPage = React.createClass({
  render: function() {
    return (
      <div id="feed_page">
        <AddFeedForm />
        {this.props.children}
      </div>
    );
  }
});

ReactDOM.render((
  <Router history={hashHistory}>
    <Route path="/" component={FeedPage}>
      <IndexRedirect to="/feeds" />
      <Route path="/feeds" component={FeedList}>
        <Route path="/feeds/:id" component={EntryList} />
      </Route>
    </Route>
  </Router>
  ), document.getElementById('container')
);
