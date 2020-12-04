
import React, { Component } from 'react'; //Importamos react
import ReactDOM from 'react-dom';
import Uploader from './components/Uploader';

class Root extends Component {
   render() {
     return(
       <Uploader />
     )
   }
}
let container = document.getElementById('upload-app');
let component = <Root />;
ReactDOM.render(component, container);