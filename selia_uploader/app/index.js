import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Uploader from './components/Uploader';

import store from './store';
import { Provider } from 'react-redux';
import { Provider as AtomProvider } from 'jotai';

class Root extends Component {
   render() {
     return(
      <Provider store={store}>
        <AtomProvider>
          <Uploader />
        </AtomProvider>
      </Provider>
     )
   }
}
let container = document.getElementById('upload-app');
let component = <Root />;
ReactDOM.render(component, container);