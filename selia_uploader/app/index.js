
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Uploader from './components/Uploader';

import store from './store';
import { Provider } from 'react-redux';

class Root extends Component {
   render() {
     return(
      <Provider store={store}>
        <Uploader />
      </Provider>
     )
   }
}
let container = document.getElementById('upload-app');
let component = <Root />;
ReactDOM.render(component, container);